from pyramid.view import view_config
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link
from clld.db.meta import DBSession
from clld.db.models.common import Language


@view_config(route_name='phylogeny', renderer='phylogeny.mako')
def phylogeny(req):
    from newick import loads
    tree = loads(req.dataset.jsondata['tree'])[0]
    langs = {l.id: l for l in DBSession.query(Language).filter(Language.id.in_(tree.get_leaf_names()))}

    def html(node):
        content = [link(req, langs[node.name]) if node.name in langs else HTML.strong(node.comment)]
        descendants = sorted(node.descendants, key=lambda n: (n.name not in langs, n.name or ''))
        if descendants:
            content.append(HTML.ul(*[html(n) for n in descendants], style="margin-left: 2em;", class_='unstyled'))
        return HTML.li(*content)

    return {'tree': HTML.ul(html(tree), class_='unstyled')}
