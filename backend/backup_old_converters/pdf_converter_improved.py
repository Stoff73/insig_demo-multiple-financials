import pdfplumber
from pathlib import Path
import re
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ImprovedPDFToMarkdownConverter:
    """Enhanced PDF to Markdown converter with improved table extraction"""
    
    def __init__(self):
        self.page_break = "\n\n---\n\n"
        
    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """
        Convert a PDF file to Markdown format with improved table handling
        
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
                    page_content = self._process_page(page, page_num)
                    if page_content:
                        markdown_content.append(page_content)
                        
                        # Add page break between pages (except last)
                        if page_num < len(pdf.pages):
                            markdown_content.append(self.page_break)
                            
        except Exception as e:
            logger.error(f"Error converting PDF: {str(e)}")
            raise
            
        return "\n".join(markdown_content)
    
    def _process_page(self, page, page_num: int) -> str:
        """Process a single PDF page with improved table extraction"""
        page_content = []
        
        # Add page number as comment
        page_content.append(f"<!-- Page {page_num} -->\n")
        
        # Try different table extraction strategies
        tables = self._extract_tables_smart(page)
        
        # Get full text first
        full_text = page.extract_text() or ""
        
        if tables:
            # Process mixed content (text and tables)
            content = self._process_mixed_content(full_text, tables, page)
            page_content.append(content)
        elif full_text:
            # No tables, just process text
            processed_text = self._process_text_content(full_text)
            page_content.append(processed_text)
        
        return "\n".join(page_content)
    
    def _extract_tables_smart(self, page) -> List[Dict]:
        """
        Smart table extraction with multiple strategies
        Returns list of dictionaries with table data and position info
        """
        extracted_tables = []
        
        # Strategy 1: Try with explicit lines (best for bordered tables)
        table_settings_lines = {
            'vertical_strategy': 'lines',
            'horizontal_strategy': 'lines',
            'snap_tolerance': 3,
            'join_tolerance': 3,
            'edge_min_length': 3,
            'min_words_vertical': 1,
            'min_words_horizontal': 1,
        }
        
        tables_lines = page.extract_tables(table_settings_lines)
        
        # Strategy 2: Try with text positioning (for tables without borders)
        table_settings_text = {
            'vertical_strategy': 'text',
            'horizontal_strategy': 'text',
            'snap_x_tolerance': 3,
            'snap_y_tolerance': 3,
            'join_x_tolerance': 3,
            'join_y_tolerance': 3,
            'edge_min_length': 3,
            'min_words_vertical': 3,
            'min_words_horizontal': 1,
            'text_tolerance': 3,
            'text_x_tolerance': 3,
            'text_y_tolerance': 3,
        }
        
        tables_text = page.extract_tables(table_settings_text)
        
        # Use the strategy that found more/better tables
        tables = tables_lines if tables_lines else tables_text
        
        # Process and clean tables
        for table in tables:
            if table and self._is_valid_table(table):
                cleaned_table = self._deep_clean_table(table)
                if cleaned_table:
                    extracted_tables.append({
                        'data': cleaned_table,
                        'type': 'financial' if self._is_financial_table(cleaned_table) else 'general'
                    })
        
        return extracted_tables
    
    def _is_valid_table(self, table: List[List]) -> bool:
        """Check if extracted data is actually a valid table"""
        if not table or len(table) < 2:
            return False
        
        # Check if table has consistent column count
        col_counts = [len(row) for row in table if row]
        if not col_counts:
            return False
            
        # Allow some variation in column count but not too much
        max_cols = max(col_counts)
        min_cols = min(col_counts)
        
        # Table should have at least 2 columns and rows
        if max_cols < 2 or len(table) < 2:
            return False
            
        # Most rows should have similar column count
        most_common_count = max(set(col_counts), key=col_counts.count)
        if col_counts.count(most_common_count) < len(col_counts) * 0.5:
            return False
            
        return True
    
    def _deep_clean_table(self, table: List[List]) -> List[List]:
        """Deep clean table data with column merging and alignment"""
        if not table:
            return []
        
        # First, handle multi-row headers by merging them
        table = self._merge_multirow_headers(table)
        
        cleaned = []
        
        # First pass: merge split cells and remove None values
        for row_idx, row in enumerate(table):
            if not row:
                continue
                
            cleaned_row = []
            i = 0
            while i < len(row):
                cell = row[i]
                
                # Merge consecutive None values with next non-None value
                if cell is None:
                    # Look for next non-None value
                    j = i + 1
                    while j < len(row) and row[j] is None:
                        j += 1
                    
                    if j < len(row) and row[j]:
                        # Skip the None values
                        i = j
                        cell = row[j]
                    else:
                        i += 1
                        continue
                
                # Clean the cell content
                cell_str = str(cell).strip() if cell else ""
                
                # Merge cells that appear to be split (e.g., currency values)
                if i + 1 < len(row) and self._should_merge_cells(cell_str, row[i + 1]):
                    next_cell = str(row[i + 1]).strip() if row[i + 1] else ""
                    cell_str = f"{cell_str} {next_cell}".strip()
                    i += 1  # Skip the merged cell
                
                if cell_str:
                    cleaned_row.append(self._clean_cell_value(cell_str))
                    
                i += 1
            
            if cleaned_row:
                cleaned.append(cleaned_row)
        
        # Second pass: ensure consistent column count
        if cleaned:
            # Find the most common column count (likely the correct one)
            col_counts = [len(row) for row in cleaned]
            target_cols = max(set(col_counts), key=col_counts.count)
            
            # Adjust all rows to have the same column count
            normalized = []
            for row in cleaned:
                if len(row) < target_cols:
                    # Pad with empty strings
                    row.extend([''] * (target_cols - len(row)))
                elif len(row) > target_cols:
                    # Truncate or merge excess columns
                    row = row[:target_cols]
                normalized.append(row)
            
            return normalized
        
        return []
    
    def _merge_multirow_headers(self, table: List[List]) -> List[List]:
        """Merge multi-row headers into single row"""
        if len(table) < 2:
            return table
        
        # Check if first few rows look like split headers
        # (many empty cells, similar patterns)
        potential_header_rows = []
        for i, row in enumerate(table[:3]):  # Check first 3 rows
            if row:
                # Count non-empty cells
                non_empty = sum(1 for cell in row if cell and str(cell).strip())
                # If row has many empty cells, might be split header
                if non_empty < len(row) * 0.7:
                    potential_header_rows.append(i)
        
        # If we have potential split headers, merge them
        if len(potential_header_rows) >= 2:
            # Merge the header rows column by column
            merged_header = []
            max_cols = max(len(table[i]) if i < len(table) else 0 for i in potential_header_rows)
            
            for col_idx in range(max_cols):
                # Collect all values for this column from header rows
                col_values = []
                for row_idx in potential_header_rows:
                    if row_idx < len(table) and col_idx < len(table[row_idx]):
                        cell = table[row_idx][col_idx]
                        if cell and str(cell).strip():
                            col_values.append(str(cell).strip())
                
                # Merge column values
                if col_values:
                    # Join with space, removing duplicates
                    merged_value = ' '.join(dict.fromkeys(col_values))
                    merged_header.append(merged_value)
                else:
                    merged_header.append('')
            
            # Replace the split headers with merged version
            new_table = [merged_header]
            # Add remaining rows (skip the merged header rows)
            skip_until = max(potential_header_rows) + 1
            new_table.extend(table[skip_until:])
            
            return new_table
        
        return table
    
    def _should_merge_cells(self, cell1: str, cell2: Any) -> bool:
        """Determine if two adjacent cells should be merged"""
        if not cell2:
            return False
            
        cell2_str = str(cell2).strip()
        
        # Merge if second cell looks like continuation
        # E.g., "Revenue" + "change %"
        if cell1 and not any(char.isdigit() for char in cell1) and "%" in cell2_str:
            return True
        
        # Merge if split number (e.g., "30 June" + "2024")
        if cell1 and cell1[-1].isalpha() and cell2_str and cell2_str[0].isdigit():
            return True
            
        return False
    
    def _clean_cell_value(self, value: str) -> str:
        """Clean individual cell value"""
        # Remove excessive whitespace
        value = re.sub(r'\s+', ' ', value)
        
        # Remove line breaks within cells
        value = value.replace('\n', ' ')
        
        # Clean up financial formatting
        value = self._format_financial_value(value)
        
        return value.strip()
    
    def _format_financial_value(self, value: str) -> str:
        """Format financial values consistently"""
        # Keep negative values in parentheses
        if '(' in value and ')' in value:
            return value
        
        # Ensure proper formatting for percentages
        if '%' in value:
            # Ensure space before % is removed for consistency
            value = re.sub(r'\s+%', '%', value)
        
        return value
    
    def _is_financial_table(self, table: List[List]) -> bool:
        """Check if table contains financial data"""
        if not table:
            return False
            
        # Check for financial keywords in headers
        financial_keywords = [
            'revenue', 'profit', 'loss', 'asset', 'liability', 
            'equity', 'cash', 'cost', 'expense', 'income',
            'margin', 'ebitda', 'depreciation', '£', '$', '€',
            'million', 'thousand', '%'
        ]
        
        # Check first two rows (likely headers)
        for row in table[:2]:
            row_text = ' '.join(str(cell).lower() for cell in row if cell)
            if any(keyword in row_text for keyword in financial_keywords):
                return True
                
        return False
    
    def _process_mixed_content(self, full_text: str, tables: List[Dict], page) -> str:
        """Process page with both text and tables, maintaining proper order"""
        content_parts = []
        
        # Split text into lines
        text_lines = full_text.split('\n')
        
        # Track which lines have been used in tables
        table_text_ranges = []
        for table_info in tables:
            table = table_info['data']
            # Find where this table appears in the text
            table_start_line = None
            table_end_line = None
            
            # Look for table content in text
            for row in table:
                for cell in row:
                    if cell:
                        cell_text = str(cell).strip()
                        for i, line in enumerate(text_lines):
                            if cell_text in line:
                                if table_start_line is None or i < table_start_line:
                                    table_start_line = i
                                if table_end_line is None or i > table_end_line:
                                    table_end_line = i
            
            if table_start_line is not None and table_end_line is not None:
                table_text_ranges.append((table_start_line, table_end_line, table_info))
        
        # Sort tables by their position in text
        table_text_ranges.sort(key=lambda x: x[0])
        
        # Process content in order
        current_line = 0
        for start, end, table_info in table_text_ranges:
            # Add text before table
            if current_line < start:
                text_before = '\n'.join(text_lines[current_line:start])
                processed = self._process_text_content(text_before)
                if processed.strip():
                    content_parts.append(processed)
            
            # Add table
            markdown_table = self._create_markdown_table(table_info['data'], table_info['type'])
            if markdown_table:
                content_parts.append('\n' + markdown_table + '\n')
            
            current_line = end + 1
        
        # Add remaining text after last table
        if current_line < len(text_lines):
            remaining_text = '\n'.join(text_lines[current_line:])
            processed = self._process_text_content(remaining_text)
            if processed.strip():
                content_parts.append(processed)
        
        return '\n\n'.join(content_parts)
    
    def _create_markdown_table(self, table: List[List], table_type: str = 'general') -> str:
        """Create properly formatted markdown table"""
        if not table or len(table) < 2:
            return ""
        
        # Ensure all rows have the same number of columns
        max_cols = max(len(row) for row in table)
        
        # Normalize all rows to have the same column count
        normalized_table = []
        for row in table:
            normalized_row = list(row)
            while len(normalized_row) < max_cols:
                normalized_row.append('')
            normalized_table.append(normalized_row[:max_cols])
        
        # First row is headers
        headers = normalized_table[0]
        
        # Build markdown table
        lines = []
        
        # Header row
        header_row = "| " + " | ".join(str(h) for h in headers) + " |"
        lines.append(header_row)
        
        # Separator row with alignment
        separator_parts = []
        for i, header in enumerate(headers):
            # Check if column is numeric by examining data rows
            is_numeric = False
            for row in normalized_table[1:]:
                if i < len(row) and row[i]:
                    if self._is_numeric_value(str(row[i])):
                        is_numeric = True
                        break
            
            if is_numeric:
                separator_parts.append("---:")  # Right align
            else:
                separator_parts.append("---")   # Left align
        
        separator = "| " + " | ".join(separator_parts) + " |"
        lines.append(separator)
        
        # Data rows
        for row in normalized_table[1:]:
            data_row = "| " + " | ".join(str(cell) for cell in row) + " |"
            lines.append(data_row)
        
        return "\n".join(lines)
    
    def _is_numeric_value(self, value: str) -> bool:
        """Check if a value is numeric (including financial formats)"""
        if not value:
            return False
        
        # Remove currency symbols and formatting
        cleaned = value.replace(',', '').replace('£', '').replace('$', '').replace('€', '')
        cleaned = cleaned.replace('(', '-').replace(')', '').strip()
        
        # Check for percentage
        if cleaned.endswith('%'):
            cleaned = cleaned[:-1].strip()
        
        # Check if it's a number
        try:
            float(cleaned)
            return True
        except ValueError:
            # Check for special cases like "n/a", "-", etc.
            if cleaned in ['-', 'n/a', 'N/A', '–']:
                return True
            return False
    
    def _process_text_content(self, text: str) -> str:
        """Process text content with improved formatting"""
        if not text:
            return ""
        
        lines = text.split('\n')
        processed_lines = []
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            if not line:
                # Empty line - end current paragraph
                if current_paragraph:
                    processed_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
                continue
            
            # Detect headers
            if self._is_header(line):
                # Save current paragraph
                if current_paragraph:
                    processed_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
                
                # Add header
                if line.isupper() and len(line) < 50:
                    processed_lines.append(f"\n## {line.title()}\n")
                else:
                    processed_lines.append(f"\n### {line}\n")
            else:
                # Add to current paragraph
                current_paragraph.append(line)
        
        # Add remaining paragraph
        if current_paragraph:
            processed_lines.append(' '.join(current_paragraph))
        
        return '\n\n'.join(processed_lines)
    
    def _is_header(self, line: str) -> bool:
        """Detect if a line is a header"""
        if len(line) < 3 or len(line) > 100:
            return False
        
        # All caps and short
        if line.isupper() and len(line) < 50:
            return True
        
        # Common header patterns
        header_patterns = [
            r'^[A-Z][^.!?]*:$',  # Ends with colon
            r'^\d+\.\s+[A-Z]',   # Numbered section
            r'^[A-Z][A-Z\s]+$',  # All caps words
        ]
        
        for pattern in header_patterns:
            if re.match(pattern, line):
                return True
        
        # Check for section keywords at start
        section_starts = [
            'Overview', 'Summary', 'Introduction', 'Conclusion',
            'Financial', 'Balance Sheet', 'Income Statement',
            'Cash Flow', 'Notes to', 'Consolidated'
        ]
        
        for start in section_starts:
            if line.startswith(start):
                return True
        
        return False


def convert_pdf_file_improved(pdf_path: Path, output_path: Path = None) -> Path:
    """
    Convert a PDF file to Markdown with improved table extraction
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output markdown file
        
    Returns:
        Path to the created markdown file
    """
    converter = ImprovedPDFToMarkdownConverter()
    
    # Generate output path if not provided
    if output_path is None:
        output_path = pdf_path.parent / f"{pdf_path.stem}_improved.md"
    
    # Convert PDF to Markdown
    markdown_content = converter.convert_pdf_to_markdown(pdf_path)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    logger.info(f"Converted {pdf_path} to {output_path}")
    return output_path