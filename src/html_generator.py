"""
HTML template and CSS framework for Lei-Seca output files.
Provides the base HTML shell and all CSS components described in the spec.
"""

from __future__ import annotations

GOOGLE_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Lora:ital,wght@0,400;0,600;0,700;1,400&"
    "family=DM+Sans:wght@400;500;600;700&"
    "family=DM+Mono:wght@400;500&"
    "display=swap"
)

BASE_CSS = """
/* ========================================================
   LEI-SECA — Base stylesheet
   ======================================================== */

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  /* Institutional palette — overridden per document via inline style */
  --color-primary:      #1a3a5c;
  --color-primary-dark: #0f2340;
  --color-primary-mid:  #1e4878;
  --color-accent:       #c8922a;
  --color-accent-light: #f0c060;

  --color-bg:           #f8f7f4;
  --color-surface:      #ffffff;
  --color-border:       #ddd8ce;
  --color-text:         #1e1e1e;
  --color-text-muted:   #5a5a5a;

  /* Callout colours */
  --callout-blue-bg:    #e8f0fb;
  --callout-blue-bdr:   #2d6fd4;
  --callout-green-bg:   #e6f4ec;
  --callout-green-bdr:  #2a8a4a;
  --callout-yellow-bg:  #fdf6e3;
  --callout-yellow-bdr: #c8922a;
  --callout-red-bg:     #fdeaea;
  --callout-red-bdr:    #c0392b;

  /* Badge prazo */
  --badge-gold-bg:   #c8922a;
  --badge-gold-text: #ffffff;
  --badge-red-bg:    #c0392b;
  --badge-red-text:  #ffffff;

  /* Typography */
  --font-body:  'Lora', Georgia, serif;
  --font-ui:    'DM Sans', system-ui, sans-serif;
  --font-mono:  'DM Mono', 'Courier New', monospace;

  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.375rem;
  --text-2xl:  1.75rem;
  --text-3xl:  2.25rem;

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  --shadow-sm: 0 1px 3px rgba(0,0,0,.10);
  --shadow-md: 0 4px 12px rgba(0,0,0,.12);
}

body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: 1.75;
  color: var(--color-text);
  background: var(--color-bg);
}

/* ── Cover ────────────────────────────────────────────── */
.cover {
  background: var(--color-primary-dark);
  color: #fff;
  padding: 4rem 3rem 3.5rem;
  text-align: center;
}

.cover .norm-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 500;
  background: var(--color-accent);
  color: #fff;
  padding: .35em .9em;
  border-radius: var(--radius-sm);
  letter-spacing: .04em;
  margin-bottom: 1.5rem;
}

.cover h1 {
  font-family: var(--font-ui);
  font-size: var(--text-3xl);
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: .75rem;
}

.cover h2 {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  font-weight: 400;
  font-style: italic;
  color: rgba(255,255,255,.75);
  margin-bottom: 2rem;
}

.cover .tags {
  display: flex;
  flex-wrap: wrap;
  gap: .5rem;
  justify-content: center;
}

.cover .tags span {
  font-family: var(--font-ui);
  font-size: var(--text-xs);
  font-weight: 500;
  padding: .3em .85em;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,.35);
  color: rgba(255,255,255,.85);
}

/* ── Table of Contents ────────────────────────────────── */
.toc {
  background: var(--color-primary-mid);
  padding: 2rem 3rem;
}

.toc h3 {
  font-family: var(--font-ui);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: rgba(255,255,255,.55);
  margin-bottom: 1rem;
}

.toc a {
  display: flex;
  align-items: baseline;
  gap: .75rem;
  padding: .45rem 0;
  font-family: var(--font-ui);
  font-size: var(--text-sm);
  color: rgba(255,255,255,.85);
  text-decoration: none;
  border-bottom: 1px solid rgba(255,255,255,.1);
  transition: color .15s;
}

.toc a:hover { color: var(--color-accent-light); }

.toc a code {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  background: rgba(255,255,255,.12);
  padding: .15em .55em;
  border-radius: var(--radius-sm);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Main content ─────────────────────────────────────── */
.content {
  max-width: 860px;
  margin: 0 auto;
  padding: 3rem 2rem 5rem;
}

/* ── Section header ───────────────────────────────────── */
.section-block {
  margin-bottom: 3.5rem;
}

.section-label {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 500;
  color: var(--color-text-muted);
  letter-spacing: .06em;
  text-transform: uppercase;
  margin-bottom: .35rem;
}

.section-block h2 {
  font-family: var(--font-ui);
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-primary);
  border-bottom: 3px solid var(--color-accent);
  padding-bottom: .4rem;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: .75rem;
  flex-wrap: wrap;
}

.art-badge {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  background: var(--color-primary);
  color: #fff;
  padding: .2em .65em;
  border-radius: var(--radius-sm);
  font-weight: 500;
  vertical-align: middle;
}

/* ── Body typography ──────────────────────────────────── */
.section-block p {
  margin-bottom: 1rem;
  max-width: 72ch;
}

.section-block ul,
.section-block ol {
  margin: .75rem 0 1rem 1.5rem;
}

.section-block li {
  margin-bottom: .4rem;
}

.section-block strong {
  font-weight: 700;
  color: var(--color-text);
}

/* ── Callouts ─────────────────────────────────────────── */
.callout {
  border-left: 4px solid;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: .85rem 1.1rem;
  margin: 1.25rem 0;
  font-size: var(--text-sm);
  line-height: 1.65;
}

.callout-blue   { background: var(--callout-blue-bg);   border-color: var(--callout-blue-bdr);   }
.callout-green  { background: var(--callout-green-bg);  border-color: var(--callout-green-bdr);  }
.callout-yellow { background: var(--callout-yellow-bg); border-color: var(--callout-yellow-bdr); }
.callout-red    { background: var(--callout-red-bg);    border-color: var(--callout-red-bdr);    }

.callout strong {
  display: block;
  font-family: var(--font-ui);
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .06em;
  margin-bottom: .35rem;
}

.callout-blue   strong { color: var(--callout-blue-bdr);   }
.callout-green  strong { color: var(--callout-green-bdr);  }
.callout-yellow strong { color: var(--callout-yellow-bdr); }
.callout-red    strong { color: var(--callout-red-bdr);    }

/* ── Inline deadline badges ───────────────────────────── */
.badge-prazo {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: .8em;
  font-weight: 500;
  padding: .15em .6em;
  border-radius: var(--radius-sm);
  line-height: 1.4;
  vertical-align: baseline;
}

.badge-prazo-gold { background: var(--badge-gold-bg); color: var(--badge-gold-text); }
.badge-prazo-red  { background: var(--badge-red-bg);  color: var(--badge-red-text);  }
.badge-prazo      { background: var(--badge-gold-bg); color: var(--badge-gold-text); }

/* ── Tables ───────────────────────────────────────────── */
.table-wrap { overflow-x: auto; margin: 1.5rem 0; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

table thead tr {
  background: var(--color-primary-dark);
  color: #fff;
}

table thead th {
  font-family: var(--font-ui);
  font-weight: 600;
  padding: .65rem 1rem;
  text-align: left;
  letter-spacing: .03em;
}

table thead th.col-num {
  text-align: center;
  font-family: var(--font-mono);
}

table tbody tr:nth-child(even) { background: rgba(0,0,0,.06); }

table tbody td {
  padding: .55rem 1rem;
  border-bottom: 1px solid var(--color-border);
  vertical-align: top;
}

table tbody td:first-child { font-weight: 700; }

table tbody td.col-num {
  text-align: center;
  font-family: var(--font-mono);
}

/* ── Comparative cards ────────────────────────────────── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
  margin: 1.5rem 0;
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  border-radius: var(--radius-md);
  padding: 1.25rem 1.35rem;
  box-shadow: var(--shadow-sm);
}

.card.card-alt { border-top-color: var(--color-accent); }

.card h4 {
  font-family: var(--font-ui);
  font-size: var(--text-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .05em;
  color: var(--color-primary);
  margin-bottom: .85rem;
}

.card.card-alt h4 { color: var(--color-accent); }

.card ul { margin-left: 1.1rem; }
.card li { font-size: var(--text-sm); margin-bottom: .3rem; }

/* ── Procedural flow ──────────────────────────────────── */
.flow {
  margin: 1.5rem 0;
  padding-left: 0;
  list-style: none;
}

.flow-step {
  display: flex;
  gap: 1rem;
  position: relative;
  padding-bottom: 1.5rem;
}

.flow-step:last-child { padding-bottom: 0; }

.flow-step:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 1.1rem;
  top: 2.4rem;
  bottom: 0;
  width: 2px;
  background: var(--color-border);
}

.flow-icon {
  flex-shrink: 0;
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 700;
  box-shadow: var(--shadow-sm);
}

.flow-icon.step-action  { background: var(--color-primary); }
.flow-icon.step-check   { background: var(--callout-yellow-bdr); }
.flow-icon.step-outcome { background: var(--callout-green-bdr);  }
.flow-icon.step-sanction{ background: var(--callout-red-bdr);    }

.flow-body { padding-top: .2rem; }

.flow-body strong {
  font-family: var(--font-ui);
  font-size: var(--text-sm);
  font-weight: 700;
  display: block;
  margin-bottom: .2rem;
  color: var(--color-primary);
}

.flow-body p { font-size: var(--text-sm); margin: 0; }

/* ── Critical points section ──────────────────────────── */
.critical-section {
  background: var(--color-primary-dark);
  color: #fff;
  padding: 2.5rem 3rem;
  border-radius: var(--radius-lg);
  margin: 3rem 0;
}

.critical-section h2 {
  font-family: var(--font-ui);
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-accent-light);
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,.15);
  padding-bottom: .6rem;
}

.critical-section ul {
  list-style: none;
  margin: 0;
}

.critical-section li {
  padding: .55rem 0 .55rem 1.5rem;
  position: relative;
  border-bottom: 1px solid rgba(255,255,255,.08);
  font-size: var(--text-sm);
  line-height: 1.65;
  color: rgba(255,255,255,.88);
}

.critical-section li::before {
  content: '⚠';
  position: absolute;
  left: 0;
  color: var(--color-accent-light);
}

.critical-section .badge-prazo {
  background: rgba(255,255,255,.15);
  color: var(--color-accent-light);
}

/* ── Responsive ───────────────────────────────────────── */
@media (max-width: 680px) {
  .cover    { padding: 2.5rem 1.5rem 2rem; }
  .cover h1 { font-size: var(--text-2xl); }
  .toc      { padding: 1.5rem; }
  .content  { padding: 2rem 1.25rem 4rem; }
  .critical-section { padding: 1.75rem 1.5rem; border-radius: 0; }
  .cards-grid { grid-template-columns: 1fr; }
}

/* ── Print ────────────────────────────────────────────── */
@media print {
  body { background: #fff; }
  .cover, .toc, .critical-section {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .callout, table thead, .art-badge, .badge-prazo, .flow-icon, .card {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .toc a { color: #000; }
  .content { max-width: 100%; padding: 0 1cm; }
}
"""


def build_html(title: str, body: str, palette: str = "") -> str:
    """
    Wrap *body* (the LLM-generated inner HTML) in the full HTML shell.

    Parameters
    ----------
    title   : plain-text document title shown in <title>.
    body    : HTML fragment produced by the LLM (cover + toc + sections).
    palette : optional inline ``<style>`` block to override :root CSS vars.
    """
    palette_block = f"\n  <style>\n{palette}\n  </style>" if palette else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Lei-Seca</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{GOOGLE_FONTS_URL}" rel="stylesheet">
  <style>
{BASE_CSS}
  </style>{palette_block}
</head>
<body>
{body}
</body>
</html>
"""
