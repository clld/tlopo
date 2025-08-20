<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${ctx.name}</%block>

<h2>${title()}</h2>

% if ctx.description:
<p>${ctx.description}</p>
% endif

<div class="row-fluid">
<div class="span8">
    ${(map_ or request.map).render()}
</div>
<div class="span4" style="margin-top: 1em;">
    ${tree|n}
</div>
</div>
