# Quick Start: Using Markdown in LunaQt2

## Creating a Markdown Cell

1. **Open LunaQt2**
2. **Create a new notebook** or open an existing one
3. **Add a markdown cell** (cell type: "markdown")
4. **Enter your markdown content**

## Basic Syntax

### Headings

```markdown
# Heading 1

## Heading 2

### Heading 3
```

### Text Formatting

```markdown
**bold text**
_italic text_
**_bold and italic_**
`inline code`
```

### Lists

```markdown
- Bullet point 1
- Bullet point 2
  - Nested point

1. Numbered item 1
2. Numbered item 2
```

### Links

```markdown
[Link text](https://example.com)
```

## Math Notation

### Inline Math

Use single dollar signs for inline math:

```markdown
The area of a circle is $A = \pi r^2$.
```

### Block Math

Use double dollar signs for centered equations:

```markdown
$$
E = mc^2
$$
```

### Common Math Symbols

| Symbol        | LaTeX                                    | Rendered |
| ------------- | ---------------------------------------- | -------- |
| Greek letters | `$\alpha, \beta, \gamma$`                | α, β, γ  |
| Fractions     | `$\frac{a}{b}$`                          | a/b      |
| Superscript   | `$x^2$`                                  | x²       |
| Subscript     | `$x_i$`                                  | xᵢ       |
| Square root   | `$\sqrt{x}$`                             | √x       |
| Summation     | `$\sum_{i=1}^{n}$`                       | Σ        |
| Integral      | `$\int_0^1 f(x)dx$`                      | ∫        |
| Matrix        | `$\begin{pmatrix}a&b\\c&d\end{pmatrix}$` | Matrix   |

### Examples

**Pythagorean Theorem**

```markdown
$a^2 + b^2 = c^2$
```

**Quadratic Formula**

```markdown
$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

**Euler's Identity**

```markdown
$$
e^{i\pi} + 1 = 0
$$
```

## Code Blocks

Use triple backticks with language name for syntax highlighting:

````markdown
```python
def hello():
    print("Hello, World!")
```
````

Supported languages include:

- Python
- JavaScript
- Java
- C/C++
- HTML/CSS
- SQL
- And 100+ more!

## Tables

```markdown
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

## Blockquotes

```markdown
> "In mathematics, you don't understand things. You just get used to them."
>
> - John von Neumann
```

## Tips and Tricks

### 1. Complex Equations

For multi-line equations, use `\begin{align}`:

```markdown
$$
\begin{align}
f(x) &= x^2 + 2x + 1 \\
     &= (x + 1)^2
\end{align}
$$
```

### 2. Chemical Formulas

Use subscripts for chemical notation:

```markdown
Water is $H_2O$, and glucose is $C_6H_{12}O_6$.
```

### 3. Matrices

```markdown
$$
A = \begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}
$$
```

### 4. Piecewise Functions

```markdown
$$
f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x^2 & \text{if } x < 0
\end{cases}
$$
```

## Resources

### KaTeX Documentation

- [Supported Functions](https://katex.org/docs/supported.html) - Full list of LaTeX commands
- [Support Table](https://katex.org/docs/support_table.html) - Compatibility reference

### Markdown Documentation

- [Python-Markdown](https://python-markdown.github.io/) - Core markdown syntax
- [GitHub Flavored Markdown](https://github.github.com/gfm/) - Extended syntax

### Math Symbols

- [LaTeX Math Symbols](http://tug.ctan.org/info/symbols/comprehensive/symbols-a4.pdf) - Comprehensive reference
- [Detexify](http://detexify.kirelabs.org/classify.html) - Draw symbols to find LaTeX code

## Keyboard Shortcuts (Future)

_Coming soon in future versions:_

- `Ctrl+B` - Bold text
- `Ctrl+I` - Italic text
- `Ctrl+K` - Insert link
- `Ctrl+M` - Insert inline math
- `Ctrl+Shift+M` - Insert block math

## Troubleshooting

### Math Not Rendering?

- Check that you're using `$` for inline and `$$` for block math
- Ensure there are no spaces between `$` and the content: `$x^2$` ✅ `$ x^2 $` ❌
- Verify LaTeX syntax is correct

### Code Not Highlighting?

- Specify the language after the opening triple backticks: ` ```python`
- Supported languages are listed in Pygments documentation

### Table Not Formatting?

- Ensure pipe characters `|` are aligned
- Header separator row must use `---` (at least 3 dashes)
- First row should be the header

## Examples to Try

Copy these into a markdown cell to see them in action!

### 1. Einstein's Field Equations

```markdown
$$
R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu}
$$
```

### 2. Schrödinger Equation

```markdown
$$
i\hbar\frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat{H}\Psi(\mathbf{r},t)
$$
```

### 3. Maxwell's Equations

```markdown
$$
\begin{align}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\epsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0\mathbf{J} + \mu_0\epsilon_0\frac{\partial \mathbf{E}}{\partial t}
\end{align}
$$
```

---

**Happy writing!** 📝✨

For more examples, see [MARKDOWN_EXAMPLE.md](MARKDOWN_EXAMPLE.md)
