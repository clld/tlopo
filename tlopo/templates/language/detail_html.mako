<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${'Protolanguage' if ctx.is_proto else 'Language'} ${ctx.name}</h2>

${request.get_datatable('units', h.models.Unit, language=ctx).render()}

<%block name="javascript">
var lids = ${u.json.dumps([ctx.id])|n};
</%block>

<%def name="sidebar()">
<div class="well well-small">
    <dl class="dl-horizontal">
        % if ctx.glottocode:
        <dt>Glottolog:</dt><dd>${u.glottolog.link(req, ctx.glottocode, label=ctx.glottolog_name)}</dd>
        % endif
        % if ctx.description:
        <dt>Name:</dt><dd>${ctx.description}</dd>
        % endif
        % if ctx.alternative_names:
        <dt>Other names:</dt><dd>${ctx.alternative_names}</dd>
        % endif
    </dl>
</div>
        % if ctx.longitude:
        % if ctx.region:
        ${request.get_map('region').render()}
        % else:
        ${request.map.render()}
        % endif
        % endif
        % if tree:
<div class="well well-small">
        ${tree|n}
</div>
        % endif
        % if ctx.sources:
<div class="well well-small">
            <ul>
                % for source in lang.sources:
                <li>${h.link(request, source, label=source.description)}<br />
                <small>${h.link(request, source)}</small></li>
                % endfor
            </ul>
    </div>
% endif
</%def>
