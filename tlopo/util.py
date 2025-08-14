import re
import html
import json
import pathlib
import urllib.parse

from markdown import markdown

from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML
from clld.db.models import common
from clld.db.meta import DBSession

assert json and markdown and link


def src_links(req, src):
    def li(url):
        purl = urllib.parse.urlparse(url)
        icon, text = {
            'doi.org': ('DOI_logo.svg', ''),
            'www.jstor.org': ('JSTOR-wr-icon.png', 'Copy in JSTOR'),
            'archive.org': ('ia_logo.png', 'Copy in the Internet Archive'),
            'hdl.handle.net': ('handle_logo.png', ''),
            'sealang.net': ('sealang_logo.png', 'Copy at SEALANG'),
            'catalog.hathitrust.org': ('hathitrust_logo.png', 'Catalog record at HathiTrust'),
            'babel.hathitrust.org': ('hathitrust_logo.png', 'Catalog record at HathiTrust'),
            'www.sil.org': ('sil_logo.png', 'Resource at SIL'),
            'openresearch-repository.anu.edu.au': ('anu_logo.png', "Record in ANU's repository"),
        }.get(purl.netloc, (None, None))
        if icon:
            if purl.netloc == 'doi.org':
                text = src.doi
            elif purl.netloc == 'hdl.handle.net':
                text = purl.path[1:]
            return HTML.li(HTML.a(
                HTML.img(height="20", width="20", src=req.static_url('tlopo:static/' + icon)),
                ' ',
                text,
                href=url))
        return HTML.li(HTML.a(url, href=url))

    links = [li(u) for u in (src.url or '').split()]
    return HTML.ul(*links, **{'class': 'unstyled'})

def source_detail_html(context=None, request=None, **kw):
    return {'chapters': {c.id: c for c in DBSession.query(common.Contribution)}}


def contribution_detail_html(context=None, request=None, **kw):
    ref_pattern = re.compile(r'<a[\s\n]+href="\.\./sources/(?P<key>[^"]+)">(?P<label>[^<]+)</a>')
    ref_tooltips = {}
    for src in DBSession.query(common.Source):
        ref_tooltips[src.id] = html.escape('{}. {}'.format(src.name, src.description))

    def repl(m):
        # add tooltips to refs:
        # <a href="#" data-toggle="tooltip" title="first tooltip">hover over me</a>
        assert m.group('key') in ref_tooltips
        return '<a title="{}" href="../sources/{}">{}</a>'.format(
                ref_tooltips[m.group('key')],
                m.group('key'),
                m.group('label'))
        #else:
        #    print(m.string[m.start():m.end()])
        #return m.string[m.start():m.end()]

    vol, _, ch = context.id.partition('-')
    text = context.description.split('<!--start-->')[1].split('</body>')[0]

    pattern = re.compile(r'<table class="cognateset" id="(?P<id>[^"]+)">')

    def cs_link(m):
        return '\n'.join([
            '<div style="float: right;"><a '
            'title="View cognateset on a map" '
            'class="btn btn-info" href="../parameters/{}">'
            '<i class="icon-map-marker icon-white"></i></a></div>'.format(m.group('id')),
            m.string[m.start():m.end()]])

    def add_toplink(text):
        return re.sub(
            r'</h[2-4]>',
            lambda m:  """<a href="#top" title="${_('go to top of the page')}" style="vertical-align: bottom">&#x21eb;</a>""" + m.string[m.start():m.end()],
            text)

    #
    # FIXME: add links from text to cognatesets!
    # look for table class="cognateset" id="..."
    # button(icon('map-marker'), href="", title="")
    #
    return {
        'refs': DBSession.query(common.Source).filter(common.Source.id.in_(context.jsondata['refs'])).order_by(common.Source.name).all(),
        'text': add_toplink(pattern.sub(cs_link, ref_pattern.sub(repl, text)))}
