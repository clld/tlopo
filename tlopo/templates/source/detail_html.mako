<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>

<h2>${ctx.name}</h2>
${ctx.coins(request)|n}

<% bibrec = ctx.bibtex() %>
<p>${bibrec.text()}</p>

<h3>Links</h3>
${u.src_links(req, ctx)|n}

<h3>References</h3>
<ul>
    % for cid, sections in ctx.grouped_sections:
    <li>${chapters[cid].name}
        <ul>
        % for sid, title in sections:
            <li><a href="${req.route_url('contribution', id=cid, _anchor=sid)}">${title}</a></li>
        % endfor
        </ul>
    </li>
    % endfor
</ul>

<h3>BibTeX</h3>
<pre>${bibrec}</pre>

<%def name="sidebar()">
    <% referents, one_open = context.get('referents', {}), False %>
    <div class="accordion" id="sidebar-accordion">
    % if referents.get('language'):
        <%util:accordion_group eid="acc-l" parent="sidebar-accordion" title="${_('Languages')}" open="${not one_open}">
            ${util.stacked_links(referents['language'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    % if referents.get('contribution'):
        <%util:accordion_group eid="acc-c" parent="sidebar-accordion" title="${_('Contributions')}" open="${not one_open}">
            ${util.stacked_links(referents['contribution'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    % if referents.get('valueset'):
        <%util:accordion_group eid="acc-v" parent="sidebar-accordion" title="${_('ValueSets')}" open="${not one_open}">
            ${util.stacked_links(referents['valueset'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    % if referents.get('sentence'):
        <%util:accordion_group eid="acc-s" parent="sidebar-accordion" title="${_('Sentences')}" open="${not one_open}">
            ${util.stacked_links(referents['sentence'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    </div>
</%def>
