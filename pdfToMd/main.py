from pathlib import Path
from markitdown import MarkItDown
import re

md = MarkItDown(enable_plugins=False) # Set to True to enable plugins

def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing problematic unicode characters that can cause issues in JSONL.
    """
    # Remove control characters (except newline, tab, carriage return)
    text = re.sub(r'[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]', '', text)
    
    # Replace problematic unicode characters with spaces
    # Keep: Basic Latin, Latin Extended, common punctuation, currency symbols, CJK characters
    allowed_ranges = (
        r'\u0020-\u007E'     # Basic Latin
        r'\u00A0-\u00FF'     # Latin-1 Supplement
        r'\u0100-\u017F'     # Latin Extended-A
        r'\u0180-\u024F'     # Latin Extended-B
        r'\u1E00-\u1EFF'     # Latin Extended Additional
        r'\u2000-\u206F'     # General Punctuation
        r'\u2070-\u209F'     # Superscripts and Subscripts
        r'\u20A0-\u20CF'     # Currency Symbols
        r'\u2100-\u214F'     # Letterlike Symbols
        r'\u2190-\u21FF'     # Arrows
        r'\u2200-\u22FF'     # Mathematical Operators
        r'\u2300-\u23FF'     # Miscellaneous Technical
        r'\u2400-\u243F'     # Control Pictures
        r'\u2440-\u245F'     # Optical Character Recognition
        r'\u2460-\u24FF'     # Enclosed Alphanumerics
        r'\u2500-\u257F'     # Box Drawing
        r'\u2580-\u259F'     # Block Elements
        r'\u25A0-\u25FF'     # Geometric Shapes
        r'\u2600-\u26FF'     # Miscellaneous Symbols
        r'\u2700-\u27BF'     # Dingbats
        r'\u3000-\u303F'     # CJK Symbols and Punctuation
        r'\u3040-\u309F'     # Hiragana
        r'\u30A0-\u30FF'     # Katakana
        r'\u4E00-\u9FFF'     # CJK Unified Ideographs
    )
    
    pattern = f'[^{allowed_ranges}]'
    text = re.sub(pattern, ' ', text)
    
    # Replace multiple spaces/whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text

# Define source and destination directories
source_dir = Path("../dataset/originalData")
dest_dir = Path("../dataset/mdData")

# Create destination directory if it doesn't exist
dest_dir.mkdir(parents=True, exist_ok=True)

# Get all PDF files from source directory
pdf_files = list(source_dir.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files to convert...")

# Process each PDF file
for pdf_file in pdf_files:
    try:
        print(f"Converting: {pdf_file.name}")
        
        # Convert PDF to markdown
        result = md.convert(str(pdf_file))
        
        # Sanitize the markdown content
        sanitized_content = sanitize_text(result.text_content)
        
        # Create output filename (replace .pdf with .md)
        output_filename = pdf_file.stem + ".md"
        output_path = dest_dir / output_filename
        
        # Save sanitized markdown content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sanitized_content)
        
        print(f"✓ Saved: {output_filename} (sanitized)")
        
    except Exception as e:
        print(f"✗ Error converting {pdf_file.name}: {str(e)}")

print("Conversion complete!")