"""Markdown renderer with KaTeX math support.

This module provides rendering of markdown content with:
- Standard markdown syntax (headers, lists, tables, code blocks)
- Inline math between $...$ (e.g., $x^2$)
- Block math between $$...$$ (e.g., $$\\int_0^1 x dx$$)
- Theme-aware colors
- Syntax highlighting for code blocks
"""

from __future__ import annotations

import re
from typing import Any

try:
    import markdown
    from markdown.extensions import Extension
    from markdown.preprocessors import Preprocessor
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    import pykatex
    KATEX_AVAILABLE = True
except ImportError:
    KATEX_AVAILABLE = False

try:
    from pygments.formatters import HtmlFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


class KaTeXPreprocessor(Preprocessor):
    """Markdown preprocessor to convert LaTeX math to KaTeX HTML."""

    # Regex patterns for math delimiters
    BLOCK_PATTERN = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)
    INLINE_PATTERN = re.compile(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)')

    def run(self, lines: list[str]) -> list[str]:
        """Process markdown lines to convert math notation to KaTeX HTML.
        
        Args:
            lines: List of markdown text lines.
            
        Returns:
            List of processed lines with math converted to HTML.
        """
        if not KATEX_AVAILABLE:
            # If pykatex is not available, leave math as-is
            return lines
        
        text = '\n'.join(lines)

        # Process block math first (to avoid conflicts with inline)
        def render_block(match: re.Match[str]) -> str:
            latex = match.group(1).strip()
            try:
                html = pykatex.render(latex, display_mode=True)
                return f'<div class="katex-block">{html}</div>'
            except Exception as e:
                return f'<div class="katex-error">Math Error: {str(e)}</div>'

        text = self.BLOCK_PATTERN.sub(render_block, text)

        # Process inline math
        def render_inline(match: re.Match[str]) -> str:
            latex = match.group(1).strip()
            try:
                html = pykatex.render(latex, display_mode=False)
                return f'<span class="katex-inline">{html}</span>'
            except Exception as e:
                return f'<span class="katex-error">(Math Error: {str(e)})</span>'

        text = self.INLINE_PATTERN.sub(render_inline, text)

        return text.split('\n')


class KaTeXExtension(Extension):
    """Markdown extension for KaTeX math rendering."""

    def extendMarkdown(self, md: Any) -> None:
        """Register the KaTeX preprocessor with the markdown processor.
        
        Args:
            md: Markdown processor instance.
        """
        md.preprocessors.register(
            KaTeXPreprocessor(md), 'katex', 27
        )


