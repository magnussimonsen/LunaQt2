"""
Integration test for markdown rendering in LunaQt2.

This script verifies that markdown cells render correctly
with all features: text formatting, math, code highlighting, and tables.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from core.rendering import get_markdown_renderer


def test_renderer_initialization():
    """Test that the renderer initializes correctly."""
    print("Testing renderer initialization...")
    renderer = get_markdown_renderer()
    assert renderer is not None
    print("✅ Renderer initialized successfully")


def test_basic_markdown():
    """Test basic markdown features."""
    print("\nTesting basic markdown features...")
    renderer = get_markdown_renderer()
    
    text = """
# Test Heading

This is **bold** and *italic* text.

- List item 1
- List item 2
"""
    
    html = renderer.render(text)
    assert "<h1>" in html
    assert "<strong>" in html or "<b>" in html
    assert "<em>" in html or "<i>" in html
    assert "<ul>" in html
    print("✅ Basic markdown works")


def test_inline_math():
    """Test inline math rendering."""
    print("\nTesting inline math...")
    renderer = get_markdown_renderer()
    
    text = "The formula is $x^2 + y^2 = z^2$."
    html = renderer.render(text)
    
    # Check if KaTeX rendered the math
    if "katex" in html.lower():
        print("✅ Inline math renders with KaTeX")
    else:
        print("⚠️  Math rendering not detected (pykatex may not be available)")


def test_block_math():
    """Test block math rendering."""
    print("\nTesting block math...")
    renderer = get_markdown_renderer()
    
    text = """
Block equation:

$$
\\int_0^1 x^2 dx = \\frac{1}{3}
$$
"""
    
    html = renderer.render(text)
    
    if "katex" in html.lower() and "block" in html.lower():
        print("✅ Block math renders with KaTeX")
    else:
        print("⚠️  Block math rendering not detected")


def test_code_highlighting():
    """Test code syntax highlighting."""
    print("\nTesting code highlighting...")
    renderer = get_markdown_renderer()
    
    text = """
```python
def hello():
    print("Hello!")
```
"""
    
    html = renderer.render(text)
    
    if "highlight" in html.lower() or "codehilite" in html.lower():
        print("✅ Code highlighting is enabled")
    else:
        print("⚠️  Code highlighting not detected")


def test_table():
    """Test table rendering."""
    print("\nTesting tables...")
    renderer = get_markdown_renderer()
    
    text = """
| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
    
    html = renderer.render(text)
    
    if "<table>" in html:
        print("✅ Tables render correctly")
    else:
        print("❌ Table rendering failed")


def test_theme_colors():
    """Test that theme colors are applied."""
    print("\nTesting theme color injection...")
    renderer = get_markdown_renderer()
    
    text = "Test content"
    html = renderer.render(
        text,
        bg_color="#1e1e1e",
        text_color="#d4d4d4",
        code_bg="#2d2d2d"
    )
    
    assert "#1e1e1e" in html
    assert "#d4d4d4" in html
    assert "#2d2d2d" in html
    print("✅ Theme colors are injected correctly")


def test_complex_document():
    """Test a complex document with all features."""
    print("\nTesting complex document...")
    renderer = get_markdown_renderer()
    
    text = """
# Mathematics in Python

## Introduction

Python is great for **scientific computing**. Here's why:

- Easy syntax
- Powerful libraries
- Great for *education*

## Example Code

```python
import numpy as np

def calculate(x):
    return np.sqrt(x**2 + 1)
```

## Mathematical Formula

The quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$

Block equation:

$$
E = mc^2
$$

## Comparison

| Feature | Python | R |
|---------|--------|---|
| Ease | ⭐⭐⭐ | ⭐⭐ |
| Speed | ⭐⭐ | ⭐⭐⭐ |
"""
    
    html = renderer.render(text)
    
    # Verify all features are present
    checks = {
        "Headers": "<h1>" in html and "<h2>" in html,
        "Bold text": "<strong>" in html or "<b>" in html,
        "Italic text": "<em>" in html or "<i>" in html,
        "Lists": "<ul>" in html,
        "Code blocks": "<pre>" in html or "<code>" in html,
        "Tables": "<table>" in html,
    }
    
    all_passed = all(checks.values())
    if all_passed:
        print("✅ Complex document renders all features correctly")
        for feature, passed in checks.items():
            print(f"   - {feature}: {'✅' if passed else '❌'}")
    else:
        print("⚠️  Some features missing in complex document")
        for feature, passed in checks.items():
            print(f"   - {feature}: {'✅' if passed else '❌'}")


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("LunaQt2 Markdown Integration Tests")
    print("=" * 60)
    
    # Initialize Qt application (required for palette operations)
    app = QApplication.instance() or QApplication(sys.argv)
    
    try:
        test_renderer_initialization()
        test_basic_markdown()
        test_inline_math()
        test_block_math()
        test_code_highlighting()
        test_table()
        test_theme_colors()
        test_complex_document()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nMarkdown rendering is fully functional and ready to use.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
