<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>

<h2>${ctx.name}</h2>
${ctx.coins(request)|n}

<div class="alert alert-info">${ctx.bibtex().text()}</div>

<h3>Links</h3>
${u.src_links(req, ctx)|n}

<h3>References</h3>

% for cid, sections in ctx.grouped_sections:
    % if loop.first:
<h4>Sections</h4>
<ul>
    % endif
    <li>${chapters[cid].name}
        <ul>
        % for sid, title in sections:
            <li><a href="${req.route_url('contribution', id=cid, _anchor=sid)}">${u.md(title)|n}</a></li>
        % endfor
        </ul>
    </li>
    % if loop.last:
</ul>
    % endif
% endfor

% for word in words:
% if loop.first:
<h4>Words</h4>
<ul>
    % endif
    <li>${h.link(req, word.language)}: <i>${h.link(req, word)}</i>
        % for hg in word.unitvalues:
        ${u.gloss(hg.unitparameter.name)|n}
        % endfor
    </li>
    % if loop.last:
</ul>
% endif
% endfor

<%def name="sidebar()">
<div class="well">
<h4>BibTeX</h4>
<pre>${ctx.bibtex()}</pre>
</div>
</%def>
