<%inherit file="../snippet.mako"/>
<%namespace name="util" file="../util.mako"/>

% if ctx.description:
<p>
    ${ctx.description}
</p>
% endif

<table>
    % for vs in ctx.valuesets:
        % for v in vs.values:
        <tr>
            <td>${h.link(req, vs.language)}</td>
            <td>${v.name}</td>
            <td>${v.description}</td>
        </tr>
        % endfor
    % endfor
</table>
