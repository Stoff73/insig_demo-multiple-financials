import pdfplumber
from pathlib import Path
import re
from typing import List, Dict, Any, Optional, Tuple
import logging
import pandas as pd
from io import StringIO

logger = logging.getLogger(__name__)

class AdvancedPDFToMarkdownConverter:
    """Advanced PDF to Markdown converter with superior table extraction"""
    
    def __init__(self):
        self.page_break = "\n\n---\n\n"
        
    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """
        Convert a PDF file to Markdown format with advanced table handling
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Markdown formatted string
        """
        markdown_content = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Add document title
                markdown_content.append(f"# {pdf_path.stem}\n\n")
                
                # Process each page
                for page_num, page in enumerate(pdf.pages, 1):
                    page_content = self._process_page_advanced(page, page_num)
                    if page_content:
                        markdown_content.append(page_content)
                        
                        # Add page break between pages (except last)
                        if page_num < len(pdf.pages):
                            markdown_content.append(self.page_break)
                            
        except Exception as e:
            logger.error(f"Error converting PDF: {str(e)}")
            raise
            
        return "\n".join(markdown_content)
    
    def _process_page_advanced(self, page, page_num: int) -> str:
        """Process a single PDF page with advanced table extraction"""
        page_content = []
        
        # Add page number as comment
        page_content.append(f"<!-- Page {page_num} -->\n")
        
        # Extract text with positions for better table detection
        chars = page.chars if hasattr(page, 'chars') else []
        words = page.extract_words() if hasattr(page, 'extract_words') else []
        
        # Try to extract tables with multiple strategies
        tables = self._extract_tables_advanced(page)
        
        # Get full text
        full_text = page.extract_text() or ""
        
        if tables:
            # Process page with tables
            content = self._integrate_tables_and_text(full_text, tables, page)
            page_content.append(content)
        elif full_text:
            # No tables, just process text
            processed_text = self._enhance_text_formatting(full_text)
            page_content.append(processed_text)
        
        return "\n".join(page_content)
    
    def _extract_tables_advanced(self, page) -> List[Dict]:
        """
        Advanced table extraction using multiple detection methods
        """
        extracted_tables = []
        
        # Method 1: Use explicit table finding with custom settings
        custom_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "snap_tolerance": 3,
            "snap_x_tolerance": 3,
            "snap_y_tolerance": 3,
            "join_tolerance": 3,
            "join_x_tolerance": 3,
            "join_y_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 1,
            "min_words_horizontal": 1,
            "keep_blank_chars": False,
            "text_tolerance": 3,
            "text_x_tolerance": 3,
            "text_y_tolerance": 3,
            "intersection_tolerance": 3,
            "intersection_x_tolerance": 3,
            "intersection_y_tolerance": 3,
        }
        
        # Try to find tables
        try:
            # First attempt with line detection
            tables = page.find_tables(table_settings=custom_settings)
            
            for table in tables:
                if table:
                    extracted_data = table.extract()
                    if extracted_data and self._validate_table_structure(extracted_data):
                        cleaned = self._advanced_table_cleaning(extracted_data)
                        if cleaned:
                            extracted_tables.append({
                                'data': cleaned,
                                'bbox': table.bbox if hasattr(table, 'bbox') else None
                            })
        except Exception as e:
            logger.debug(f"Table extraction with lines failed: {e}")
        
        # Method 2: Fallback to text-based extraction
        if not extracted_tables:
            text_settings = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "snap_tolerance": 3,
                "join_tolerance": 3,
                "edge_min_length": 3,
                "min_words_vertical": 3,
                "min_words_horizontal": 1,
            }
            
            try:
                tables = page.extract_tables(text_settings)
                for table in tables:
                    if table and self._validate_table_structure(table):
                        cleaned = self._advanced_table_cleaning(table)
                        if cleaned:
                            extracted_tables.append({
                                'data': cleaned,
                                'bbox': None
                            })
            except Exception as e:
                logger.debug(f"Text-based table extraction failed: {e}")
        
        return extracted_tables
    
    def _validate_table_structure(self, table: List[List]) -> bool:
        """Validate that extracted data is actually a table"""
        if not table or len(table) < 2:
            return False
        
        # Remove completely empty rows
        non_empty_rows = [row for row in table if any(cell for cell in row if cell)]
        if len(non_empty_rows) < 2:
            return False
        
        # Check column consistency
        col_counts = [len(row) for row in non_empty_rows]
        if not col_counts:
            return False
        
        # Must have at least 2 columns
        if max(col_counts) < 2:
            return False
        
        # Check if it's structured data (not just random text)
        # Count cells with numeric content
        numeric_cells = 0
        total_cells = 0
        
        for row in non_empty_rows:
            for cell in row:
                if cell:
                    total_cells += 1
                    if self._contains_number(str(cell)):
                        numeric_cells += 1
        
        # If more than 20% of cells contain numbers, likely a table
        if total_cells > 0 and numeric_cells / total_cells > 0.2:
            return True
        
        # Check for table-like headers
        if non_empty_rows[0]:
            first_row_text = ' '.join(str(cell) for cell in non_empty_rows[0] if cell)
            table_keywords = ['total', 'amount', 'date', 'revenue', 'cost', 'profit', 
                            'asset', 'liability', 'equity', 'cash', 'balance']
            if any(keyword in first_row_text.lower() for keyword in table_keywords):
                return True
        
        return False
    
    def _contains_number(self, text: str) -> bool:
        """Check if text contains numeric values"""
        # Remove common separators
        cleaned = text.replace(',', '').replace('£', '').replace('$', '').replace('€', '')
        # Check for digits
        return bool(re.search(r'\d', cleaned))
    
    def _advanced_table_cleaning(self, table: List[List]) -> List[List]:
        """Advanced table cleaning with intelligent cell merging"""
        if not table:
            return []
        
        # Step 1: Remove completely empty rows
        non_empty = []
        for row in table:
            if row and any(cell for cell in row if cell):
                non_empty.append(row)
        
        if not non_empty:
            return []
        
        # Step 2: Intelligent column reconstruction
        reconstructed = self._reconstruct_columns(non_empty)
        
        # Step 3: Merge split headers
        with_merged_headers = self._merge_split_headers(reconstructed)
        
        # Step 4: Final cleaning
        final_cleaned = []
        for row in with_merged_headers:
            cleaned_row = []
            for cell in row:
                if cell is None:
                    cleaned_row.append('')
                else:
                    # Clean cell content
                    cell_str = str(cell).strip()
                    # Remove internal line breaks
                    cell_str = re.sub(r'\n+', ' ', cell_str)
                    # Remove excessive spaces
                    cell_str = re.sub(r'\s+', ' ', cell_str)
                    cleaned_row.append(cell_str)
            final_cleaned.append(cleaned_row)
        
        # Step 5: Ensure consistent column count
        if final_cleaned:
            max_cols = max(len(row) for row in final_cleaned)
            normalized = []
            for row in final_cleaned:
                normalized_row = list(row)
                while len(normalized_row) < max_cols:
                    normalized_row.append('')
                normalized.append(normalized_row[:max_cols])
            return normalized
        
        return final_cleaned
    
    def _reconstruct_columns(self, table: List[List]) -> List[List]:
        """Reconstruct table columns by analyzing cell positions"""
        if not table:
            return []
        
        # Find the row with most non-None values (likely the most complete)
        max_cols = 0
        reference_row_idx = 0
        for i, row in enumerate(table):
            non_none_count = sum(1 for cell in row if cell is not None and str(cell).strip())
            if non_none_count > max_cols:
                max_cols = non_none_count
                reference_row_idx = i
        
        if max_cols == 0:
            return table
        
        # Use the reference row to determine column positions
        reference_row = table[reference_row_idx]
        column_positions = []
        for i, cell in enumerate(reference_row):
            if cell is not None and str(cell).strip():
                column_positions.append(i)
        
        # Reconstruct all rows based on these positions
        reconstructed = []
        for row in table:
            new_row = []
            for pos in column_positions:
                if pos < len(row):
                    # Check if we should merge with adjacent cells
                    cell_value = row[pos]
                    
                    # If current cell is None, try adjacent cells
                    if cell_value is None:
                        # Try previous cell
                        if pos > 0 and row[pos-1] is not None:
                            cell_value = row[pos-1]
                        # Try next cell
                        elif pos < len(row) - 1 and row[pos+1] is not None:
                            cell_value = row[pos+1]
                    
                    new_row.append(cell_value)
                else:
                    new_row.append(None)
            reconstructed.append(new_row)
        
        return reconstructed
    
    def _merge_split_headers(self, table: List[List]) -> List[List]:
        """Merge headers that have been split across multiple rows"""
        if len(table) < 2:
            return table
        
        # Detect if first rows are split headers
        first_row = table[0]
        second_row = table[1] if len(table) > 1 else []
        
        # Count None values in first rows
        first_none_ratio = sum(1 for cell in first_row if cell is None) / len(first_row) if first_row else 0
        second_none_ratio = sum(1 for cell in second_row if cell is None) / len(second_row) if second_row else 0
        
        # If both rows have many None values, they might be split headers
        if first_none_ratio > 0.3 and second_none_ratio > 0.3:
            # Merge first two rows
            merged_header = []
            max_len = max(len(first_row), len(second_row) if second_row else 0)
            
            for i in range(max_len):
                parts = []
                
                if i < len(first_row) and first_row[i] is not None:
                    parts.append(str(first_row[i]).strip())
                
                if second_row and i < len(second_row) and second_row[i] is not None:
                    second_val = str(second_row[i]).strip()
                    if second_val and second_val not in parts:
                        parts.append(second_val)
                
                merged_value = ' '.join(parts) if parts else ''
                merged_header.append(merged_value)
            
            # Return merged table
            return [merged_header] + table[2:]
        
        return table
    
    def _integrate_tables_and_text(self, full_text: str, tables: List[Dict], page) -> str:
        """Integrate tables with surrounding text in correct positions"""
        content_parts = []
        text_lines = full_text.split('\n')
        
        # Mark lines that belong to tables
        table_line_indices = set()
        
        for table_info in tables:
            table_data = table_info['data']
            
            # Find where table content appears in text
            for row in table_data:
                for cell in row:
                    if cell:
                        cell_text = str(cell).strip()
                        if len(cell_text) > 3:  # Skip very short strings
                            for i, line in enumerate(text_lines):
                                if cell_text in line:
                                    table_line_indices.add(i)
        
        # Build content with tables inserted at appropriate positions
        current_text = []
        table_inserted = {i: False for i in range(len(tables))}
        
        for i, line in enumerate(text_lines):
            if i in table_line_indices:
                # This line is part of a table
                # Add any accumulated text
                if current_text:
                    text_content = self._enhance_text_formatting('\n'.join(current_text))
                    if text_content.strip():
                        content_parts.append(text_content)
                    current_text = []
                
                # Find and insert the appropriate table
                for j, table_info in enumerate(tables):
                    if not table_inserted[j]:
                        # Check if this table contains content from this line
                        table_data = table_info['data']
                        for row in table_data:
                            if any(str(cell) in line for cell in row if cell):
                                # Insert this table
                                md_table = self._create_perfect_markdown_table(table_data)
                                if md_table:
                                    content_parts.append('\n' + md_table + '\n')
                                table_inserted[j] = True
                                break
            else:
                # Regular text line
                current_text.append(line)
        
        # Add any remaining text
        if current_text:
            text_content = self._enhance_text_formatting('\n'.join(current_text))
            if text_content.strip():
                content_parts.append(text_content)
        
        # Add any tables that weren't inserted (fallback)
        for j, table_info in enumerate(tables):
            if not table_inserted[j]:
                md_table = self._create_perfect_markdown_table(table_info['data'])
                if md_table:
                    content_parts.append('\n' + md_table + '\n')
        
        return '\n\n'.join(content_parts)
    
    def _create_perfect_markdown_table(self, table: List[List]) -> str:
        """Create a perfectly formatted markdown table"""
        if not table or len(table) < 2:
            return ""
        
        # Ensure all rows have same column count
        max_cols = max(len(row) for row in table)
        normalized = []
        
        for row in table:
            norm_row = list(row)
            while len(norm_row) < max_cols:
                norm_row.append('')
            normalized.append(norm_row[:max_cols])
        
        # Build markdown table
        lines = []
        
        # Header row
        headers = [str(cell) if cell else '' for cell in normalized[0]]
        lines.append('| ' + ' | '.join(headers) + ' |')
        
        # Separator with alignment
        separators = []
        for col_idx in range(max_cols):
            # Check if column contains numbers
            is_numeric = False
            for row_idx in range(1, len(normalized)):
                if col_idx < len(normalized[row_idx]):
                    cell = normalized[row_idx][col_idx]
                    if cell and self._is_financial_value(str(cell)):
                        is_numeric = True
                        break
            
            separators.append('---:' if is_numeric else '---')
        
        lines.append('| ' + ' | '.join(separators) + ' |')
        
        # Data rows
        for row in normalized[1:]:
            row_data = [str(cell) if cell else '' for cell in row]
            lines.append('| ' + ' | '.join(row_data) + ' |')
        
        return '\n'.join(lines)
    
    def _is_financial_value(self, value: str) -> bool:
        """Check if value is financial/numeric"""
        if not value:
            return False
        
        # Remove formatting
        cleaned = value.replace(',', '').replace('£', '').replace('$', '').replace('€', '')
        cleaned = cleaned.replace('(', '-').replace(')', '').replace('%', '')
        
        # Check if numeric
        try:
            float(cleaned)
            return True
        except ValueError:
            # Check for special values
            return cleaned in ['-', '–', 'n/a', 'N/A']
    
    def _enhance_text_formatting(self, text: str) -> str:
        """Enhance text formatting with better structure detection"""
        if not text:
            return ""
        
        lines = text.split('\n')
        formatted = []
        current_para = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_para:
                    formatted.append(' '.join(current_para))
                    current_para = []
                continue
            
            # Detect headers
            if self._is_section_header(line):
                if current_para:
                    formatted.append(' '.join(current_para))
                    current_para = []
                
                # Format as header
                if line.isupper() and len(line) < 50:
                    formatted.append(f"\n## {line.title()}\n")
                else:
                    formatted.append(f"\n### {line}\n")
            else:
                current_para.append(line)
        
        if current_para:
            formatted.append(' '.join(current_para))
        
        return '\n\n'.join(formatted)
    
    def _is_section_header(self, line: str) -> bool:
        """Detect section headers"""
        if not line or len(line) < 3:
            return False
        
        # All caps and reasonable length
        if line.isupper() and 3 < len(line) < 60:
            return True
        
        # Starts with common header words
        header_starts = [
            'Overview', 'Summary', 'Introduction', 'Background',
            'Financial', 'Consolidated', 'Notes', 'Balance Sheet',
            'Income Statement', 'Cash Flow', 'Statement of'
        ]
        
        for start in header_starts:
            if line.startswith(start):
                return True
        
        return False


def convert_pdf_file_advanced(pdf_path: Path, output_path: Path = None) -> Path:
    """
    Convert a PDF file to Markdown with advanced table extraction
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output markdown file
        
    Returns:
        Path to the created markdown file
    """
    converter = AdvancedPDFToMarkdownConverter()
    
    # Generate output path if not provided
    if output_path is None:
        output_path = pdf_path.parent / f"{pdf_path.stem}_advanced.md"
    
    # Convert PDF to Markdown
    markdown_content = converter.convert_pdf_to_markdown(pdf_path)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    logger.info(f"Converted {pdf_path} to {output_path}")
    return output_path