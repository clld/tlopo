<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>


<h2>${u.markdown(ctx.name)|n}</h2>

<p>
Presented in chapter ${h.link(req, ctx.chapter, url_kw=dict(_anchor=ctx.fragment))}.
</p>

% if ctx.note:
<blockquote>${ctx.note}</blockquote>
% endif

% if ctx.description:
<p>${ctx.description}</p>
% endif

<div style="clear: both"/>
% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}

<%block name="javascript">
% if ctx.taxon_assocs:
    var taxa = ${u.json.dumps({t.taxon.name: t.taxon.id for t in ctx.taxon_assocs})|n};
% endif
</%block>
