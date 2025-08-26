import pdfplumber
from pathlib import Path
import re
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class BestPDFToMarkdownConverter:
    """Optimized PDF to Markdown converter with smart table reconstruction"""
    
    def __init__(self):
        self.page_break = "\n\n---\n\n"
        
    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """Convert PDF to Markdown with intelligent table handling"""
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
        """Process a single page"""
        page_content = []
        
        # Add page number
        page_content.append(f"<!-- Page {page_num} -->\n")
        
        # Extract tables with optimal settings
        tables = page.extract_tables({
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "edge_min_length": 3,
        })
        
        # Extract text
        text = page.extract_text() or ""
        
        if tables:
            # Process tables and text together
            processed_content = self._integrate_content(text, tables)
            page_content.append(processed_content)
        elif text:
            # Just format text
            page_content.append(self._format_text(text))
        
        return "\n".join(page_content)
    
    def _integrate_content(self, text: str, tables: List) -> str:
        """Integrate tables with text"""
        content = []
        text_lines = text.split('\n')
        table_lines_used = set()
        
        # Process each table
        for table in tables:
            if not table or len(table) < 2:
                continue
            
            # Clean and reconstruct the table
            cleaned_table = self._reconstruct_table(table)
            
            if cleaned_table:
                # Find where this table appears in text
                for row in cleaned_table:
                    for cell in row:
                        if cell:
                            for i, line in enumerate(text_lines):
                                if str(cell) in line:
                                    table_lines_used.add(i)
                
                # Create markdown table
                md_table = self._create_markdown_table(cleaned_table)
                if md_table:
                    content.append(md_table)
        
        # Add non-table text
        text_content = []
        for i, line in enumerate(text_lines):
            if i not in table_lines_used:
                line = line.strip()
                if line:
                    text_content.append(line)
        
        if text_content:
            formatted_text = self._format_text('\n'.join(text_content))
            content.append(formatted_text)
        
        return '\n\n'.join(content)
    
    def _reconstruct_table(self, table: List[List]) -> List[List]:
        """Intelligently reconstruct table from split cells"""
        if not table:
            return []
        
        # Step 1: Merge split header rows
        merged_table = self._merge_header_rows(table)
        
        # Step 2: Clean each row
        cleaned = []
        for row in merged_table:
            cleaned_row = self._clean_row(row)
            if cleaned_row and any(cell for cell in cleaned_row):
                cleaned.append(cleaned_row)
        
        # Step 3: Normalize column count
        if cleaned:
            # Determine proper column count by analyzing the data
            col_count = self._determine_column_count(cleaned)
            
            normalized = []
            for row in cleaned:
                norm_row = self._normalize_row(row, col_count)
                normalized.append(norm_row)
            
            return normalized
        
        return cleaned
    
    def _merge_header_rows(self, table: List[List]) -> List[List]:
        """Merge split header rows intelligently"""
        if len(table) < 2:
            return table
        
        # Check if first rows look like split headers
        first_row = table[0] if table else []
        second_row = table[1] if len(table) > 1 else []
        third_row = table[2] if len(table) > 2 else []
        
        # Count None values to detect split headers
        def count_nones(row):
            return sum(1 for cell in row if cell is None)
        
        first_nones = count_nones(first_row)
        second_nones = count_nones(second_row)
        third_nones = count_nones(third_row) if third_row else 0
        
        # If many Nones, likely split headers
        if first_row and second_row:
            first_ratio = first_nones / len(first_row)
            second_ratio = second_nones / len(second_row)
            
            # Merge if both have > 40% None values
            if first_ratio > 0.4 and second_ratio > 0.4:
                # Intelligent merging
                merged_header = self._merge_rows_smart(first_row, second_row, third_row if third_nones > len(third_row) * 0.4 else None)
                
                if third_row and third_nones > len(third_row) * 0.4:
                    # Merged 3 rows
                    return [merged_header] + table[3:]
                else:
                    # Merged 2 rows
                    return [merged_header] + table[2:]
        
        return table
    
    def _merge_rows_smart(self, row1: List, row2: List, row3: Optional[List] = None) -> List:
        """Smart merging of split rows"""
        max_len = max(len(row1), len(row2), len(row3) if row3 else 0)
        merged = []
        
        for i in range(max_len):
            parts = []
            
            # Get values from each row
            val1 = row1[i] if i < len(row1) else None
            val2 = row2[i] if i < len(row2) else None
            val3 = row3[i] if row3 and i < len(row3) else None
            
            # Combine non-None values
            for val in [val1, val2, val3]:
                if val is not None and str(val).strip():
                    parts.append(str(val).strip())
            
            # Merge intelligently
            if parts:
                # Remove duplicates while preserving order
                seen = set()
                unique_parts = []
                for part in parts:
                    if part not in seen:
                        seen.add(part)
                        unique_parts.append(part)
                
                merged.append(' '.join(unique_parts))
            else:
                merged.append('')
        
        return merged
    
    def _clean_row(self, row: List) -> List:
        """Clean a single row"""
        cleaned = []
        
        i = 0
        while i < len(row):
            cell = row[i]
            
            # Skip None values
            if cell is None:
                # Check if we should use the next non-None value
                j = i + 1
                while j < len(row) and row[j] is None:
                    j += 1
                
                if j < len(row):
                    # Use the next non-None value
                    i = j
                    cell = row[j]
                else:
                    i += 1
                    continue
            
            # Clean the cell
            if cell is not None:
                cell_str = str(cell).strip()
                # Remove newlines
                cell_str = re.sub(r'\n+', ' ', cell_str)
                # Remove excessive spaces
                cell_str = re.sub(r'\s+', ' ', cell_str)
                
                cleaned.append(cell_str)
            
            i += 1
        
        return cleaned
    
    def _determine_column_count(self, table: List[List]) -> int:
        """Determine the proper column count for a table"""
        if not table:
            return 0
        
        # Look for the row with the most non-empty cells
        max_cells = 0
        for row in table:
            non_empty = sum(1 for cell in row if cell and str(cell).strip())
            max_cells = max(max_cells, non_empty)
        
        return max_cells
    
    def _normalize_row(self, row: List, target_cols: int) -> List:
        """Normalize row to have exact column count"""
        normalized = list(row)
        
        # Pad if too short
        while len(normalized) < target_cols:
            normalized.append('')
        
        # Truncate if too long
        return normalized[:target_cols]
    
    def _create_markdown_table(self, table: List[List]) -> str:
        """Create markdown table"""
        if not table or len(table) < 2:
            return ""
        
        lines = []
        
        # Header
        headers = table[0]
        lines.append('| ' + ' | '.join(str(h) for h in headers) + ' |')
        
        # Separator with alignment
        seps = []
        for i, header in enumerate(headers):
            # Check if numeric column
            is_numeric = False
            for row in table[1:]:
                if i < len(row) and row[i]:
                    if self._is_numeric(str(row[i])):
                        is_numeric = True
                        break
            
            seps.append('---:' if is_numeric else '---')
        
        lines.append('| ' + ' | '.join(seps) + ' |')
        
        # Data rows
        for row in table[1:]:
            lines.append('| ' + ' | '.join(str(cell) if cell else '' for cell in row) + ' |')
        
        return '\n'.join(lines)
    
    def _is_numeric(self, value: str) -> bool:
        """Check if value is numeric"""
        if not value:
            return False
        
        # Clean the value
        cleaned = value.replace(',', '').replace('£', '').replace('$', '')
        cleaned = cleaned.replace('(', '-').replace(')', '').replace('%', '')
        
        try:
            float(cleaned)
            return True
        except:
            return cleaned in ['-', '–', 'n/a']
    
    def _format_text(self, text: str) -> str:
        """Format text content"""
        if not text:
            return ""
        
        lines = text.split('\n')
        formatted = []
        para = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if para:
                    formatted.append(' '.join(para))
                    para = []
            elif line.isupper() and len(line) < 50:
                if para:
                    formatted.append(' '.join(para))
                    para = []
                formatted.append(f"\n## {line.title()}\n")
            else:
                para.append(line)
        
        if para:
            formatted.append(' '.join(para))
        
        return '\n\n'.join(formatted)


def convert_pdf_file_best(pdf_path: Path, output_path: Path = None) -> Path:
    """Convert PDF to Markdown with best quality"""
    converter = BestPDFToMarkdownConverter()
    
    if output_path is None:
        output_path = pdf_path.parent / f"{pdf_path.stem}_converted.md"
    
    markdown_content = converter.convert_pdf_to_markdown(pdf_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    logger.info(f"Converted {pdf_path} to {output_path}")
    return output_path