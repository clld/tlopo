<%inherit file="tlopo.mako"/>
<%namespace name="util" file="util.mako"/>
<%namespace name="lib" file="lib.mako"/>

<%! active_menu_item = "languages" %>
<%block name="title">Phylogeny</%block>

<%def name="sidebar()">
    <%util:well>
        ${u.markdown(req.dataset.jsondata['tree_description'])|n}
    </%util:well>
</%def>

${lib.languages_contextnav()}

<h2>Phylogeny</h2>

${tree|n}
