<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%namespace name="lib" file="../lib.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Regions</%block>

${lib.languages_contextnav()}

<h2>${title()}</h2>
<div>
    ${(map_ or request.map).render()}
</div>

<%block name="javascript">
var bboxes = ${geojson|n};
</%block>
