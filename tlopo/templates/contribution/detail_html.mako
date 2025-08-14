<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%block name="head">
<style>
body {
  color: #222;
  font-family: Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif;
  font-size: 13px;
  line-height: 1.7;
  background: #fefefe;
}

a {
  color: #0645ad;
  text-decoration: none;
}

a:visited {
  color: #0b0080;
}

a:hover {
  color: #06e;
}

a:active {
  color: #faa700;
}

a:focus {
  outline: thin dotted;
}

*::-moz-selection {
  background: rgba(255, 255, 0, 0.3);
  color: #000;
}

*::selection {
  background: rgba(255, 255, 0, 0.3);
  color: #000;
}

a::-moz-selection {
  background: rgba(255, 255, 0, 0.3);
  color: #0645ad;
}

a::selection {
  background: rgba(255, 255, 0, 0.3);
  color: #0645ad;
}

p {
  margin: 1em 0;
}

img {
  max-width: 100%;
}

h1, h2, h3, h4, h5, h6 {
  color: #111;
  line-height: 125%;
  margin-top: 2em;
  font-weight: normal;
}

h4, h5, h6 {
  font-weight: bold;
}

h1 {
  font-size: 2.5em;
}

h2 {
  font-size: 2em;
}

h3 {
  font-size: 1.5em;
}

h4 {
  font-size: 1.2em;
}

h5 {
  font-size: 1em;
}

h6 {
  font-size: 0.9em;
}

blockquote {
  color: #444;
  margin: 0;
  padding-left: 3em;
  border-left: 0.5em #EEE solid;
}

hr {
  display: block;
  height: 2px;
  border: 0;
  border-top: 1px solid #aaa;
  border-bottom: 1px solid #eee;
  margin: 1em 0;
  padding: 0;
}

pre, code, kbd, samp {
  color: #000;
  font-family: monospace, monospace;
  _font-family: 'courier new', monospace;
  font-size: 0.98em;
}

pre {
  white-space: pre;
  white-space: pre-wrap;
  word-wrap: break-word;
}

b, strong {
  font-weight: bold;
}

dfn {
  font-style: italic;
}

ins {
  background: #ff9;
  color: #000;
  text-decoration: none;
}

mark {
  background: #ff0;
  color: #000;
  font-style: italic;
  font-weight: bold;
}

sub, sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}

sup {
  top: -0.5em;
}

sub {
  bottom: -0.25em;
}

ul, ol {
  margin: 1em 0;
  padding: 0 0 0 2em;
}

li p:last-child {
  margin-bottom: 0;
}

ul ul, ol ol {
  margin: .3em 0;
}

dl {
  margin-bottom: 1em;
}

dt {
  font-weight: bold;
  margin-bottom: .3em;
}

dd {
  margin: 0 0 .8em 2em;
}

dd:last-child {
  margin-bottom: 0;
}

img {
  border: 0;
  -ms-interpolation-mode: bicubic;
  vertical-align: middle;
}

span.sideways {writing-mode: sideways-lr;}
span.downwards {writing-mode: vertical-rl;}
th:has(> span.downwards) {vertical-align: top;}
span.sc {font-variant: small-caps;}

figure {
  display: block;
  text-align: center;
  margin: 1em 0;
}

figure img {
  border: none;
  margin: 0 auto;
}

figcaption {
  font-size: 100%;
  margin: 0 0 .8em;
}

table {
  margin-bottom: 2em;
  border-bottom: 1px solid #ddd;
  border-right: 1px solid #ddd;
  border-spacing: 0;
  border-collapse: collapse;
}

table th {
  padding: .2em 1em;
  background-color: #eee;
  border-top: 1px solid #ddd;
  border-left: 1px solid #ddd;
}

table td {
  padding: .2em 1em;
  border-top: 1px solid #ddd;
  border-left: 1px solid #ddd;
  vertical-align: top;
}

.author {
  font-size: 1.2em;
  text-align: center;
}

@media only screen and (min-width: 480px) {
  body {
    font-size: 14px;
  }
}
@media only screen and (min-width: 768px) {
  body {
    font-size: 16px;
  }
}
@media print {
  * {
    background: transparent !important;
    color: black !important;
    filter: none !important;
    -ms-filter: none !important;
  }

  body {
    font-size: 12pt;
    max-width: 100%;
  }

  a, a:visited {
    text-decoration: underline;
  }

  hr {
    height: 1px;
    border: 0;
    border-bottom: 1px solid black;
  }

  a[href]:after {
    content: " (" attr(href) ")";
  }

  abbr[title]:after {
    content: " (" attr(title) ")";
  }

  .ir a:after, a[href^="javascript:"]:after, a[href^="#"]:after {
    content: "";
  }

  pre, blockquote {
    border: 1px solid #999;
    padding-right: 1em;
    page-break-inside: avoid;
  }

  tr, img {
    page-break-inside: avoid;
  }

  img {
    max-width: 100% !important;
  }

  @page :left {
    margin: 15mm 20mm 15mm 10mm;
}

  @page :right {
    margin: 15mm 10mm 15mm 20mm;
}

  p, h2, h3 {
    orphans: 3;
    widows: 3;
  }

  h2, h3 {
    page-break-after: avoid;
  }
}

td.bggray {background-color: lightgray}
td.bgred {background-color: pink}
td.bggreen {background-color: palegreen}
td.bgblue {background-color: powderblue}
table.multispan td {text-align: center; vertical-align: center}
table.igt {
  border-collapse: collapse !important;
  border: none;
}
table.igt td {
  border: none;
  padding-top: 0.1em;
  padding-bottom: 0.1em;
  padding-left: 0;
  padding-right: 1em;
  white-space: nowrap;
}
table.labeled caption {
  padding-left: 2em;
}
table.igt caption {
  caption-side: bottom;
  text-align: left;
}
span.smallcaps {font-variant: all-small-caps}
    </style>
</%block>

<h2>${_('Contribution')} ${ctx.name}</h2>

% for co in ctx.primary_contributors:
    ${h.link(req, co)}
    % if not loop.last:
        and
    % endif
% endfor

${text|n}

<%def name="sidebar()">
    <div class="accordion" id="sidebar-accordion">
        <%util:accordion_group eid="acc-map" parent="sidebar-accordion" title="${_('Contents')}" open="${True}">
        <div class="alert alert-info">The lexicon of Proto Oceanic: ${ctx.volume_num} ${ctx.volume}</div>
        % if ctx.prev:
        <a title="${ctx.prev.name}" href="${req.route_url('contribution', id=ctx.prev.id)}"><i class="icon-step-backward"></i></a>
        % endif
        ${_('Contribution')} ${ctx.name}
        % if ctx.next:
        <a title="${ctx.next.name}" href="${req.route_url('contribution', id=ctx.next.id)}"><i class="icon-step-forward"></i></a>
        % endif

        ${ctx.toc()|n}
        </%util:accordion_group>
        <%util:accordion_group eid="cogsets" parent="sidebar-accordion" title="${_('Cognatesets')}">
        <ul>
            % for cs in ctx.cognatesets:
            <li class="refs"><a href="#${cs.fragment}">${u.md(cs.name)|n}</a></li>
            % endfor
        </ul>
        </%util:accordion_group>
        <%util:accordion_group eid="sources" parent="sidebar-accordion" title="${_('References')}">
        <ul>
            % for ref in refs:
            <li class="refs">${h.link(req, ref)} “${ref.description}”</li>
            % endfor
        </ul>
        </%util:accordion_group>
    </div>
</%def>
