<%inherit file="../snippet.mako"/>
<%namespace name="util" file="../util.mako"/>

% if ctx.description:
<p>
    ${ctx.description}
</p>
% endif

<table>
    % for vs in sorted(ctx.valuesets, key=lambda vs: (vs.language.group, vs.language.name)):
        % for v in vs.values:
        <tr>
            <td>${vs.language.group}</td>
            <td>${h.link(req, vs.language)}</td>
            <td>${v.name}</td>
            <td>${v.description}</td>
        </tr>
        % endfor
    % endfor
</table>
