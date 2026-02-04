# Example: Markdown with Math in LunaQt2

## Overview

This example demonstrates the markdown rendering capabilities in LunaQt2, including text formatting, math equations, code blocks, and tables.

## Text Formatting

You can use **bold text** for emphasis, _italic text_ for subtle emphasis, and even **_bold italic_** for maximum impact.

> "Mathematics is the language in which God has written the universe." - Galileo Galilei

## Mathematical Expressions

### Inline Math

Here's an inline equation: $f(x) = x^2 + 2x + 1$. You can also write Greek letters like $\alpha$, $\beta$, $\gamma$, and $\Delta$.

The famous Pythagorean theorem: $a^2 + b^2 = c^2$

### Block Equations

The quadratic formula:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

Euler's identity (one of the most beautiful equations in mathematics):

$$
e^{i\pi} + 1 = 0
$$

Integration example:

$$
\int_0^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

Matrix notation:

$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
\begin{pmatrix}
x \\
y
\end{pmatrix}
=
\begin{pmatrix}
ax + by \\
cx + dy
\end{pmatrix}
$$

## Code Blocks

### Python Example

```python
def calculate_factorial(n):
    """Calculate factorial using recursion."""
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

# Example usage
result = calculate_factorial(5)
print(f"5! = {result}")
```

### JavaScript Example

```javascript
const fibonacci = (n) => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
};

console.log(fibonacci(10)); // Output: 55
```

## Lists

### Unordered List

- First item
- Second item
  - Nested item 1
  - Nested item 2
- Third item

### Ordered List

1. Step one: Install dependencies
2. Step two: Configure settings
3. Step three: Run the application

### Task List

- [x] Implement markdown rendering
- [x] Add KaTeX support
- [x] Add syntax highlighting
- [ ] Add live preview (future)
- [ ] Add export to PDF (future)

## Tables

| Feature                | Status     | Priority |
| ---------------------- | ---------- | -------- |
| Markdown parsing       | ✅ Done    | High     |
| Math rendering (KaTeX) | ✅ Done    | High     |
| Syntax highlighting    | ✅ Done    | Medium   |
| Theme support          | ✅ Done    | High     |
| Edit mode              | ⏳ Planned | Medium   |
| Export to PDF          | ⏳ Planned | Low      |

## Links and Images

Visit the [KaTeX documentation](https://katex.org/docs/supported.html) for a full list of supported LaTeX commands.

Check out the [Python-Markdown extensions](https://python-markdown.github.io/extensions/) for additional formatting options.

## Physics and Engineering

### Equations of Motion

Velocity: $v = v_0 + at$

Displacement: $s = v_0 t + \frac{1}{2}at^2$

Kinetic energy: $E_k = \frac{1}{2}mv^2$

### Calculus

Derivative of $x^n$:

$$
\frac{d}{dx}(x^n) = nx^{n-1}
$$

Product rule:

$$
\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)
$$

## Statistics

### Normal Distribution

The probability density function:

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}
$$

### Bayes' Theorem

$$
P(A|B) = \frac{P(B|A)P(A)}{P(B)}
$$

## Conclusion

LunaQt2 now supports rich markdown formatting with beautiful math rendering! This makes it perfect for:

- 📚 Educational notebooks
- 🔬 Scientific documentation
- 📊 Data analysis reports
- 📝 Technical documentation
- 🎓 Homework and assignments

**Enjoy creating beautiful notebooks!** ✨
