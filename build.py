#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensambla la PWA de Programación Concurrente. Es AUTOCONTENIDO: el armazón
(CSS/JS del buscador, notas, resaltador, modo oscuro y service worker) vive en
template.html, que ya trae la marca, la paleta, los estilos y los scripts
horneados y expone cinco puntos de inyección:

  <!--PAGE-TITLE-->   título de la pestaña
  <!--DESCRIPTION-->  meta description
  <!--TOC-->          índice de la barra lateral
  <!--NAV-LINK-->     enlace a la otra vista (Repaso final <-> Apunte)
  <!--CONTENT-->      contenido del <main>

build.py solo rellena esos huecos. Genera:
  - index.html         (apunte completo)
  - repaso-final.html  (repaso compacto; mismo shell, otro <main> e índice)
  - repaso-final.md    (mirror en Markdown del repaso, portable)

El contenido se escribe UNA sola vez en content/part-*.html (+ content/repaso-final.html).
Los bloques de código van como <pre data-code="rust">...</pre> (se escapan solos).
Los diagramas van como <div class="mermaid">...</div> (evitar '<' literal adentro).
"""
import os
import re
import glob
import html as htmllib

HERE = os.path.dirname(os.path.abspath(__file__))
# Armazón autocontenido del proyecto (shell con placeholders). Ver docstring.
TEMPLATE = os.path.join(HERE, 'template.html')

# Enlaces de navegación entre las dos vistas (mismo shell, distinto <main>):
# el apunte apunta al repaso y el repaso al apunte.
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
# Rellena el shell: el MISMO template.html para las dos vistas; solo cambian los
# cinco placeholders. Es str.replace literal (sin regex ni marcadores heredados);
# cada placeholder aparece una única vez en el template.
# ---------------------------------------------------------------------------
PLACEHOLDER_TOKENS = ('<!--PAGE-TITLE-->', '<!--DESCRIPTION-->', '<!--TOC-->',
                      '<!--NAV-LINK-->', '<!--CONTENT-->')


def build_page(template, content_html, toc_html, nav_link, page_title, description):
    for token in PLACEHOLDER_TOKENS:
        if token not in template:
            raise SystemExit('template.html no tiene el placeholder %s' % token)
    return (template
            .replace('<!--PAGE-TITLE-->', page_title, 1)
            .replace('<!--DESCRIPTION-->', description, 1)
            .replace('<!--TOC-->', toc_html.strip(), 1)
            .replace('<!--NAV-LINK-->', nav_link, 1)
            .replace('<!--CONTENT-->', content_html, 1))


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
    index = build_page(template, content_html, toc_html, NAV_TO_REPASO,
                       page_title='Programación Concurrente | Final FIUBA',
                       description='Guía de estudio para el final de Programación '
                                   'Concurrente, FIUBA: teoría, diagramas y finales resueltos.')
    write(os.path.join(HERE, 'index.html'), index)

    # Repaso final (repaso-final.html): MISMO shell, con su PROPIO índice (anclas
    # in-page a las secciones del repaso, para que buscador y navegación funcionen)
    # y enlace de barra lateral -> Apunte.
    repaso = build_page(template, repaso_content, toc_repaso, NAV_TO_APUNTE,
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
