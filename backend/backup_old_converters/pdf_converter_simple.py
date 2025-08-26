import pdfplumber
from pathlib import Path
import re
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class PDFToMarkdownConverter:
    """Simple PDF to Markdown converter that preserves text structure"""
    
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
        
        # Extract text
        text = page.extract_text()
        
        if text:
            # Process the text content
            processed_text = self._process_text(text)
            if processed_text:
                page_content.append(processed_text)
        
        return "\n".join(page_content)
    
    def _process_text(self, text: str) -> str:
        """Process extracted text and format it properly"""
        if not text:
            return ""
        
        lines = text.split('\n')
        processed_content = []
        current_section = []
        in_table = False
        table_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Detect headers
            if self._is_header(line):
                # Save any pending content
                if current_section:
                    processed_content.extend(self._format_section(current_section))
                    current_section = []
                if table_lines:
                    processed_content.append(self._format_table_from_text(table_lines))
                    table_lines = []
                    in_table = False
                
                # Add header
                if line.isupper() and len(line) < 50:
                    processed_content.append(f"\n## {line.title()}\n")
                elif self._is_major_section(line):
                    processed_content.append(f"\n## {line}\n")
                else:
                    processed_content.append(f"\n### {line}\n")
            
            # Detect table-like content
            elif self._looks_like_table_row(line):
                in_table = True
                table_lines.append(line)
            
            # If we were in a table but hit non-table content
            elif in_table and not self._looks_like_table_row(line):
                # Process accumulated table lines
                if table_lines:
                    table_md = self._format_table_from_text(table_lines)
                    if table_md:
                        processed_content.append(table_md)
                    table_lines = []
                in_table = False
                current_section.append(line)
            
            # Regular text
            else:
                current_section.append(line)
        
        # Process any remaining content
        if current_section:
            processed_content.extend(self._format_section(current_section))
        if table_lines:
            table_md = self._format_table_from_text(table_lines)
            if table_md:
                processed_content.append(table_md)
        
        return "\n".join(processed_content)
    
    def _format_table_from_text(self, lines: List[str]) -> str:
        """Convert text lines that look like a table into Markdown table"""
        if not lines:
            return ""
        
        # Try to detect common financial table patterns
        # Look for lines with consistent structure
        
        # Check if this looks like a financial statement table
        if any('revenue' in line.lower() or 'profit' in line.lower() or 
               'assets' in line.lower() or 'equity' in line.lower() for line in lines):
            return self._format_financial_table_text(lines)
        
        # Otherwise, try to format as a generic table
        return self._format_generic_table(lines)
    
    def _format_financial_table_text(self, lines: List[str]) -> str:
        """Format financial statement text as a table"""
        if not lines:
            return ""
        
        # Common patterns for financial tables
        table_data = []
        
        for line in lines:
            # Parse line for financial data
            # Look for pattern: Label ... numbers
            
            # Extract numbers from the line
            numbers = re.findall(r'[\d,]+\.?\d*[%xp]?|\([^)]+\)', line)
            
            # Extract the label (text before numbers)
            if numbers:
                # Find position of first number
                first_num_pos = len(line)
                for num in numbers:
                    pos = line.find(num)
                    if pos != -1 and pos < first_num_pos:
                        first_num_pos = pos
                
                label = line[:first_num_pos].strip()
                
                # Clean up the label
                label = re.sub(r'\s+', ' ', label)
                
                if label:
                    row = [label] + numbers
                    table_data.append(row)
            else:
                # Line might be a header or label
                if line and not line.isspace():
                    # Could be a section header within the table
                    if len(line) < 50:
                        table_data.append([line])
        
        if not table_data:
            return "\n".join(lines)
        
        # Format as markdown table
        return self._create_markdown_table(table_data)
    
    def _format_generic_table(self, lines: List[str]) -> str:
        """Format generic table from text lines"""
        if not lines:
            return ""
        
        # Try to parse as space-separated values
        table_data = []
        
        for line in lines:
            # Split by multiple spaces (assuming columns are separated by spaces)
            parts = re.split(r'\s{2,}', line)
            if len(parts) > 1:
                table_data.append(parts)
            else:
                # Single column or header
                table_data.append([line])
        
        if table_data:
            return self._create_markdown_table(table_data)
        
        return "\n".join(lines)
    
    def _create_markdown_table(self, data: List[List[str]]) -> str:
        """Create a markdown table from data"""
        if not data:
            return ""
        
        # Determine the maximum number of columns
        max_cols = max(len(row) for row in data)
        
        # Normalize all rows to have the same number of columns
        for row in data:
            while len(row) < max_cols:
                row.append("")
        
        # If we only have one row, it's not really a table
        if len(data) == 1:
            return " ".join(data[0])
        
        # Check if first row looks like headers
        first_row = data[0]
        has_headers = not any(self._is_numeric(cell) for cell in first_row)
        
        if not has_headers:
            # Add generic headers
            headers = [f"Column {i+1}" for i in range(max_cols)]
            data.insert(0, headers)
        
        # Build the markdown table
        lines = []
        
        # Headers
        lines.append("| " + " | ".join(data[0]) + " |")
        
        # Separator
        separator = "|"
        for i in range(max_cols):
            # Check if column is numeric (excluding header)
            is_numeric = False
            if len(data) > 1:
                for row in data[1:]:
                    if i < len(row) and self._is_numeric(row[i]):
                        is_numeric = True
                        break
            
            if is_numeric:
                separator += " ---: |"
            else:
                separator += " --- |"
        lines.append(separator)
        
        # Data rows
        for row in data[1:]:
            lines.append("| " + " | ".join(row) + " |")
        
        return "\n".join(lines) + "\n"
    
    def _is_numeric(self, text: str) -> bool:
        """Check if text represents a number"""
        if not text:
            return False
        
        # Remove formatting
        cleaned = text.replace(',', '').replace('$', '').replace('£', '').replace('€', '')
        cleaned = cleaned.replace('(', '-').replace(')', '').strip()
        
        # Check for percentage
        if cleaned.endswith('%'):
            try:
                float(cleaned[:-1])
                return True
            except ValueError:
                pass
        
        # Check for multiplier
        if cleaned.endswith('x'):
            try:
                float(cleaned[:-1])
                return True
            except ValueError:
                pass
        
        # Check for regular number
        try:
            float(cleaned)
            return True
        except ValueError:
            pass
        
        return False
    
    def _looks_like_table_row(self, line: str) -> bool:
        """Check if a line looks like it's from a table"""
        # Has multiple numbers
        numbers = re.findall(r'\b[\d,]+\.?\d*[%xp]?\b|\([^)]+\)', line)
        if len(numbers) >= 2:
            return True
        
        # Has financial metrics with values
        financial_patterns = [
            r'revenue.*\d',
            r'profit.*\d',
            r'margin.*\d',
            r'assets.*\d',
            r'equity.*\d',
            r'cash.*\d',
            r'debt.*\d',
            r'\d+.*\d+.*\d+',  # Multiple numbers in a row
        ]
        
        line_lower = line.lower()
        for pattern in financial_patterns:
            if re.search(pattern, line_lower):
                return True
        
        return False
    
    def _is_header(self, line: str) -> bool:
        """Detect if a line is likely a header"""
        if len(line) < 3:
            return False
        
        # All caps headers
        if line.isupper() and len(line) < 100:
            return True
        
        # Common header patterns
        header_patterns = [
            r'^[A-Z][A-Za-z\s]+:$',  # Ends with colon
            r'^\d+\.\s+[A-Z]',  # Numbered sections
            r'^(Chief|Director|Chairman|President)',  # Executive titles
            r'^(Financial|Operational|Strategic)',  # Report sections
        ]
        
        for pattern in header_patterns:
            if re.match(pattern, line):
                return True
        
        return False
    
    def _is_major_section(self, line: str) -> bool:
        """Check if this is a major section header"""
        major_sections = [
            'executive', 'financial', 'operational', 'strategic',
            'chairman', 'chief', 'director', 'president',
            'statement', 'report', 'review', 'analysis',
            'consolidated', 'balance sheet', 'income statement',
            'cash flow', 'equity'
        ]
        
        line_lower = line.lower()
        return any(section in line_lower for section in major_sections)
    
    def _format_section(self, lines: List[str]) -> List[str]:
        """Format a section of regular text"""
        if not lines:
            return []
        
        # Join lines that are part of the same paragraph
        paragraphs = []
        current_para = []
        
        for line in lines:
            # Check if this starts a new paragraph
            if line.startswith(('•', '-', '*', '+')):
                # Bullet point
                if current_para:
                    paragraphs.append(' '.join(current_para))
                    current_para = []
                paragraphs.append(line)
            elif line[0].isupper() and current_para and current_para[-1].endswith('.'):
                # New sentence starting with capital after period
                paragraphs.append(' '.join(current_para))
                current_para = [line]
            else:
                # Continue current paragraph
                current_para.append(line)
        
        # Add remaining paragraph
        if current_para:
            paragraphs.append(' '.join(current_para))
        
        # Add spacing between paragraphs
        formatted = []
        for para in paragraphs:
            formatted.append(para)
            if not para.startswith(('•', '-', '*', '+')):
                formatted.append("")  # Add blank line after paragraphs
        
        return formatted


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