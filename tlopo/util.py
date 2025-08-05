import re
import html
import json
import pathlib

from markdown import markdown

from clld.web.util.helpers import link
from clld.db.models import common
from clld.db.meta import DBSession

assert json and markdown and link


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

    #
    # FIXME: add links from text to cognatesets!
    # look for table class="cognateset" id="..."
    # button(icon('map-marker'), href="", title="")
    #
    return {'text': pattern.sub(cs_link, ref_pattern.sub(repl, text))}
