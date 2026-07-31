#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensambla la PWA de Programación Concurrente reutilizando el shell probado de
aprendizaje-automatico/index.html (todo su CSS/JS: buscador, notas, resaltador,
modo oscuro, service worker) y reemplazando SOLO el contenido, el índice y la marca.

Genera:
  - index.html      (app PWA completa)
  - resumen.html    (versión standalone imprimible)
  - resumen.md      (mirror en Markdown, fuente portable)

El contenido se escribe UNA sola vez en content/part-*.html.
Los bloques de código van como <pre data-code="rust">...</pre> (se escapan solos).
Los diagramas van como <div class="mermaid">...</div> (evitar '<' literal adentro).
"""
import os
import re
import glob
import html as htmllib

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'aprendizaje-automatico', 'index.html')

ACCENT = '#c2410c'

ROOT_LIGHT = """:root {
      color-scheme: light;
      --bg: #f7f5f2;
      --surface: #ffffff;
      --surface-2: #f1ece5;
      --ink: #221a13;
      --muted: #6d6154;
      --line: #e4dccf;
      --accent: #c2410c;
      --accent-2: #fbe7d6;
      --accent-ink: #9a3412;
      --warm: #9b5f1d;
      --warm-bg: #fbe4c9;
      --danger: #a23b3b;
      --danger-bg: #fbe3e0;
      --blue: #3f5bb2;
      --blue-bg: #e7ecfb;
      --hl-yellow: #ffe08a;
      --hl-mint: #b7ecc6;
      --hl-pink: #ffc1d2;
      --hl-blue: #bcd7ff;
      --shadow: 0 18px 55px rgba(58, 38, 18, .09);
      --radius: 18px;
      --sidebar: 300px;
    }"""

ROOT_DARK = """html[data-theme="dark"] {
      color-scheme: dark;
      --bg: #16110c;
      --surface: #1e1710;
      --surface-2: #2a2118;
      --ink: #f3ede4;
      --muted: #b2a493;
      --line: #382c20;
      --accent: #fb923c;
      --accent-2: #3a2416;
      --accent-ink: #fed7aa;
      --warm: #f0b766;
      --warm-bg: #3b2c19;
      --danger: #f3a29a;
      --danger-bg: #3e2422;
      --blue: #9bb0f7;
      --blue-bg: #1e2440;
      --hl-yellow: #725d19;
      --hl-mint: #1f5a37;
      --hl-pink: #71384b;
      --hl-blue: #294f78;
      --shadow: 0 18px 55px rgba(0, 0, 0, .28);
    }"""

INJECTED_STYLE = """  <style>
    pre.code { margin: 16px 0; padding: 15px 18px; overflow-x: auto; border: 1px solid var(--line); border-radius: 12px; background: var(--surface-2); color: var(--ink); font-size: 13.5px; line-height: 1.55; -webkit-overflow-scrolling: touch; }
    pre.code code { padding: 0; background: transparent; font-size: inherit; }
    .diagram { margin: 22px 0; padding: 16px 14px 12px; overflow-x: auto; border: 1px solid var(--line); border-radius: 16px; background: #fbfaf8; }
    .diagram .mermaid { display: flex; justify-content: center; min-width: 0; text-align: center; }
    .diagram figcaption { margin-top: 10px; color: #5a4d40; font-size: 12.5px; line-height: 1.45; text-align: center; }
    html[data-theme="dark"] .diagram { background: #f5f0ea; border-color: #cabfb0; }
    html[data-theme="dark"] .diagram figcaption { color: #5a4d40; }
    .exam-answer { margin: 18px 0; padding: 15px 18px; border-left: 4px solid var(--accent); border-radius: 0 12px 12px 0; background: var(--accent-2); color: var(--accent-ink); }
    .exam-answer strong { color: inherit; }
    .cmp { display: grid; gap: 12px; margin: 18px 0; }
    @media (min-width: 720px) { .cmp.two { grid-template-columns: 1fr 1fr; } }
    body.hide-code pre.code { display: none; }
    body.hide-code pre.code + p { margin-top: 0; }
  </style>
"""

MERMAID_SCRIPT = """  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({
      startOnLoad: true,
      securityLevel: 'loose',
      theme: 'base',
      themeVariables: {
        background: '#fbfaf8',
        primaryColor: '#fdecdf',
        primaryBorderColor: '#c2410c',
        primaryTextColor: '#1a130d',
        secondaryColor: '#e7ecfb',
        tertiaryColor: '#f1ece5',
        lineColor: '#8a7a6b',
        fontFamily: 'Inter, system-ui, sans-serif',
        fontSize: '15px'
      },
      flowchart: { htmlLabels: true, curve: 'basis' },
      sequence: { useMaxWidth: true }
    });
  </script>
  <script>
    (function () {
      var KEY = 'concu-hide-code';
      var btn = document.getElementById('code-toggle');
      var lbl = document.getElementById('code-toggle-label');
      function apply(hidden) {
        document.body.classList.toggle('hide-code', hidden);
        if (btn) { btn.classList.toggle('active', hidden); btn.setAttribute('aria-pressed', hidden ? 'true' : 'false'); }
        if (lbl) { lbl.textContent = hidden ? 'Código oculto' : 'Código'; }
      }
      var hidden = localStorage.getItem(KEY) === '1';
      apply(hidden);
      if (btn) btn.addEventListener('click', function () {
        hidden = !hidden;
        localStorage.setItem(KEY, hidden ? '1' : '0');
        apply(hidden);
      });
    })();
  </script>
</body>"""

# Botón que se inyecta en la barra lateral (side-actions)
CODE_TOGGLE_BUTTON = """<button class="icon-button wide" id="code-toggle" type="button" aria-pressed="false" title="Mostrar u ocultar los bloques de código">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m8 6-6 6 6 6"></path><path d="m16 6 6 6-6 6"></path></svg>
        <span id="code-toggle-label">Código</span>
      </button>"""

# Enlaces de navegación entre las dos vistas (mismo shell, distinto <main>),
# igual que aprendizaje-automatico alterna entre Apunte y Resumen.
NAV_TO_REPASO = ('<a class="icon-button wide" href="repaso-final.html" '
                 'title="Repaso compacto: el mínimo para el final">Repaso final</a>')
NAV_TO_APUNTE = ('<a class="icon-button wide" href="index.html" '
                 'title="Volver al apunte completo">Apunte</a>')


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def write(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(data)


def load_content():
    parts = sorted(glob.glob(os.path.join(HERE, 'content', 'part-*.html')))
    if not parts:
        raise SystemExit('No hay archivos content/part-*.html')
    chunks = [read(p).strip() for p in parts]
    return '\n\n'.join(chunks) + '\n'


def escape_code_blocks(markup):
    """<pre data-code="lang">raw</pre> -> <pre class=code><code>escaped</code></pre>"""
    def repl(m):
        lang = m.group(1) or 'text'
        inner = m.group(2)
        inner = inner.strip('\n')
        esc = inner.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return ('<pre class="code" data-lang="%s"><code>%s</code></pre>'
                % (lang, esc))
    return re.sub(r'<pre data-code="([^"]*)">(.*?)</pre>', repl, markup,
                  flags=re.DOTALL)


# ---------------------------------------------------------------------------
# Shell compartido: mismo armazón (índice, notas, buscador, resaltador, tema)
# para el apunte (index.html) y para el repaso final (repaso-final.html). Solo
# cambian el contenido del <main> y el enlace de navegación de la barra lateral,
# tal como aprendizaje-automatico alterna entre su Apunte y su Resumen.
# ---------------------------------------------------------------------------
def build_shell(template, content_html, toc_html, nav_link, page_title=None,
                description=None):
    doc = template

    # palette
    doc = re.sub(r':root \{[^}]*\}', ROOT_LIGHT, doc, count=1)
    doc = re.sub(r'html\[data-theme="dark"\] \{[^}]*\}', ROOT_DARK, doc, count=1)

    # head branding
    doc = doc.replace('content="#167e9e"', 'content="%s"' % ACCENT)
    desc = description or ('Guía de estudio para el final de Programación Concurrente, '
                           'FIUBA: teoría, diagramas y finales resueltos.')
    doc = re.sub(r'<meta name="description"[^>]*>',
                 '<meta name="description" content="%s">' % desc,
                 doc, count=1)
    doc = re.sub(r'<link rel="icon"[^>]*>',
                 '<link rel="icon" href="pwa-icon.svg" type="image/svg+xml">',
                 doc, count=1)
    doc = doc.replace('href="apple-touch-icon.png"', 'href="pwa-icon.svg"')

    # sidebar nav (índice)
    i = doc.index('<div class="nav-title">')
    j = doc.index('<div class="side-actions">')
    doc = doc[:i] + toc_html.strip() + '\n\n    ' + doc[j:]

    # main content
    a = doc.index('<main class="content" id="content">') + len('<main class="content" id="content">')
    b = doc.index('</main>', a)
    doc = doc[:a] + '\n' + content_html + '\n    ' + doc[b:]

    # inject styles + mermaid
    doc = doc.replace('</head>', INJECTED_STYLE + '</head>', 1)
    # insert mermaid before the LAST </body>
    head, sep, tail = doc.rpartition('</body>')
    doc = head + MERMAID_SCRIPT[:-len('</body>')] + '</body>' + tail

    # barra lateral: el link "Resumen" del template se reemplaza por el toggle de
    # código + el enlace a la otra vista (apunte <-> repaso final).
    doc = doc.replace(
        '<a class="icon-button wide" href="resumen.html">Resumen</a>',
        CODE_TOGGLE_BUTTON + '\n      ' + nav_link,
        1)

    # brand text everywhere
    doc = doc.replace('Aprendizaje Automático', 'Programación Concurrente')

    # título de la pestaña (opcional; por defecto queda el del apunte)
    if page_title:
        doc = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % page_title, doc, count=1)
    return doc


# ---------------------------------------------------------------------------
# Exportador HTML -> Markdown, con placeholders para code/mermaid
# (genera repaso-final.md, mirror portable del repaso).
# ---------------------------------------------------------------------------
class El:
    __slots__ = ('tag', 'attrs', 'children')

    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []


VOID = {'br', 'hr', 'img', 'input', 'link', 'meta'}


def parse_html(markup):
    root = El('root')
    stack = [root]
    tokens = re.findall(r'<!--[\s\S]*?-->|<![^>]*>|<[^>]+>|[^<]+', markup)
    for tok in tokens:
        if tok.startswith('<!--') or tok.startswith('<!'):
            continue
        if not tok.startswith('<'):
            stack[-1].children.append(tok)
            continue
        if tok.startswith('</'):
            m = re.match(r'</\s*([\w-]+)', tok)
            tag = m.group(1).lower() if m else ''
            while len(stack) > 1:
                node = stack.pop()
                if node.tag == tag:
                    break
            continue
        m = re.match(r'<\s*([\w-]+)', tok)
        if not m:
            continue
        name = m.group(1).lower()
        attrs = {}
        for a in re.finditer(r'([:\w-]+)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s"\'=<>`]+)))?', tok[1 + len(name):]):
            attrs[a.group(1).lower()] = htmllib.unescape(a.group(2) or a.group(3) or a.group(4) or '')
        node = El(name, attrs)
        stack[-1].children.append(node)
        if name not in VOID and not tok.endswith('/>'):
            stack.append(node)
    return root


def has_class(node, cls):
    return cls in (node.attrs.get('class', '') or '').split()


def clean(s):
    return re.sub(r'[ \t\r\n]+', ' ', s).strip()


def inline(node):
    if isinstance(node, str):
        return re.sub(r'[ \t\r\n]+', ' ', node)
    content = ''.join(inline(c) for c in node.children)
    t = node.tag
    if t in ('strong', 'b'):
        return '**%s**' % clean(content)
    if t in ('em', 'i'):
        return '*%s*' % clean(content)
    if t == 'code':
        return '`%s`' % clean(content)
    if t == 'a':
        return '[%s](%s)' % (clean(content), node.attrs.get('href', ''))
    if t == 'br':
        return '  \n'
    return content


def plain(node):
    if isinstance(node, str):
        return re.sub(r'[ \t\r\n]+', ' ', node)
    return ''.join(plain(c) for c in node.children)


def render_list(node, depth=0):
    ordered = node.tag == 'ol'
    lines = []
    n = 1
    for item in [c for c in node.children if isinstance(c, El) and c.tag == 'li']:
        nested = [c for c in item.children if isinstance(c, El) and c.tag in ('ul', 'ol')]
        primary = ''.join(inline(c) for c in item.children if c not in nested)
        marker = ('%d.' % n) if ordered else '-'
        lines.append('%s%s %s' % ('  ' * depth, marker, clean(primary)))
        for lst in nested:
            lines.append(render_list(lst, depth + 1).rstrip())
        n += 1
    return '\n'.join(lines) + '\n\n'


def render_table(node):
    rows = []
    for tr in _collect(node, 'tr'):
        cells = [clean(''.join(inline(c) for c in cell.children)).replace('|', '\\|')
                 for cell in tr.children if isinstance(cell, El) and cell.tag in ('th', 'td')]
        if cells:
            rows.append(cells)
    if not rows:
        return ''
    width = max(len(r) for r in rows)
    rows = [r + [''] * (width - len(r)) for r in rows]
    line = lambda r: '| ' + ' | '.join(r) + ' |'
    out = [line(rows[0]), line(['---'] * width)] + [line(r) for r in rows[1:]]
    return '\n'.join(out) + '\n\n'


def _collect(node, tag):
    found = []
    def rec(n):
        if isinstance(n, El):
            if n.tag == tag:
                found.append(n)
            else:
                for c in n.children:
                    rec(c)
    rec(node)
    return found


def render_children(node):
    return ''.join(render_block(c) for c in node.children)


def render_block(node):
    if isinstance(node, str):
        return (clean(node) + '\n\n') if node.strip() else ''
    t = node.tag
    if t == 'section':
        return render_section(node)
    if t == 'h1':
        return '# %s\n\n' % clean(plain(node))
    if t == 'h2':
        return '## %s\n\n' % clean(plain(node))
    if t == 'h3':
        return '### %s\n\n' % clean(plain(node))
    if t == 'h4':
        return '#### %s\n\n' % clean(plain(node))
    if t == 'p':
        return '%s\n\n' % clean(''.join(inline(c) for c in node.children))
    if t in ('ul', 'ol'):
        return render_list(node)
    if t == 'table':
        return render_table(node)
    if t == 'pre':
        ph = node.attrs.get('data-ph')
        if ph is not None:
            lang, code = PLACEHOLDERS[int(ph)]
            return '```%s\n%s\n```\n\n' % (lang, code)
        return '```\n%s\n```\n\n' % plain(node)
    if t == 'summary':
        return '**%s**\n\n' % clean(plain(node))
    if t in ('header', 'main', 'div', 'figure', 'details'):
        if t == 'div' and node.attrs.get('data-ph') is not None:
            code = PLACEHOLDERS[int(node.attrs['data-ph'])][1]
            return '```mermaid\n%s\n```\n\n' % code
        if t == 'figure' and has_class(node, 'diagram'):
            body = render_children(node)
            cap = _collect(node, 'figcaption')
            caption = ('*%s*\n\n' % clean(plain(cap[0]))) if cap else ''
            return body + caption
        if has_class(node, 'chapter-number') or has_class(node, 'chapter-head'):
            # chapter-head handled in render_section; standalone -> skip number
            if has_class(node, 'chapter-number'):
                return ''
        return render_children(node)
    if t == 'figcaption':
        return ''
    return render_children(node)


def render_section(node):
    md = ('<a id="%s"></a>\n\n' % node.attrs['id']) if node.attrs.get('id') else ''
    for child in node.children:
        if isinstance(child, El) and has_class(child, 'chapter-head'):
            num = _collect(child, None)
            number_node = _first(child, lambda n: has_class(n, 'chapter-number'))
            heading = _first(child, lambda n: n.tag == 'h2')
            number = clean(plain(number_node)) if number_node else ''
            title = clean(plain(heading)) if heading else ''
            md += '## %s. %s\n\n' % (number, title)
        else:
            md += render_block(child)
    return md


def _first(node, pred):
    if isinstance(node, El) and pred(node):
        return node
    if isinstance(node, El):
        for c in node.children:
            r = _first(c, pred)
            if r:
                return r
    return None


PLACEHOLDERS = []


def build_markdown(raw_content):
    """raw_content has <pre data-code> and <div class=mermaid>. Swap for placeholders
    so the naive parser never sees '<' inside code/diagrams."""
    global PLACEHOLDERS
    PLACEHOLDERS = []

    def stash_pre(m):
        lang = m.group(1) or 'text'
        PLACEHOLDERS.append((lang, m.group(2).strip('\n')))
        return '<pre data-ph="%d"></pre>' % (len(PLACEHOLDERS) - 1)

    def stash_mermaid(m):
        PLACEHOLDERS.append(('mermaid', m.group(1).strip('\n')))
        return '<div data-ph="%d"></div>' % (len(PLACEHOLDERS) - 1)

    tmp = re.sub(r'<pre data-code="([^"]*)">(.*?)</pre>', stash_pre, raw_content, flags=re.DOTALL)
    tmp = re.sub(r'<div class="mermaid">(.*?)</div>', stash_mermaid, tmp, flags=re.DOTALL)

    root = parse_html(tmp)
    main = El('main')
    main.children = root.children
    md = render_block(main)
    md = re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'
    # The hero <h1> already renders the title; insert the "Abrir apunte" link
    # right after it instead of prepending a duplicate H1.
    first_nl = md.find('\n')
    if md.startswith('# ') and first_nl != -1:
        md = md[:first_nl] + '\n\n[Abrir apunte](index.html)\n' + md[first_nl:]
    return md


# ---------------------------------------------------------------------------
def main():
    template = read(TEMPLATE)
    raw_content = load_content()
    toc_html = read(os.path.join(HERE, 'toc.html'))
    toc_repaso = read(os.path.join(HERE, 'toc-repaso.html'))

    content_html = escape_code_blocks(raw_content)
    raw_repaso = read(os.path.join(HERE, 'content', 'repaso-final.html'))
    repaso_content = escape_code_blocks(raw_repaso)

    # Apunte completo (index.html): índice del apunte, enlace de barra lateral -> Repaso final.
    index = build_shell(template, content_html, toc_html, NAV_TO_REPASO)
    write(os.path.join(HERE, 'index.html'), index)

    # Repaso final (repaso-final.html): MISMO shell, con su PROPIO índice (anclas
    # in-page a las secciones del repaso, para que buscador y navegación funcionen)
    # y enlace de barra lateral -> Apunte.
    repaso = build_shell(template, repaso_content, toc_repaso, NAV_TO_APUNTE,
                         page_title='Repaso final | Programación Concurrente',
                         description='Repaso final de Programación Concurrente, FIUBA: '
                                     'el mínimo teórico para aprobar un final.')
    write(os.path.join(HERE, 'repaso-final.html'), repaso)

    # Mirror portable en Markdown del repaso.
    write(os.path.join(HERE, 'repaso-final.md'), build_markdown(raw_repaso))

    words = len(re.sub(r'<[^>]+>', ' ', content_html).split())
    rwords = len(re.sub(r'<[^>]+>', ' ', raw_repaso).split())
    print('OK  index.html + repaso-final.html + repaso-final.md')
    print('    ~%d palabras de apunte, ~%d palabras de repaso final' % (words, rwords))


if __name__ == '__main__':
    main()
