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
            % if vs.language.is_proto:
            <td colspan="2">${h.link(req, vs.language)}</td>
            % else:
            <td>${vs.language.group}</td>
            <td>${h.link(req, vs.language)}</td>
            % endif
            <td class="form${' proto' if vs.language.is_proto else ''}">${v.word.name}</td>
            <td class="gloss">${v.word.description}</td>
        </tr>
        % endfor
    % endfor
</table>
