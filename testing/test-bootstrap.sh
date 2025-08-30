#!/bin/bash
# Bootstrap Test Suite - Validate minimal architect kernel

echo "🧪 ARCHITECT KERNEL BOOTSTRAP TEST"
echo "=================================="

# Test 1: Kernel README Validation
echo "Test 1: Validating kernel README structure..."
if [ ! -f "README.md" ]; then
    echo "❌ FAIL: README.md not found"
    exit 1
fi

# Check for essential kernel components
if ! grep -q "Identity & Mission" README.md; then
    echo "❌ FAIL: Missing Identity & Mission section"
    exit 1
fi

if ! grep -q "Bootstrap Commands" README.md; then
    echo "❌ FAIL: Missing Bootstrap Commands section"
    exit 1
fi

if ! grep -q "Safety Protocol" README.md; then
    echo "❌ FAIL: Missing Safety Protocol section"
    exit 1
fi

echo "✅ PASS: Kernel README structure valid"

# Test 2: Framework Files Validation
echo "Test 2: Validating framework files..."
if [ ! -f "frameworks/programming-framework.md" ]; then
    echo "❌ FAIL: programming-framework.md not found"
    exit 1
fi

if ! grep -q "Command Interface Enhancement" frameworks/programming-framework.md; then
    echo "❌ FAIL: Invalid programming framework structure"
    exit 1
fi

echo "✅ PASS: Framework files valid"

# Test 3: Specialization Files Validation  
echo "Test 3: Validating specialization files..."
if [ ! -f "specializations/prototeam-specialization.md" ]; then
    echo "❌ FAIL: prototeam-specialization.md not found"
    exit 1
fi

if ! grep -q "Domain Identity Enhancement" specializations/prototeam-specialization.md; then
    echo "❌ FAIL: Invalid specialization structure"
    exit 1
fi

echo "✅ PASS: Specialization files valid"

# Test 4: Documentation Validation
echo "Test 4: Validating documentation..."
if [ ! -f "docs/BOOTSTRAP.md" ]; then
    echo "❌ FAIL: BOOTSTRAP.md not found"
    exit 1
fi

if ! grep -q "Quick Start" docs/BOOTSTRAP.md; then
    echo "❌ FAIL: Invalid bootstrap documentation"
    exit 1
fi

echo "✅ PASS: Documentation valid"

# Test 5: Directory Structure Validation
echo "Test 5: Validating directory structure..."
required_dirs=("frameworks" "specializations" "docs" "examples" "testing" "startup" "tools")

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ FAIL: Missing directory: $dir"
        exit 1
    fi
done

echo "✅ PASS: Directory structure valid"

# Test 6: Kernel Size Validation
echo "Test 6: Validating kernel size..."
kernel_lines=$(wc -l < README.md)
if [ "$kernel_lines" -gt 80 ]; then
    echo "⚠️  WARNING: Kernel README has $kernel_lines lines (target: <80)"
else
    echo "✅ PASS: Kernel size optimal ($kernel_lines lines)"
fi

# Test Summary
echo ""
echo "🎯 BOOTSTRAP TEST SUMMARY"
echo "========================="
echo "✅ All core tests passed"
echo "📝 Kernel README: $kernel_lines lines"
echo "🏗️  Framework files: $(ls frameworks/ | wc -l)"
echo "🎯 Specializations: $(ls specializations/ | wc -l)"
echo "📚 Documentation: $(ls docs/ | wc -l)"
echo ""
echo "🚀 Repository ready for architect bootstrap!"

# Optional: Syntax validation for markdown files
echo ""
echo "🔍 Optional: Markdown syntax validation..."
for file in README.md frameworks/*.md specializations/*.md docs/*.md; do
    if [ -f "$file" ]; then
        # Basic markdown validation - check for balanced headers
        if ! grep -q "^#" "$file"; then
            echo "⚠️  WARNING: $file may have header formatting issues"
        fi
    fi
done

echo "✅ Bootstrap validation complete!"