# Makefile for Study Guide Generation

.PHONY: help generate print web clean install

# Default target
help:
	@echo "Study Guide Generation Commands:"
	@echo ""
	@echo "  make generate    - Generate both printable and web versions"
	@echo "  make print       - Generate printable version only"
	@echo "  make web         - Generate GitHub Pages version only"
	@echo "  make clean       - Clean generated files"
	@echo "  make install     - Install required dependencies"
	@echo "  make help        - Show this help message"
	@echo ""

# Check if Python 3 is available
check-python:
	@python3 --version > /dev/null 2>&1 || (echo "❌ Python 3 is required but not installed" && exit 1)

# Generate both versions
generate: check-python
	@echo "🚀 Generating Study Guide Versions..."
	@python3 scripts/generate_versions.py

# Generate printable version only
print: check-python
	@echo "📖 Generating Printable Version..."
	@python3 -c "import sys; sys.path.append('scripts'); from generate_versions import *; docs_dir = Path('docs'); output_dir = Path('generated'); output_dir.mkdir(exist_ok=True); generate_printable_version(docs_dir, output_dir / 'study-guide-printable.md'); print('✅ Printable version generated: generated/study-guide-printable.md')"

# Generate web version only
web: check-python
	@echo "🌐 Generating GitHub Pages Version..."
	@python3 -c "import sys; sys.path.append('scripts'); from generate_versions import *; docs_dir = Path('docs'); output_dir = Path('generated'); output_dir.mkdir(exist_ok=True); generate_github_pages_version(docs_dir, output_dir / 'study-guide-complete.md'); print('✅ GitHub Pages version generated: generated/study-guide-complete.md')"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -rf generated/
	@echo "✅ Cleaned generated/ directory"

# Install dependencies (if any)
install:
	@echo "📦 Installing dependencies..."
	@echo "✅ No external dependencies required (uses Python standard library)"

# Generate PDF from printable version (requires pandoc)
pdf: generate
	@if command -v pandoc > /dev/null 2>&1; then \
		echo "📄 Generating PDF..."; \
		pandoc generated/study-guide-printable.md -o study-guide.pdf; \
		echo "✅ PDF generated: study-guide.pdf"; \
	else \
		echo "❌ Pandoc is required for PDF generation"; \
		echo "Install pandoc: https://pandoc.org/installing.html"; \
		exit 1; \
	fi

# Deploy complete version to docs (for GitHub Pages)
deploy: generate
	@echo "🚀 Deploying complete version to docs..."
	@cp generated/study-guide-complete.md docs/study-guide-complete.md
	@echo "✅ Complete version deployed to docs/study-guide-complete.md"
	@echo "💡 Commit and push to update GitHub Pages"

# Show file sizes and word counts
stats: generate
	@echo "📊 Study Guide Statistics:"
	@echo "=========================="
	@if [ -f "generated/study-guide-printable.md" ]; then \
		echo "Printable version:"; \
		echo "  Size: $$(wc -c < generated/study-guide-printable.md | numfmt --to=iec)"; \
		echo "  Words: $$(wc -w < generated/study-guide-printable.md | tr -d ' ')"; \
		echo "  Lines: $$(wc -l < generated/study-guide-printable.md | tr -d ' ')"; \
	fi
	@if [ -f "generated/study-guide-complete.md" ]; then \
		echo ""; \
		echo "GitHub Pages version:"; \
		echo "  Size: $$(wc -c < generated/study-guide-complete.md | numfmt --to=iec)"; \
		echo "  Words: $$(wc -c < generated/study-guide-complete.md | tr -d ' ')"; \
		echo "  Lines: $$(wc -l < generated/study-guide-complete.md | tr -d ' ')"; \
	fi
