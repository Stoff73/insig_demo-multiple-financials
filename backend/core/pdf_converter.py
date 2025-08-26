"""
Unified PDF to Markdown converter
Consolidates all PDF converter versions into one optimized module
"""
import pdfplumber
from pathlib import Path
import re
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PDFToMarkdownConverter:
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
                formatted_line = self._format_text_line(line)
                if formatted_line:
                    text_content.append(formatted_line)
        
        # Combine text and tables
        if text_content:
            content.insert(0, "\n".join(text_content))
        
        return "\n\n".join(content)
    
    def _reconstruct_table(self, table: List[List]) -> List[List]:
        """Reconstruct and clean table data"""
        if not table:
            return []
        
        cleaned_table = []
        max_cols = max(len(row) if row else 0 for row in table)
        
        for row in table:
            if not row:
                continue
            
            # Clean cells and pad row to max columns
            cleaned_row = []
            for cell in row:
                cleaned_cell = self._clean_cell(cell)
                cleaned_row.append(cleaned_cell)
            
            # Pad with empty cells if needed
            while len(cleaned_row) < max_cols:
                cleaned_row.append("")
            
            # Skip rows that are entirely empty
            if any(cell for cell in cleaned_row):
                cleaned_table.append(cleaned_row)
        
        return cleaned_table
    
    def _clean_cell(self, cell: Any) -> str:
        """Clean and format a table cell"""
        if cell is None:
            return ""
        
        # Convert to string and clean
        cell_str = str(cell).strip()
        
        # Remove excessive whitespace
        cell_str = re.sub(r'\s+', ' ', cell_str)
        
        # Clean common artifacts
        cell_str = cell_str.replace('\n', ' ')
        
        return cell_str
    
    def _create_markdown_table(self, table: List[List]) -> Optional[str]:
        """Create a markdown table from cleaned data"""
        if not table or len(table) < 2:
            return None
        
        # Use first row as headers
        headers = table[0]
        rows = table[1:]
        
        # Create markdown table
        md_lines = []
        
        # Header row
        md_lines.append("| " + " | ".join(headers) + " |")
        
        # Separator row
        md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        # Data rows
        for row in rows:
            md_lines.append("| " + " | ".join(row) + " |")
        
        return "\n".join(md_lines)
    
    def _format_text(self, text: str) -> str:
        """Format extracted text"""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            formatted_line = self._format_text_line(line)
            if formatted_line:
                formatted_lines.append(formatted_line)
        
        return "\n".join(formatted_lines)
    
    def _format_text_line(self, line: str) -> str:
        """Format a single line of text"""
        line = line.strip()
        
        if not line:
            return ""
        
        # Detect headers (all caps, short lines)
        if line.isupper() and len(line) < 100:
            return f"## {line.title()}"
        
        # Detect section headers (ends with colon)
        if line.endswith(':') and len(line) < 100:
            return f"### {line}"
        
        # Regular text
        return line


# Compatibility aliases for existing code
BestPDFToMarkdownConverter = PDFToMarkdownConverter