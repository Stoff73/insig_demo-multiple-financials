import pymupdf  # PyMuPDF
import pdfplumber
from pathlib import Path
import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FinalPDFToMarkdownConverter:
    """Final PDF to Markdown converter with best-in-class table extraction"""
    
    def __init__(self):
        self.page_break = "\n\n---\n\n"
        
    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """
        Convert a PDF file to Markdown format using PyMuPDF for better accuracy
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Markdown formatted string
        """
        markdown_content = []
        
        try:
            # Use PyMuPDF for better text and table extraction
            doc = pymupdf.open(str(pdf_path))
            
            # Add document title
            markdown_content.append(f"# {pdf_path.stem}\n\n")
            
            # Process each page
            for page_num, page in enumerate(doc, 1):
                page_content = self._process_page_pymupdf(page, page_num, pdf_path)
                if page_content:
                    markdown_content.append(page_content)
                    
                    # Add page break between pages (except last)
                    if page_num < len(doc):
                        markdown_content.append(self.page_break)
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Error converting PDF with PyMuPDF: {str(e)}")
            # Fallback to pdfplumber
            return self._convert_with_pdfplumber(pdf_path)
            
        return "\n".join(markdown_content)
    
    def _process_page_pymupdf(self, page, page_num: int, pdf_path: Path) -> str:
        """Process a single PDF page using PyMuPDF"""
        page_content = []
        
        # Add page number as comment
        page_content.append(f"<!-- Page {page_num} -->\n")
        
        # Try to extract tables using PyMuPDF's table detection
        tables = self._extract_tables_pymupdf(page)
        
        # Get full text
        full_text = page.get_text()
        
        if tables:
            # Process with tables
            content = self._process_mixed_content_pymupdf(full_text, tables)
            page_content.append(content)
        else:
            # Fallback to pdfplumber for this page if no tables found
            content = self._process_page_with_pdfplumber(pdf_path, page_num - 1)
            if content:
                page_content.append(content)
            else:
                # Just use the text
                processed_text = self._format_text(full_text)
                page_content.append(processed_text)
        
        return "\n".join(page_content)
    
    def _extract_tables_pymupdf(self, page) -> List[Dict]:
        """Extract tables using PyMuPDF's table detection"""
        extracted_tables = []
        
        try:
            # Find tables on the page
            tabs = page.find_tables()
            
            if tabs and tabs.tables:
                for table in tabs.tables:
                    # Extract table data
                    table_data = table.extract()
                    
                    if table_data and self._is_valid_table(table_data):
                        # Clean the table
                        cleaned = self._clean_table_data(table_data)
                        if cleaned:
                            extracted_tables.append({
                                'data': cleaned,
                                'bbox': table.bbox if hasattr(table, 'bbox') else None
                            })
        except Exception as e:
            logger.debug(f"PyMuPDF table extraction failed: {e}")
        
        return extracted_tables
    
    def _process_page_with_pdfplumber(self, pdf_path: Path, page_num: int) -> str:
        """Fallback to pdfplumber for a specific page"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    
                    # Try different table extraction settings
                    tables = self._extract_tables_pdfplumber(page)
                    text = page.extract_text() or ""
                    
                    if tables:
                        return self._process_mixed_content_pdfplumber(text, tables)
                    else:
                        return self._format_text(text)
        except Exception as e:
            logger.debug(f"Pdfplumber fallback failed: {e}")
        
        return ""
    
    def _extract_tables_pdfplumber(self, page) -> List[Dict]:
        """Extract tables using pdfplumber with optimized settings"""
        extracted_tables = []
        
        # Optimized settings for financial tables
        settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": [],
            "explicit_horizontal_lines": [],
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
        
        try:
            tables = page.extract_tables(settings)
            
            for table in tables:
                if table and self._is_valid_table(table):
                    cleaned = self._clean_table_data(table)
                    if cleaned:
                        extracted_tables.append({'data': cleaned})
        except Exception as e:
            logger.debug(f"Pdfplumber table extraction failed: {e}")
        
        return extracted_tables
    
    def _is_valid_table(self, table: List[List]) -> bool:
        """Validate that the extracted data is a proper table"""
        if not table or len(table) < 2:
            return False
        
        # Check for reasonable structure
        non_empty_rows = []
        for row in table:
            if row and any(str(cell).strip() if cell else False for cell in row):
                non_empty_rows.append(row)
        
        if len(non_empty_rows) < 2:
            return False
        
        # Must have at least 2 columns
        max_cols = max(len(row) for row in non_empty_rows)
        if max_cols < 2:
            return False
        
        return True
    
    def _clean_table_data(self, table: List[List]) -> List[List]:
        """Clean and normalize table data"""
        if not table:
            return []
        
        cleaned = []
        
        # Process each row
        for row in table:
            if not row:
                continue
            
            cleaned_row = []
            for cell in row:
                if cell is None:
                    cleaned_row.append('')
                else:
                    # Clean cell content
                    cell_str = str(cell).strip()
                    # Remove internal newlines
                    cell_str = re.sub(r'\n+', ' ', cell_str)
                    # Remove excessive spaces
                    cell_str = re.sub(r'\s+', ' ', cell_str)
                    cleaned_row.append(cell_str)
            
            # Only add non-empty rows
            if any(cell for cell in cleaned_row):
                cleaned.append(cleaned_row)
        
        # Ensure consistent column count
        if cleaned:
            max_cols = max(len(row) for row in cleaned)
            normalized = []
            
            for row in cleaned:
                norm_row = list(row)
                while len(norm_row) < max_cols:
                    norm_row.append('')
                normalized.append(norm_row[:max_cols])
            
            return normalized
        
        return cleaned
    
    def _process_mixed_content_pymupdf(self, text: str, tables: List[Dict]) -> str:
        """Process content with both text and tables from PyMuPDF"""
        content_parts = []
        
        # Add tables first (PyMuPDF doesn't give us position info easily)
        for table_info in tables:
            md_table = self._create_markdown_table(table_info['data'])
            if md_table:
                content_parts.append(md_table)
        
        # Then add text (filtering out table content if possible)
        if text:
            # Try to filter out table content from text
            filtered_text = self._filter_table_content_from_text(text, tables)
            formatted = self._format_text(filtered_text)
            if formatted.strip():
                content_parts.append(formatted)
        
        return '\n\n'.join(content_parts)
    
    def _process_mixed_content_pdfplumber(self, text: str, tables: List[Dict]) -> str:
        """Process content with both text and tables from pdfplumber"""
        content_parts = []
        
        # Similar to PyMuPDF processing
        for table_info in tables:
            md_table = self._create_markdown_table(table_info['data'])
            if md_table:
                content_parts.append(md_table)
        
        if text:
            filtered_text = self._filter_table_content_from_text(text, tables)
            formatted = self._format_text(filtered_text)
            if formatted.strip():
                content_parts.append(formatted)
        
        return '\n\n'.join(content_parts)
    
    def _filter_table_content_from_text(self, text: str, tables: List[Dict]) -> str:
        """Remove table content from text to avoid duplication"""
        if not tables:
            return text
        
        filtered_lines = []
        text_lines = text.split('\n')
        
        for line in text_lines:
            is_table_content = False
            
            # Check if this line contains table data
            for table_info in tables:
                table_data = table_info['data']
                for row in table_data:
                    # If multiple cells from this row appear in the line, it's likely table content
                    cells_in_line = sum(1 for cell in row if cell and str(cell) in line)
                    if cells_in_line >= 2:
                        is_table_content = True
                        break
                
                if is_table_content:
                    break
            
            if not is_table_content:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _create_markdown_table(self, table: List[List]) -> str:
        """Create a properly formatted markdown table"""
        if not table or len(table) < 2:
            return ""
        
        lines = []
        
        # Header row
        headers = table[0]
        header_line = '| ' + ' | '.join(str(h) if h else '' for h in headers) + ' |'
        lines.append(header_line)
        
        # Separator row with alignment
        separators = []
        for col_idx, header in enumerate(headers):
            # Check if column contains numbers
            is_numeric = False
            for row in table[1:]:
                if col_idx < len(row) and row[col_idx]:
                    if self._is_numeric_cell(str(row[col_idx])):
                        is_numeric = True
                        break
            
            separators.append('---:' if is_numeric else '---')
        
        separator_line = '| ' + ' | '.join(separators) + ' |'
        lines.append(separator_line)
        
        # Data rows
        for row in table[1:]:
            # Ensure row has correct number of columns
            while len(row) < len(headers):
                row.append('')
            row = row[:len(headers)]
            
            data_line = '| ' + ' | '.join(str(cell) if cell else '' for cell in row) + ' |'
            lines.append(data_line)
        
        return '\n'.join(lines)
    
    def _is_numeric_cell(self, value: str) -> bool:
        """Check if a cell contains numeric data"""
        if not value:
            return False
        
        # Remove formatting
        cleaned = value.replace(',', '').replace('£', '').replace('$', '').replace('€', '')
        cleaned = cleaned.replace('(', '-').replace(')', '').replace('%', '')
        cleaned = cleaned.strip()
        
        # Check if numeric
        try:
            float(cleaned)
            return True
        except ValueError:
            return cleaned in ['-', '–', 'n/a', 'N/A', '']
    
    def _format_text(self, text: str) -> str:
        """Format text with proper structure"""
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
            if self._is_header(line):
                if current_para:
                    formatted.append(' '.join(current_para))
                    current_para = []
                
                if line.isupper() and len(line) < 50:
                    formatted.append(f"\n## {line.title()}\n")
                else:
                    formatted.append(f"\n### {line}\n")
            else:
                current_para.append(line)
        
        if current_para:
            formatted.append(' '.join(current_para))
        
        return '\n\n'.join(formatted)
    
    def _is_header(self, line: str) -> bool:
        """Check if a line is a header"""
        if not line or len(line) < 3:
            return False
        
        # All caps and reasonable length
        if line.isupper() and 3 < len(line) < 60:
            return True
        
        # Common header patterns
        header_keywords = [
            'Overview', 'Summary', 'Financial', 'Statement',
            'Balance Sheet', 'Income', 'Cash Flow', 'Notes'
        ]
        
        for keyword in header_keywords:
            if line.startswith(keyword):
                return True
        
        return False
    
    def _convert_with_pdfplumber(self, pdf_path: Path) -> str:
        """Fallback conversion using pdfplumber"""
        markdown_content = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                markdown_content.append(f"# {pdf_path.stem}\n\n")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_content = []
                    page_content.append(f"<!-- Page {page_num} -->\n")
                    
                    # Extract tables
                    tables = self._extract_tables_pdfplumber(page)
                    
                    # Extract text
                    text = page.extract_text() or ""
                    
                    if tables:
                        content = self._process_mixed_content_pdfplumber(text, tables)
                        page_content.append(content)
                    elif text:
                        page_content.append(self._format_text(text))
                    
                    if page_content:
                        markdown_content.append("\n".join(page_content))
                        if page_num < len(pdf.pages):
                            markdown_content.append(self.page_break)
        except Exception as e:
            logger.error(f"Pdfplumber fallback also failed: {str(e)}")
            raise
        
        return "\n".join(markdown_content)


def convert_pdf_file_final(pdf_path: Path, output_path: Path = None) -> Path:
    """
    Convert a PDF file to Markdown with the best available method
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output markdown file
        
    Returns:
        Path to the created markdown file
    """
    converter = FinalPDFToMarkdownConverter()
    
    # Generate output path if not provided
    if output_path is None:
        output_path = pdf_path.parent / f"{pdf_path.stem}_converted.md"
    
    # Convert PDF to Markdown
    markdown_content = converter.convert_pdf_to_markdown(pdf_path)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    logger.info(f"Converted {pdf_path} to {output_path}")
    return output_path