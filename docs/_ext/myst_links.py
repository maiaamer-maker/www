"""
Fixes ``&`` in the URLs of Markdown links.

MyST HTML-escapes link URLs when it parses them, and Sphinx's HTML writer
escapes them again, so ``?v=abc&list=xyz`` reaches the browser as
``?v=abc&amp;list=xyz`` and the second parameter is lost. Undoing MyST's
escaping on Markdown pages leaves the writer's as the only one.
"""

import html

from docutils import nodes


def unescape_link_urls(app, doctree):
    if not app.env.doc2path(app.env.docname).suffix == '.md':
        return
    for ref in doctree.findall(nodes.reference):
        if '&' in ref.get('refuri', ''):
            ref['refuri'] = html.unescape(ref['refuri'])


def setup(app):
    app.connect('doctree-read', unescape_link_urls)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
