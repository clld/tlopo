<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "units" %>

<p style="padding-top: 1em; padding-bottom: 1em">
<strong style="font-size: x-large">${h.link(req, ctx.language)} <i>${'*' if ctx.language.is_proto else ''}${ctx.name}</i></strong>
</p>

<ul>
% for cog in ctx.cognates:
    <li>
Referenced in a <a href="${req.route_url('parameter', id=cog.valueset.parameter.id)}">cognateset</a>
in chapter ${h.link(req, cog.valueset.parameter.chapter, url_kw=dict(_anchor=cog.valueset.parameter.fragment))} with glosses
% for ga in ctx.unitvalues:
    % if ga.unitparameter.id in cog.jsondata['glosses']:
% if ga.pos:
[${ga.pos}]
% endif
${h.link(request, ga.unitparameter)}

    % endif
% endfor
    </li>
% endfor
</ul>

<h3>Glosses</h3>
<ul>
    % for value in ctx.unitvalues:
    <li>
        % if value.pos:
            [${value.pos}]
        % endif
        ${h.link(request, value.unitparameter)}
    </li>
    % endfor
</ul>

<h3>References</h3>
<ul>
% for ref in ctx.chapter_assocs:
    <li>
        ${h.link(request, ref.chapter, url_kw=dict(_anchor=ref.fragment))}
        <ul>
            % for gloss in ctx.unitvalues:
                % if gloss.id in ref.gloss_ids.split():
            <li>
                % if gloss.pos:
                [${gloss.pos}]
                % endif
                ${h.link(request, gloss.unitparameter)}
            </li>
                % endif
            % endfor
        </ul>
    </li>
% endfor
</ul>