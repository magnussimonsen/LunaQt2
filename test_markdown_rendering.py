"""Test markdown rendering functionality."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.rendering import get_markdown_renderer

def test_basic_markdown():
    """Test basic markdown rendering."""
    renderer = get_markdown_renderer()
    
    # Test basic markdown
    markdown_text = """# Heading 1

This is a paragraph with **bold** and *italic* text.

## Heading 2

- Item 1
- Item 2
- Item 3

### Code Block

```python
def hello():
    print("Hello, World!")
```

### Inline Math

The quadratic formula is $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$.

### Block Math

$$
\\int_0^1 x^2 dx = \\frac{1}{3}
$$

### Table

| Name | Age |
|------|-----|
| Alice | 25 |
| Bob | 30 |
"""
    
    html = renderer.render(
        markdown_text,
        bg_color="#1e1e1e",
        text_color="#d4d4d4",
        code_bg="#2d2d2d",
        link_color="#3498db",
        border_color="#444444",
    )
    
    print("Markdown rendered successfully!")
    print(f"HTML length: {len(html)} characters")
    
    # Check that key elements are present
    assert "<h1>" in html, "H1 heading not found"
    assert "<strong>" in html or "<b>" in html, "Bold text not found"
    assert "<em>" in html or "<i>" in html, "Italic text not found"
    assert "<ul>" in html, "Unordered list not found"
    assert "<table>" in html, "Table not found"
    
    # Check for math rendering
    if "katex" in html.lower():
        print("✓ KaTeX math rendering is working!")
    else:
        print("⚠ KaTeX math rendering not detected (pykatex might not be available)")
    
    # Check for code highlighting
    if "highlight" in html.lower():
        print("✓ Syntax highlighting is working!")
    else:
        print("⚠ Syntax highlighting not detected (Pygments might not be fully configured)")
    
    print("\n✅ Markdown renderer test passed!")
    return html


if __name__ == "__main__":
    html = test_basic_markdown()
    
    # Optionally, save to file for inspection
    with open("test_markdown_output.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\n📄 Output saved to test_markdown_output.html")
