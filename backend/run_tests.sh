#!/usr/bin/env bash
# Test runner script

echo "🧪 Running tests..."

# Run pytest
pytest --cov=app --cov-report=html --cov-report=term-missing tests/

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report: htmlcov/index.html"
