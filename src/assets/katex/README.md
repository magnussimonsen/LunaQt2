# KaTeX Assets

This directory contains KaTeX CSS and fonts for offline math rendering.

## Files (to be downloaded)

You can download KaTeX assets from: https://github.com/KaTeX/KaTeX/releases

For version 0.16.9:

1. Download `katex.min.css` from the release
2. Download the `fonts/` folder from the release

Place the files here:

```
katex/
├── katex.min.css
└── fonts/
    ├── KaTeX_Main-Regular.woff2
    ├── KaTeX_Math-Italic.woff2
    ├── KaTeX_Size1-Regular.woff2
    ├── KaTeX_Size2-Regular.woff2
    ├── KaTeX_Size3-Regular.woff2
    ├── KaTeX_Size4-Regular.woff2
    └── ... (other font files)
```

## Alternative: Use pykatex

The current implementation uses `pykatex`, which handles KaTeX rendering server-side
without requiring CSS/fonts to be bundled. The pykatex package includes all necessary
KaTeX functionality.

If you want to switch to client-side KaTeX rendering (using Qt WebEngine), you would
need to bundle these assets and reference them locally in the HTML template.

## Current Status

✅ **Using pykatex** - Server-side math rendering, no asset bundling required  
⏭️ **Optional**: Bundle assets for Qt WebEngine implementation (future enhancement)
