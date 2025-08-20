
<%def name="languages_contextnav()">
    <ul class="nav nav-tabs">
        <li class="${'active' if request.matched_route.name == 'languages' else ''}">
            <a href="${request.route_url('languages')}">Browse</a>
        </li>
        <li class="${'active' if request.matched_route.name == 'phylogeny' else ''}">
            <a href="${request.route_url('phylogeny')}">Phylogeny</a>
        </li>
        <li class="${'active' if request.matched_route.name == 'regions' else ''}">
            <a href="${request.route_url('regions')}">Regions</a>
        </li>
    </ul>
</%def>
