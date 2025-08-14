<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Volumes</h3>
        <ol>
            % for chap in volumes:
            <li><a href="${req.route_url('contribution', id=chap.id)}">${chap.volume}</a></li>
            % endfor
        </ol>
    </div>
</%def>

<h2>Welcome to Lexicon of Proto Oceanic</h2>

<p class="lead">
    The lexicon of Proto Oceanic is a series of six volumes reconstructing the lexicon of Proto Oceanic,
    the language ancestral to most of the Austornesian languages of Melanesia, Polynesia and Micronesia.
    Each volume presents a series of essays that draw on the features identified by the reconstructions
    to describe the way of life and environment of Proto Oceanic speakers, using relevant background
    material including archaeological, ethnographic and bio-geographical information. The volumes are
    intended to serve as a resource for linguists, culture historians, archaeologists and others interested
    in the prehistory of the Pacific region.
</p>
