<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>

<h2>${ctx.name}</h2>
${ctx.coins(request)|n}

<div class="alert alert-info">${ctx.bibtex().text()}</div>

<h3>Links</h3>
${u.src_links(req, ctx)|n}

<h3>References</h3>
<ul>
    % for cid, sections in ctx.grouped_sections:
    <li>${chapters[cid].name}
        <ul>
        % for sid, title in sections:
            <li><a href="${req.route_url('contribution', id=cid, _anchor=sid)}">${u.md(title)|n}</a></li>
        % endfor
        </ul>
    </li>
    % endfor
</ul>

<%def name="sidebar()">
<div class="well">
<h4>BibTeX</h4>
<pre>${ctx.bibtex()}</pre>
</div>
</%def>
