#!/usr/bin/env python3
"""
Cleanup script to remove redundant PDF converter files
Keeps only the core module and updates imports
"""
from pathlib import Path
import shutil
from datetime import datetime

def cleanup_redundant_files():
    """Remove redundant PDF converter files after backing them up"""
    backend_dir = Path(__file__).parent
    backup_dir = backend_dir / "backup_old_converters"
    
    # List of redundant PDF converter files to remove
    redundant_files = [
        "pdf_converter.py",
        "pdf_converter_advanced.py", 
        "pdf_converter_final.py",
        "pdf_converter_improved.py",
        "pdf_converter_simple.py",
        "pdf_converter_v2.py"
    ]
    
    # Keep pdf_converter_best.py for now as fallback
    files_backed_up = []
    files_removed = []
    
    # Create backup directory
    if any((backend_dir / f).exists() for f in redundant_files):
        backup_dir.mkdir(exist_ok=True)
        print(f"Created backup directory: {backup_dir}")
    
    # Backup and remove redundant files
    for filename in redundant_files:
        file_path = backend_dir / filename
        if file_path.exists():
            # Backup the file
            backup_path = backup_dir / filename
            shutil.copy2(file_path, backup_path)
            files_backed_up.append(filename)
            
            # Remove the original
            file_path.unlink()
            files_removed.append(filename)
            print(f"Backed up and removed: {filename}")
    
    # Create a README in the backup directory
    if files_backed_up:
        readme_content = f"""# Backup of Old PDF Converters
Created: {datetime.now().isoformat()}

These files were replaced by the unified core/pdf_converter.py module.

Files backed up:
{chr(10).join(f'- {f}' for f in files_backed_up)}

The new unified converter is located at: backend/core/pdf_converter.py

To restore these files if needed:
```bash
cp backup_old_converters/*.py ../
```
"""
        with open(backup_dir / "README.md", 'w') as f:
            f.write(readme_content)
        print(f"\nCreated README in backup directory")
    
    print(f"\nCleanup complete!")
    print(f"Files backed up: {len(files_backed_up)}")
    print(f"Files removed: {len(files_removed)}")
    
    if files_backed_up:
        print(f"\nBackups saved to: {backup_dir}")
        print("You can safely delete the backup directory once you've verified everything works.")

if __name__ == "__main__":
    cleanup_redundant_files()