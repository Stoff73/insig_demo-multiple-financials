import pdfplumber
from tabulate import tabulate
from pathlib import Path
import re
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class PDFToMarkdownConverter:
    """Enhanced PDF to Markdown converter with better table handling"""
    
    def __init__(self):
        self.page_break = "\n\n---\n\n"
        
    def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """
        Convert a PDF file to Markdown format with improved table extraction
        
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
        """Process a single PDF page with improved table detection"""
        page_content = []
        
        # Add page number as comment
        page_content.append(f"<!-- Page {page_num} -->\n")
        
        # Extract tables with optimized settings for financial documents
        table_settings = {
            "vertical_strategy": "text",  
            "horizontal_strategy": "text",
            "snap_tolerance": 3,
            "snap_x_tolerance": 3,
            "snap_y_tolerance": 3,
            "join_tolerance": 3,
            "join_x_tolerance": 3,
            "join_y_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 2,
            "min_words_horizontal": 2,
            "intersection_tolerance": 3,
            "text_tolerance": 3,
            "text_x_tolerance": 3,
            "text_y_tolerance": 3,
        }
        
        # Extract tables
        tables = page.extract_tables(table_settings)
        
        # If no tables found, try with looser settings
        if not tables:
            table_settings["min_words_vertical"] = 1
            table_settings["min_words_horizontal"] = 1
            tables = page.extract_tables(table_settings)
        
        # Process tables
        if tables:
            for table_idx, table in enumerate(tables):
                processed_table = self._process_financial_table(table)
                if processed_table:
                    page_content.append(processed_table)
                    page_content.append("")  # Add blank line after table
        
        # Extract remaining text (excluding table areas)
        text = page.extract_text()
        if text:
            # Get table bounding boxes to exclude from text
            table_areas = self._get_table_areas(page)
            processed_text = self._process_text_excluding_tables(text, table_areas)
            if processed_text:
                page_content.append(processed_text)
        
        return "\n".join(page_content)
    
    def _get_table_areas(self, page) -> List[Tuple[float, float, float, float]]:
        """Get bounding boxes of tables on the page"""
        table_areas = []
        tables = page.find_tables()
        for table in tables:
            if table.bbox:
                table_areas.append(table.bbox)
        return table_areas
    
    def _process_financial_table(self, table: List[List]) -> str:
        """Process a financial table with better structure preservation"""
        if not table:
            return ""
        
        # Clean the table
        cleaned_table = self._clean_financial_table(table)
        if not cleaned_table or len(cleaned_table) < 2:
            return ""
        
        # Fix common extraction issues
        cleaned_table = self._fix_table_structure(cleaned_table)
        
        # Detect table type and format accordingly
        if self._is_financial_statement(cleaned_table):
            return self._format_financial_statement(cleaned_table)
        else:
            return self._format_standard_table(cleaned_table)
    
    def _fix_table_structure(self, table: List[List]) -> List[List]:
        """Fix common table extraction issues"""
        if not table:
            return table
        
        fixed_table = []
        
        for row in table:
            # Check if first cell has multiple items concatenated
            if row and len(row[0]) > 50:
                first_cell = row[0]
                # Check for common financial row headers that got concatenated
                patterns = [
                    r'(Order intake|Revenue|Book-to-bill|Order book|Gross margin|Operating profit|'
                    r'Profit before tax|Earnings per share|Operating cash flow|Net Debt|EBITDA|'
                    r'Assets|Liabilities|Equity|Total)',
                    r'(Semiconductor|Industrial|Healthcare|Technology|Equipment)',
                    r'(Six months|Year ended|Quarter ended)',
                ]
                
                # Try to split concatenated headers
                for pattern in patterns:
                    matches = re.findall(pattern, first_cell, re.IGNORECASE)
                    if len(matches) > 1:
                        # Split the concatenated cell
                        parts = re.split(pattern, first_cell)
                        new_row = []
                        for part in parts:
                            if part.strip():
                                new_row.append(part.strip())
                        # Add rest of the row
                        new_row.extend(row[1:])
                        row = new_row
                        break
            
            # If we have a row with a very long first cell and empty other cells,
            # it might be a header or section separator
            if row and len(row[0]) > 30 and all(not cell for cell in row[1:]):
                # Try to parse it as multiple metrics
                metrics = re.findall(r'([A-Z][a-z]+(?:\s+[a-z]+)*)', row[0])
                if len(metrics) > 2:
                    # Create separate rows for each metric
                    for metric in metrics:
                        fixed_table.append([metric] + [''] * (len(row) - 1))
                    continue
            
            fixed_table.append(row)
        
        return fixed_table
    
    def _clean_financial_table(self, table: List[List]) -> List[List]:
        """Clean financial table data with better handling of empty cells"""
        if not table:
            return []
        
        cleaned = []
        for row in table:
            if row and any(self._clean_cell(cell) for cell in row):
                # Process each cell
                cleaned_row = []
                for cell in row:
                    cleaned_cell = self._clean_cell(cell)
                    cleaned_row.append(cleaned_cell)
                cleaned.append(cleaned_row)
        
        # Fix column alignment issues
        if cleaned:
            max_cols = max(len(row) for row in cleaned)
            for row in cleaned:
                while len(row) < max_cols:
                    row.append("")
        
        return cleaned
    
    def _clean_cell(self, cell: Any) -> str:
        """Clean individual table cell with better null handling"""
        if cell is None:
            return ""
        
        # Convert to string and clean
        cell_str = str(cell).strip()
        
        # Handle special characters
        cell_str = cell_str.replace('\n', ' ')
        
        # Don't over-compress spaces in text cells
        if not self._is_numeric_cell(cell_str):
            cell_str = re.sub(r'\s+', ' ', cell_str)
        else:
            # For numeric cells, remove internal spaces
            cell_str = cell_str.replace(' ', '')
        
        return cell_str
    
    def _is_financial_statement(self, table: List[List]) -> bool:
        """Detect if table is a financial statement"""
        if not table:
            return False
        
        # Check for common financial statement keywords
        financial_keywords = [
            'revenue', 'income', 'expense', 'profit', 'loss', 'assets', 
            'liabilities', 'equity', 'cash', 'margin', 'ebitda', 'operating',
            'net', 'gross', 'total', 'balance', 'statement'
        ]
        
        # Check first few rows for financial keywords
        for row in table[:3]:
            row_text = ' '.join(str(cell).lower() for cell in row)
            if any(keyword in row_text for keyword in financial_keywords):
                return True
        
        # Check if table has numeric columns
        numeric_cols = 0
        if len(table) > 1:
            for col_idx in range(len(table[0])):
                numeric_count = 0
                for row in table[1:]:
                    if col_idx < len(row):
                        if self._is_numeric_cell(row[col_idx]):
                            numeric_count += 1
                if numeric_count > len(table) * 0.5:
                    numeric_cols += 1
        
        return numeric_cols >= 2
    
    def _format_financial_statement(self, table: List[List]) -> str:
        """Format a financial statement table with proper structure"""
        if not table:
            return ""
        
        # Identify header rows (usually first 1-2 rows)
        header_rows = []
        data_rows = []
        
        for idx, row in enumerate(table):
            # Check if row is likely a header
            if idx < 2 and self._is_header_row(row):
                header_rows.append(row)
            else:
                data_rows.append(row)
        
        # If no clear headers, use first row
        if not header_rows and table:
            header_rows = [table[0]]
            data_rows = table[1:]
        
        # Build the markdown table
        markdown_lines = []
        
        # Combine multi-row headers if needed
        if len(header_rows) > 1:
            combined_headers = self._combine_header_rows(header_rows)
            header_row = combined_headers
        else:
            header_row = header_rows[0] if header_rows else []
        
        # Ensure headers are not empty
        header_row = [h if h else f"Column {i+1}" for i, h in enumerate(header_row)]
        
        # Add header
        markdown_lines.append("| " + " | ".join(header_row) + " |")
        
        # Add separator with alignment
        separator = "|"
        for idx, header in enumerate(header_row):
            # Check if column contains numbers
            is_numeric = False
            if idx > 0:  # First column is usually labels
                for row in data_rows:
                    if idx < len(row) and self._is_numeric_cell(row[idx]):
                        is_numeric = True
                        break
            
            if is_numeric:
                separator += " ---: |"  # Right align for numbers
            else:
                separator += " --- |"   # Left align for text
        
        markdown_lines.append(separator)
        
        # Add data rows
        for row in data_rows:
            # Ensure row has correct number of columns
            while len(row) < len(header_row):
                row.append("")
            row = row[:len(header_row)]
            
            # Format cells
            formatted_row = []
            for idx, cell in enumerate(row):
                if idx > 0 and self._is_numeric_cell(cell):
                    # Format numbers nicely
                    formatted_row.append(self._format_number(cell))
                else:
                    formatted_row.append(cell)
            
            markdown_lines.append("| " + " | ".join(formatted_row) + " |")
        
        return "\n".join(markdown_lines)
    
    def _format_standard_table(self, table: List[List]) -> str:
        """Format a standard table"""
        if not table or len(table) < 2:
            return ""
        
        # Use first row as headers
        headers = table[0]
        
        # Ensure headers are not empty
        headers = [h if h else f"Column {i+1}" for i, h in enumerate(headers)]
        
        markdown_lines = []
        
        # Add headers
        markdown_lines.append("| " + " | ".join(headers) + " |")
        
        # Add separator
        separator = "|"
        for idx, header in enumerate(headers):
            # Check if column is numeric
            is_numeric = False
            for row in table[1:]:
                if idx < len(row) and self._is_numeric_cell(row[idx]):
                    is_numeric = True
                    break
            
            if is_numeric:
                separator += " ---: |"
            else:
                separator += " --- |"
        
        markdown_lines.append(separator)
        
        # Add data rows
        for row in table[1:]:
            while len(row) < len(headers):
                row.append("")
            row = row[:len(headers)]
            
            markdown_lines.append("| " + " | ".join(row) + " |")
        
        return "\n".join(markdown_lines)
    
    def _is_header_row(self, row: List[str]) -> bool:
        """Check if a row is likely a header row"""
        if not row:
            return False
        
        # Count non-empty cells
        non_empty = sum(1 for cell in row if cell)
        
        # Headers often have mostly text, not numbers
        numeric_count = sum(1 for cell in row if self._is_numeric_cell(cell))
        
        # If mostly non-numeric and has content, likely a header
        return non_empty > 0 and numeric_count < len(row) * 0.5
    
    def _combine_header_rows(self, header_rows: List[List[str]]) -> List[str]:
        """Combine multiple header rows into one"""
        if not header_rows:
            return []
        
        combined = []
        max_cols = max(len(row) for row in header_rows)
        
        for col_idx in range(max_cols):
            col_parts = []
            for row in header_rows:
                if col_idx < len(row) and row[col_idx]:
                    col_parts.append(row[col_idx])
            
            combined.append(' '.join(col_parts))
        
        return combined
    
    def _is_numeric_cell(self, cell: str) -> bool:
        """Check if a cell contains numeric data"""
        if not cell:
            return False
        
        # Remove common formatting
        cleaned = str(cell).replace(',', '').replace('$', '').replace('£', '').replace('€', '')
        cleaned = cleaned.replace('(', '-').replace(')', '').strip()
        
        # Check for percentage
        if cleaned.endswith('%'):
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
        
        # Check for multipliers (e.g., "2.5x")
        if cleaned.endswith('x'):
            try:
                float(cleaned[:-1])
                return True
            except ValueError:
                pass
        
        # Check for basis points
        if 'bps' in cleaned.lower() or 'bp' in cleaned.lower():
            parts = re.findall(r'[\d.]+', cleaned)
            if parts:
                return True
        
        return False
    
    def _format_number(self, cell: str) -> str:
        """Format numeric cell for better readability"""
        if not cell:
            return ""
        
        cell_str = str(cell).strip()
        
        # Keep special formatting
        if '(' in cell_str and ')' in cell_str:
            return cell_str
        
        # Keep percentages and multipliers
        if cell_str.endswith('%') or cell_str.endswith('x'):
            return cell_str
        
        # Keep basis points
        if 'bps' in cell_str.lower() or 'bp' in cell_str.lower():
            return cell_str
        
        return cell_str
    
    def _process_text_excluding_tables(self, text: str, table_areas: List) -> str:
        """Process text while excluding table areas"""
        if not text:
            return ""
        
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that look like table data
            if self._looks_like_table_row(line):
                continue
            
            # Process headers and regular text
            if self._is_header(line):
                if line.isupper() and len(line) < 50:
                    processed_lines.append(f"\n## {line.title()}\n")
                elif self._is_section_header(line):
                    processed_lines.append(f"\n### {line}\n")
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
        
        return self._form_paragraphs(processed_lines)
    
    def _looks_like_table_row(self, line: str) -> bool:
        """Check if a line looks like it's from a table"""
        # Multiple numbers separated by spaces often indicates table data
        numbers = re.findall(r'\b\d+\.?\d*\b', line)
        if len(numbers) > 3:
            return True
        
        # Multiple currency symbols
        currency_symbols = line.count('$') + line.count('£') + line.count('€')
        if currency_symbols > 2:
            return True
        
        # Multiple percentages
        if line.count('%') > 2:
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
            r'^[A-Z][^.!?]*:$',
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
            'revenue', 'expenses', 'notes', 'management', 'analysis'
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
            # Headers
            if line.startswith('#'):
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
                paragraphs.append(line)
            # List items
            elif line.startswith(('- ', '* ', '• ', '+ ')):
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
                paragraphs.append(line)
            # Paragraph breaks
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