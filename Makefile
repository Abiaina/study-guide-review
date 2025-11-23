# Makefile for Study Guide Generation

.PHONY: help generate print web complete clean install

# Default target
help:
	@echo "Study Guide Generation Commands:"
	@echo ""
	@echo "  make generate    - Generate both printable and web versions (docs only)"
	@echo "  make complete    - Generate complete study guide (docs + flashcards) for printing"
	@echo "  make print       - Generate printable version only (docs only)"
	@echo "  make web         - Generate GitHub Pages version only (docs only)"
	@echo "  make clean       - Clean generated files"
	@echo "  make install     - Install required dependencies"
	@echo "  make help        - Show this help message"
	@echo ""

# Check if Python 3 is available
check-python:
	@python3 --version > /dev/null 2>&1 || (echo "❌ Python 3 is required but not installed" && exit 1)

# Generate both versions (docs only)
generate: check-python
	@echo "🚀 Generating Study Guide Versions..."
	@python3 scripts/generate_versions.py

# Generate complete study guide (docs + flashcards) for printing
# Fix code comments and ensure consistent code blocks
fix-code: check-python
	@echo "🔧 Fixing code comments and ensuring consistent code blocks..."
	@python3 scripts/fix_code_comments.py
	@echo "✅ Code blocks fixed"

# Post-process generated file to fix any remaining issues
post-process: check-python
	@echo "🔧 Post-processing generated study guide..."
	@python3 scripts/post_process_generated.py

# Generate complete study guide (docs + flashcards)
complete: check-python fix-code
	@echo "📚 Generating Complete Study Guide (docs + flashcards)..."
	@python3 scripts/generate_complete_study_guide.py
	@python3 scripts/post_process_generated.py
	@echo "✅ Complete study guide generated: generated/study-guide-complete-printable.md"

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

# Generate PDF from complete study guide (requires pandoc)
pdf-complete: complete
	@if command -v pandoc > /dev/null 2>&1; then \
		echo "📄 Generating PDF from complete study guide..."; \
		pandoc generated/study-guide-complete-printable.md -o study-guide-complete.pdf; \
		echo "✅ PDF generated: study-guide-complete.pdf"; \
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
stats: generate complete
	@echo "📊 Study Guide Statistics:"
	@echo "=========================="
	@if [ -f "generated/study-guide-printable.md" ]; then \
		echo "Printable version (docs only):"; \
		echo "  Size: $$(wc -c < generated/study-guide-printable.md | numfmt --to=iec)"; \
		echo "  Words: $$(wc -w < generated/study-guide-printable.md | tr -d ' ')"; \
		echo "  Lines: $$(wc -l < generated/study-guide-printable.md | tr -d ' ')"; \
	fi
	@if [ -f "generated/study-guide-complete.md" ]; then \
		echo ""; \
		echo "GitHub Pages version:"; \
		echo "  Size: $$(wc -c < generated/study-guide-complete.md | numfmt --to=iec)"; \
		echo "  Words: $$(wc -w < generated/study-guide-complete.md | tr -d ' ')"; \
		echo "  Lines: $$(wc -l < generated/study-guide-complete.md | tr -d ' ')"; \
	fi
	@if [ -f "generated/study-guide-complete-printable.md" ]; then \
		echo ""; \
		echo "Complete study guide (docs + flashcards):"; \
		echo "  Size: $$(wc -c < generated/study-guide-complete-printable.md | numfmt --to=iec)"; \
		echo "  Words: $$(wc -w < generated/study-guide-complete-printable.md | tr -d ' ')"; \
		echo "  Lines: $$(wc -l < generated/study-guide-complete-printable.md | tr -d ' ')"; \
	fi
