from pathlib import Path
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False) # Set to True to enable plugins

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
        
        # Create output filename (replace .pdf with .md)
        output_filename = pdf_file.stem + ".md"
        output_path = dest_dir / output_filename
        
        # Save markdown content to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        print(f"✓ Saved: {output_filename}")
        
    except Exception as e:
        print(f"✗ Error converting {pdf_file.name}: {str(e)}")

print("Conversion complete!")