class MarkdownRenderer:
    """Service for rendering markdown with math support.
    
    This class handles:
    - Markdown-to-HTML conversion
    - KaTeX math rendering
    - Theme-aware styling
    - Syntax highlighting
    """

    def __init__(self) -> None:
        """Initialize the markdown renderer."""
        self._md_processor = None
        self._setup_processor()

    def _setup_processor(self) -> None:
        """Set up the markdown processor with extensions."""
        if not MARKDOWN_AVAILABLE:
            return
        
        extensions = [
            'extra',       # Tables, fenced code, etc.
            'nl2br',       # Newline to <br>
            'sane_lists',  # Better list handling
        ]
        
        # Add code highlighting if Pygments is available
        if PYGMENTS_AVAILABLE:
            extensions.append('codehilite')
        
        # Add KaTeX extension if available
        if KATEX_AVAILABLE:
            extensions.append(KaTeXExtension())
        
        try:
            self._md_processor = markdown.Markdown(
                extensions=extensions,
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'linenums': False,
                    }
                } if PYGMENTS_AVAILABLE else {}
            )
        except Exception:
            # Fallback to basic processor if extension setup fails
            self._md_processor = markdown.Markdown()

    def render(
        self,
        text: str,
        *,
        bg_color: str = "#ffffff",
        text_color: str = "#000000",
        code_bg: str = "#f5f5f5",
        link_color: str = "#3498db",
        border_color: str = "#cccccc",
        font_family: str = "sans-serif",
        font_size: int = 11,
        code_font: str = "'Fira Code', 'Consolas', monospace"
    ) -> str:
        """Render markdown text to themed HTML.
        
        Args:
            text: Markdown text to render.
            bg_color: Background color (hex).
            text_color: Text color (hex).
            code_bg: Code block background color (hex).
            link_color: Link color (hex).
            border_color: Border color for tables/blockquotes (hex).
            font_family: Font family for body text.
            font_size: Font size in points.
            code_font: Font family for code.
            
        Returns:
            HTML string with inline styles.
        """
        if not MARKDOWN_AVAILABLE or self._md_processor is None:
            # Fallback: basic HTML escaping and newline conversion
            return self._fallback_render(text, bg_color, text_color, font_family, font_size)
        
        # Reset the processor state for fresh conversion
        self._md_processor.reset()
        
        # Convert markdown to HTML
        try:
            html_body = self._md_processor.convert(text)
        except Exception:
            # Fallback on error
            return self._fallback_render(text, bg_color, text_color, font_family, font_size)
        
        # Get Pygments CSS if available
        pygments_css = ""
        if PYGMENTS_AVAILABLE:
            try:
                formatter = HtmlFormatter(style='monokai' if self._is_dark_bg(bg_color) else 'default')
                pygments_css = formatter.get_style_defs('.highlight')
            except Exception:
                pass
        
        # Build complete HTML with theme-aware styling
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
            font-family: {font_family};
            font-size: {font_size}pt;
            padding: 8px;
            margin: 0;
            line-height: 1.6;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1em;
            margin-bottom: 0.5em;
            font-weight: bold;
        }}
        
        h1 {{ font-size: 2em; }}
        h2 {{ font-size: 1.5em; }}
        h3 {{ font-size: 1.25em; }}
        
        p {{
            margin: 0.5em 0;
        }}
        
        code {{
            background-color: {code_bg};
            padding: 2px 4px;
            border-radius: 3px;
            font-family: {code_font};
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: {code_bg};
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 0.5em 0;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            border-radius: 0;
        }}
        
        blockquote {{
            border-left: 4px solid {border_color};
            padding-left: 10px;
            margin-left: 0;
            margin-right: 0;
            opacity: 0.8;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 0.5em 0;
        }}
        
        table, th, td {{
            border: 1px solid {border_color};
        }}
        
        th, td {{
            padding: 6px 12px;
            text-align: left;
        }}
        
        th {{
            background-color: {code_bg};
            font-weight: bold;
        }}
        
        a {{
            color: {link_color};
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        ul, ol {{
            margin: 0.5em 0;
            padding-left: 2em;
        }}
        
        li {{
            margin: 0.25em 0;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid {border_color};
            margin: 1em 0;
        }}
        
        /* KaTeX math styling */
        .katex-block {{
            text-align: center;
            margin: 1em 0;
        }}
        
        .katex-inline {{
            display: inline;
        }}
        
        .katex-error {{
            color: #e74c3c;
            font-style: italic;
        }}
        
        /* Pygments syntax highlighting */
        {pygments_css}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""
        return html

    def _fallback_render(
        self,
        text: str,
        bg_color: str,
        text_color: str,
        font_family: str,
        font_size: int
    ) -> str:
        """Fallback renderer when markdown library is not available.
        
        Args:
            text: Plain text to render.
            bg_color: Background color.
            text_color: Text color.
            font_family: Font family.
            font_size: Font size.
            
        Returns:
            Basic HTML with escaped text.
        """
        # Simple HTML escaping
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        
        # Convert newlines to <br>
        text = text.replace('\n', '<br>')
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
            font-family: {font_family};
            font-size: {font_size}pt;
            padding: 8px;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div>{text}</div>
</body>
</html>
"""
        return html

    def _is_dark_bg(self, color: str) -> bool:
        """Determine if a background color is dark.
        
        Args:
            color: Hex color string (e.g., "#1a1a1a").
            
        Returns:
            True if the color is dark, False otherwise.
        """
        try:
            # Remove # if present
            color = color.lstrip('#')
            
            # Convert to RGB
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            # Calculate relative luminance
            # https://www.w3.org/TR/WCAG20/#relativeluminancedef
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            
            return luminance < 0.5
        except Exception:
            return False


# Singleton instance
_renderer_instance: MarkdownRenderer | None = None


def get_markdown_renderer() -> MarkdownRenderer:
    """Get the singleton markdown renderer instance.
    
    Returns:
        Shared MarkdownRenderer instance.
    """
    global _renderer_instance
    if _renderer_instance is None:
        _renderer_instance = MarkdownRenderer()
    return _renderer_instance


__all__ = ["MarkdownRenderer", "get_markdown_renderer"]
