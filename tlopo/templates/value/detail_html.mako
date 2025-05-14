<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>${_('Value')} ${ctx.domainelement.name if ctx.domainelement else ctx.name}</h2>

<dl>
    <dt>Language:</dt>
    <dd>${h.link(request, ctx.valueset.language)}</dd>
    <dt>${_('Parameter')}:</dt>
    <dd>${h.link(request, ctx.valueset.parameter)}</dd>
    % if ctx.references:
    <dt>References</dt>
    <dd>${h.linked_references(request, ctx)|n}</dd>
    % endif
    % for k, v in ctx.datadict().items():
    <dt>${k}</dt>
    <dd>${v}</dd>
    % endfor
</dl>
