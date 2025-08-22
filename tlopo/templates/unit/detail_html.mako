<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "units" %>

<p style="padding-top: 1em; padding-bottom: 1em">
<strong style="font-size: x-large">${h.link(req, ctx.language)} <i>${'*' if ctx.language.is_proto else ''}${ctx.name}</i></strong>
</p>

<h3>Glosses</h3>
<ul>
    % for value in ctx.unitvalues:
    <li>
        % if value.pos:
            [${value.pos}]
        % endif
        <a href="${req.resource_url(value.unitparameter)}">${u.gloss(value.unitparameter.name)|n}</a>
    </li>
    % endfor
</ul>

<h3>References</h3>

% for cog in ctx.cognates:
        % if loop.first:
<h4>Cognatesets</h4>
<ul>
        % endif
    <li>
        <a href="${req.resource_url(cog.valueset.parameter)}">${u.md(cog.valueset.parameter.name)|n}</a>
        with glosses
        % for ga in ctx.unitvalues:
        % if ga.unitparameter.id in cog.jsondata['glosses']:
        % if ga.pos:
        [${ga.pos}]
        % endif
        <a href="${req.resource_url(ga.unitparameter)}">${u.gloss(ga.unitparameter.name)|n}</a>
        % endif
        % endfor
    </li>
    % if loop.last:
</ul>
    % endif
% endfor


% for ref in ctx.chapter_assocs:
    % if loop.first:
<h4>Sections</h4>
<ul>
    % endif
    <li>
        ${h.link(request, ref.chapter, url_kw=dict(_anchor=ref.fragment))}
        <ul>
            % for gloss in ctx.unitvalues:
                % if gloss.id in ref.gloss_ids.split():
            <li>
                % if gloss.pos:
                [${gloss.pos}]
                % endif
                <a href="${req.resource_url(gloss.unitparameter)}">${u.gloss(gloss.unitparameter.name)|n}</a>
            </li>
                % endif
            % endfor
        </ul>
    </li>
    % if loop.last:
</ul>
    % endif
% endfor