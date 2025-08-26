import pdfplumber
from tabulate import tabulate
from pathlib import Path
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PDFToMarkdownConverter:
    """Convert PDF documents to Markdown format with table preservation"""
    
    def __init__(self):
        self.page_break = "\n\n---\n\n"
        
    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """
        Convert a PDF file to Markdown format
        
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
        """Process a single PDF page"""
        page_content = []
        
        # Add page number as comment
        page_content.append(f"<!-- Page {page_num} -->\n")
        
        # Extract tables first
        tables = page.extract_tables()
        
        if tables:
            # Process tables
            for table_idx, table in enumerate(tables):
                cleaned_table = self._clean_table(table)
                if cleaned_table:
                    markdown_table = self._table_to_markdown(cleaned_table)
                    page_content.append(markdown_table)
                    page_content.append("")  # Add blank line after table
        
        # Extract text (excluding table areas)
        text = page.extract_text()
        
        if text:
            # Process text content
            processed_text = self._process_text(text, tables)
            if processed_text:
                page_content.append(processed_text)
        
        return "\n".join(page_content)
    
    def _clean_table(self, table: List[List]) -> List[List]:
        """Clean and filter table data"""
        if not table:
            return []
            
        # Remove empty rows and columns
        cleaned = []
        for row in table:
            if row and any(cell for cell in row if cell):
                # Clean each cell
                cleaned_row = [
                    self._clean_cell(cell) for cell in row
                ]
                cleaned.append(cleaned_row)
                
        return cleaned if len(cleaned) > 1 else []
    
    def _clean_cell(self, cell: Any) -> str:
        """Clean individual table cell"""
        if cell is None:
            return ""
            
        # Convert to string and clean
        cell_str = str(cell).strip()
        
        # Remove excessive whitespace
        cell_str = re.sub(r'\s+', ' ', cell_str)
        
        # Handle common financial formatting
        cell_str = self._format_financial_value(cell_str)
        
        return cell_str
    
    def _format_financial_value(self, value: str) -> str:
        """Format financial values for better readability"""
        # Keep negative values in parentheses
        if '(' in value and ')' in value:
            return value
            
        # Ensure proper decimal formatting
        if re.match(r'^-?\d+\.?\d*$', value.replace(',', '')):
            # It's a number, keep it as is
            return value
            
        return value
    
    def _table_to_markdown(self, table: List[List]) -> str:
        """Convert table data to Markdown table format"""
        if not table or len(table) < 2:
            return ""
            
        # Use the first row as headers
        headers = table[0]
        
        # Create the markdown table
        markdown_lines = []
        
        # Add headers
        header_row = "| " + " | ".join(headers) + " |"
        markdown_lines.append(header_row)
        
        # Add separator
        separator = "|"
        for header in headers:
            # Check if column contains numbers for right alignment
            is_numeric = False
            for row in table[1:]:
                idx = headers.index(header)
                if idx < len(row):
                    cell = row[idx]
                    if self._is_numeric_cell(cell):
                        is_numeric = True
                        break
            
            if is_numeric:
                separator += " ---: |"  # Right align for numbers
            else:
                separator += " --- |"   # Left align for text
                
        markdown_lines.append(separator)
        
        # Add data rows
        for row in table[1:]:
            # Ensure row has same number of columns as headers
            while len(row) < len(headers):
                row.append("")
            row = row[:len(headers)]  # Truncate if too many columns
            
            data_row = "| " + " | ".join(row) + " |"
            markdown_lines.append(data_row)
            
        return "\n".join(markdown_lines)
    
    def _is_numeric_cell(self, cell: str) -> bool:
        """Check if a cell contains numeric data"""
        if not cell:
            return False
            
        # Remove common formatting
        cleaned = cell.replace(',', '').replace('$', '').replace('£', '').replace('€', '')
        cleaned = cleaned.replace('(', '-').replace(')', '')
        
        # Check if it's a number
        try:
            float(cleaned)
            return True
        except ValueError:
            # Check for percentage
            if cleaned.endswith('%'):
                try:
                    float(cleaned[:-1])
                    return True
                except ValueError:
                    pass
        
        return False
    
    def _process_text(self, text: str, tables: List) -> str:
        """Process extracted text, format headers and paragraphs"""
        if not text:
            return ""
            
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip lines that are likely part of tables
            if tables and self._is_table_text(line, tables):
                continue
                
            # Detect and format headers
            if self._is_header(line):
                # Determine header level based on context
                if line.isupper() and len(line) < 50:
                    processed_lines.append(f"\n## {line.title()}\n")
                elif self._is_section_header(line):
                    processed_lines.append(f"\n### {line}\n")
                else:
                    processed_lines.append(line)
            else:
                # Regular paragraph text
                processed_lines.append(line)
                
        # Join lines into paragraphs
        text_content = self._form_paragraphs(processed_lines)
        
        return text_content
    
    def _is_table_text(self, line: str, tables: List) -> bool:
        """Check if a line is likely part of a table"""
        # Simple heuristic: if line contains multiple numbers separated by spaces
        # it might be table data
        numbers = re.findall(r'\d+\.?\d*', line)
        if len(numbers) > 3:
            return True
            
        # Check if line matches any table cell content
        for table in tables:
            for row in table:
                for cell in row:
                    if cell and str(cell).strip() in line:
                        return True
                        
        return False
    
    def _is_header(self, line: str) -> bool:
        """Detect if a line is likely a header"""
        if len(line) < 3:
            return False
            
        # All caps and not too long
        if line.isupper() and len(line) < 100:
            return True
            
        # Common header patterns
        header_patterns = [
            r'^Chapter \d+',
            r'^Section \d+',
            r'^\d+\.\s+[A-Z]',
            r'^[A-Z][^.!?]*:$',  # Ends with colon
        ]
        
        for pattern in header_patterns:
            if re.match(pattern, line):
                return True
                
        return False
    
    def _is_section_header(self, line: str) -> bool:
        """Check if line is a section header"""
        section_keywords = [
            'overview', 'summary', 'introduction', 'conclusion',
            'financial', 'statement', 'balance sheet', 'income',
            'cash flow', 'equity', 'assets', 'liabilities',
            'revenue', 'expenses', 'notes'
        ]
        
        line_lower = line.lower()
        return any(keyword in line_lower for keyword in section_keywords)
    
    def _form_paragraphs(self, lines: List[str]) -> str:
        """Form proper paragraphs from lines"""
        if not lines:
            return ""
            
        paragraphs = []
        current_paragraph = []
        
        for line in lines:
            # Check if line is a header (starts with #)
            if line.startswith('#'):
                # Save current paragraph if exists
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
                paragraphs.append(line)
            # Check for list items
            elif line.startswith(('- ', '* ', '• ')):
                # Save current paragraph if exists
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
                paragraphs.append(line)
            # Empty line or short line might indicate paragraph break
            elif len(line) < 40 and line.endswith(('.', '!', '?', ':')):
                current_paragraph.append(line)
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            else:
                current_paragraph.append(line)
                
        # Add remaining paragraph
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
            
        return '\n\n'.join(paragraphs)


def convert_pdf_file(pdf_path: Path, output_path: Path = None) -> Path:
    """
    Convenience function to convert a PDF file to Markdown
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output markdown file
        
    Returns:
        Path to the created markdown file
    """
    converter = PDFToMarkdownConverter()
    
    # Generate output path if not provided
    if output_path is None:
        output_path = pdf_path.with_suffix('.md')
        
    # Convert PDF to Markdown
    markdown_content = converter.convert_pdf_to_markdown(pdf_path)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    return output_path