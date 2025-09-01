#!/bin/bash

# Generate combined versions of the study guide
# This script runs the Python generator and provides feedback

echo "🚀 Generating Study Guide Versions..."
echo "======================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "scripts/generate_versions.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "Current directory: $(pwd)"
    echo "Expected files: scripts/generate_versions.py"
    exit 1
fi

# Run the Python script
echo "📝 Running generation script..."
python3 scripts/generate_versions.py

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Generation completed successfully!"
    echo ""
    echo "📁 Generated files:"
    echo "  - generated/study-guide-printable.md (for printing)"
    echo "  - generated/study-guide-complete.md (for GitHub Pages)"
    echo ""
    echo "🔄 Next steps:"
    echo "  1. Review the generated files in the 'generated/' directory"
    echo "  2. Copy study-guide-complete.md to docs/ for web viewing"
    echo "  3. Use study-guide-printable.md for printing or PDF conversion"
    echo ""
    echo "🖨️  To convert to PDF (requires pandoc):"
    echo "  pandoc generated/study-guide-printable.md -o study-guide.pdf"
else
    echo "❌ Generation failed. Please check the error messages above."
    exit 1
fi
