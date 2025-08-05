<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "taxons" %>
<%block name="title">Taxon <i>${ctx.name}</i></%block>

<h2>
    ${title()}
    <a class="gbif" title="${ctx.name} at GBIF" href="https://gbif.org/species/${ctx.id}"><img src="${req.static_url('tlopo:static/gbif.jpeg')}"></a>
</h2>


% if ctx.description:
<p>${ctx.description}</p>
% endif

<h3>Referenced in</h3>
<ul>
    % for ca in ctx.chapter_assocs:
    <li>
        Chapter ${h.link(req, ca.chapter)|n}
        % if ca.section:
        section ${h.link(req, ca.chapter, label=ca.section, url_kw=dict(_anchor=ca.fragment))|n}
        % endif
    </li>
    % endfor
</ul>

<h3>Names</h3>

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${req.get_datatable('units', h.models.Unit, taxon=ctx).render()}


<%block name="javascript">
var taxa = ${u.json.dumps({ctx.name: ctx.id})|n};
</%block>
