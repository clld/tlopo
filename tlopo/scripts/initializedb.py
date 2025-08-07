import itertools
import collections

from csvw.dsv import reader
from pycldf import Sources
from clldutils.misc import slug
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex

from nameparser import HumanName

import tlopo
from tlopo import models


NON_OCEANIC = "WMP CMP Fma IJ NA".split()


def main(args):
    from pytlopo.util import variants

    data = Data()
    ds = data.add(
        common.Dataset,
        'tlopo',
        id='tlopo',
        domain='',
        name="The lexicon of Proto Oceanic",
        description="The lexicon of Proto Oceanic: The culture and environment of ancestral Oceanic society",
        publisher_name="MPI EVA",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de/",
        license="http://creativecommons.org/licenses/by/4.0/",
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'},

    )
    editors, seen, contribs = ['rossm', 'pawleya', 'osmondm'], set(), collections.defaultdict(list)
    for chapter in args.cldf.iter_rows('ContributionTable'):
        for name in chapter['Contributor'].split(' and '):
            cid = HumanName(name.strip()).last.lower() + HumanName(name.strip()).first.lower()[0]
            if cid not in seen:
                co = data.add(common.Contributor, cid, id=cid, name=name.strip())
                if cid in editors:
                    common.Editor(dataset=ds, ord=editors.index(cid), contributor=co)
                seen.add(cid)
            contribs[chapter['ID']].append(cid)

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    langs = {gr: list(rows) for gr, rows in itertools.groupby(
        sorted(args.cldf.iter_rows('languages.csv'), key=lambda r: r['Group'] or ''),
        lambda r: r['Group'] or ''
    )}
    colors = qualitative_colors(len(langs))

    for (gr, langs), color in zip(langs.items(), colors):
        for lang in langs:
            data.add(
                models.Languoid,
                lang['ID'],
                id=lang['ID'],
                name=lang['Name'],
                latitude=lang['Latitude'],
                longitude=lang['Longitude'],
                group=gr,
                icon=color.replace('#', 't' if gr in NON_OCEANIC else 'c'),
                is_proto=lang['Is_Proto'],
                #glottocode=lang['Glottocode']
            )

    for row in args.cldf.iter_rows('ContributionTable'):
        chap = data.add(
            models.Chapter,
            row['ID'],
            id=row['ID'],
            name='{} {}'.format(row['ID'].replace('-', '.'), row['Name']),
            # FIXME: make sure, pandoc.css is available in contribution details page!
            description=args.cldf.directory.parent.joinpath(
                'out',
                'vol{}'.format(row['Volume_Number']),
                'chapter{}.html'.format(row['ID'].split('-')[-1])).read_text(encoding='utf8'),
            volume_num=row['Volume_Number'],
            volume=row['Volume'],
            jsondata=dict(toc=row['Table_Of_Contents']),
        )
        assert len(set(contribs[row['ID']])) == len(contribs[row['ID']]), contribs[row['ID']]
        for i, cid in enumerate(contribs[row['ID']]):
            DBSession.add(common.ContributionContributor(
                contribution=chap, contributor=data['Contributor'][cid], ord=i))

    for row in args.cldf.iter_rows('taxa.csv'):
        t = data.add(
            models.Taxon, row['ID'],
            id=row['ID'],
            name=row['name'],
            description=row['name_eng'],
            rank=row['rank'],
            kingdom=row['kingdom'],
            phylum=row['phylum'],
            klass=row['class'],
            order=row['order'],
            family=row['family'],
            genus=row['genus'],
            genus_eng=row['genus_eng'],
            family_eng=row['family_eng'],
            synonyms=row['synonyms'],
        )
        for cid, fragment in set(tuple(s) for s in row['sections']):
            DBSession.add(models.TaxonChapter(
                taxon=t, chapter=data['Chapter'][cid], fragment=fragment))

    # group glosses by name:
    w2t = set()
    glosses, gid2tid = collections.defaultdict(list), collections.defaultdict(set)
    for gloss, rows in itertools.groupby(
        sorted(args.cldf.iter_rows('glosses.csv'), key=lambda r: slug(str(r['Name']))),
        lambda r: slug(str(r['Name']))
    ):
        for row in rows:
            glosses[row['Form_ID']].append((row, gloss))  # Comment,Source,Part_Of_Speech
            # FIXME: remember Taxon_IDs for each gloss!
            for tid in row['Taxon_IDs']:
                w2t.add((row['Form_ID'], tid))
            gid2tid[row['ID']] |= set(row['Taxon_IDs'])
        data.add(
            models.Gloss,
            gloss,
            id=gloss,
            name=row['Name'],
        )

    for row in args.cldf.iter_rows('FormTable'):
        w = data.add(
            models.Word,
            row['ID'],
            id=row['ID'],
            name=row['Value'],
            description='; '.join(g['Name'] for g, _ in glosses.get(row['ID'], []) if g['Name']),
            language=data['Languoid'][row['Language_ID']],
            variants=' {} '.format(' '.join(variants(row['Value']))),
        )
        for grow, glossid in glosses.get(row['ID'], []):
            g = data.add(
                models.HasGloss, grow['ID'],  # FIXME: POS, comment, etc
                id=grow['ID'],
                unit=w,
                pos=grow['Part_Of_Speech'],
                name=grow['Name'],
                unitparameter=data['Gloss'][glossid],
            )
            for ref in grow['Source']:
                sid, pages = Sources.parse(ref)
                DBSession.add(models.GlossReference(
                    key=sid,
                    description=pages,
                    hasgloss=g,
                    source=data['Source'][sid]))

    for fid, tid in w2t:
        DBSession.add(models.WordTaxon(word=data['Word'][fid], taxon=data['Taxon'][tid]))

    names = set()
    for row in args.cldf.iter_rows('cognatesetreferences.csv'):
        taxa = set()
        for gid in row['Gloss_IDs']:
            if gid in gid2tid:
                taxa |= gid2tid[gid]
        chapter_id = '-'.join(row['ID'].split('-')[:2])
        cs = data.add(
            models.Cognateset, row['ID'],
            id=row['ID'],
            name=cognateset_name(row, data, glosses, names),
            chapter=data['Chapter'][chapter_id],
            fragment=row['ID'],
        )
        for taxon in taxa:
            DBSession.add(models.TaxonCognateset(taxon=data['Taxon'][taxon], cognateset=cs))
        refid = 0
        for lid, fids in itertools.groupby(sorted(row['Form_IDs']), lambda i: i.split('-')[0]):
            # Create ValueSet and Cognate
            vs = data.add(
                common.ValueSet,
                '{}-{}'.format(row['ID'], lid),
                id='{}-{}'.format(row['ID'], lid),
                language=data['Languoid'][lid],
                parameter=cs,
                contribution=data['Chapter']['-'.join(row['ID'].split('-')[:2])],
            )
            for fid in fids:
                refid += 1
                DBSession.add(models.Cognate(
                    id='{}-{}'.format(row['ID'], refid),
                    valueset=vs,
                    word=data['Word'][fid],
                    ord=row['Form_IDs'].index(fid),
                    jsondata={
                        'glosses': [gid for lgid, gid in glosses[fid] if lgid['ID'] in row['Gloss_IDs']],
                        'hasglosses': [r['ID'] for r, _ in glosses[fid] if r['ID'] in row['Gloss_IDs']],
                    }
                ))

    # Now add WordChapter based on cf.csv and cognatesetreference.csv.
    for row in args.cldf.iter_rows('cognatesetreferences.csv'):
        chapter_id = '-'.join(row['ID'].split('-')[:2])
        for fid in row['Form_IDs']:
            DBSession.add(models.WordChapter(
                word=data['Word'][fid],
                chapter=data['Chapter'][chapter_id],
                gloss_ids=' '.join(row['Gloss_IDs']),
                fragment=row['ID']))

    # Now add WordChapter based on cf.csv and cognatesetreference.csv.
    for row in args.cldf.iter_rows('cfitems.csv'):
        chapter_id = '-'.join(row['Cfset_ID'].split('-')[:2])
        DBSession.add(models.WordChapter(
            word=data['Word'][row['Form_ID']],
            chapter=data['Chapter'][chapter_id],
            gloss_ids=' '.join(row['Gloss_IDs']),
            fragment=row['Cfset_ID']))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


def cognateset_name(row, data, glosses, names):
    def fmt_name(f):
        return "{} _*{}_ ‘{}’".format(
            f.language.name,
            f.name,
            '; '.join(g['Name'] for g, _ in glosses.get(fid, [])
                      if g['Name'] and g['ID'] in row['Gloss_IDs']),
        )

    for fid in row['Form_IDs']:
        f = data['Word'][fid]
        if f.language.is_proto:
            if f.language.name not in ['PAn'] and not f.language.name.endswith('MP'):
                name = fmt_name(f)
                break
    else:
        for fid in row['Form_IDs']:
            f = data['Word'][fid]
            if f.language.is_proto:
                name = fmt_name(f)
                break
        else:
            name = row['ID']

    if name in names:
        for dis in 'bcdef':
            _name = '{} ({})'.format(name, dis)
            if _name not in names:
                name = _name
                break
        else:
            raise ValueError(name)

    assert name not in names, name
    names.add(name)
    return name
