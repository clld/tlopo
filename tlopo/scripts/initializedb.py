import itertools
import collections

from csvw.dsv import reader
from pycldf import Sources
from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex


import tlopo
from tlopo import models

def main(args):

    data = Data()

    data.add(
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
    #ID,semantics,Volume,chapter
    chapter_md = {r['ID']: r for r in reader(args.cldf.directory / 'semantics.csv', dicts=True)}

    for lang in args.cldf.iter_rows('languages.csv', 'ID', 'Name', 'Note_name', 'Latitude', 'Longitude'): #'Subgroup', 'Glottocode', 'Note_name', 'Name2', 'Latitude', 'Longitude'):
        data.add(
            common.Language,
            lang['ID'],
            id=lang['ID'],
            name=lang['Name'],
            latitude=lang['Latitude'],
            longitude=lang['Longitude'],
            #glottocode=lang['Glottocode']
            )


    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    reconstructions = collections.Counter()
    chapters = set()
    for cogset in args.cldf.iter_rows('cognatesets.csv', 'ID', 'Reconstruction', 'Gloss', 'Notes', 'Domain', 'Description'):
        if cogset['Domain'] not in chapters:
            chapters.add(cogset['Domain'])
            md = chapter_md[cogset['Domain']]
            chapter = data.add(
                common.Contribution,
                cogset['Domain'],
                id='{}-{}'.format(md['Volume'], md['chapter']),
                name=md['semantics'],
            )
        if cogset['Reconstruction'] in reconstructions:
            name = '{} {}'.format(cogset['Reconstruction'], reconstructions[cogset['Reconstruction']] + 1)
        else:
            name = cogset['Reconstruction']
        reconstructions.update([cogset['Reconstruction']])
        data.add(        
            models.Cognateset,
            cogset['ID'],
            id=cogset['ID'],
            name=name,
            gloss=cogset['Gloss'],
            chapter=chapter,
            description=cogset['Description']
        )

    for (cogid, lid), forms in itertools.groupby(
        sorted(
            args.cldf.iter_rows('forms.csv', 'ID', 'Form', 'Gloss', 'Language_ID', 'Notes', 'Source','Cognateset_ID'),
            key=lambda r: (r['Cognateset_ID'] or '', r['Language_ID'], r['ID'])
        ),
        lambda r: (r['Cognateset_ID'], r['Language_ID'])
    ):
        if not cogid:
            continue
        vsid = '{}-{}'.format(cogid, lid)
        vs = data.add(
            common.ValueSet,
            vsid,
            id=vsid,
            language=data['Language'][lid],
            parameter=data['Cognateset'][cogid],
            contribution=chapter,
        )
        for form in forms:
            data.add(
                models.Word,
                form['ID'],
                valueset=vs,
                id=form['ID'],
                name=form['Form'],
                description=form['Gloss'],
                #note=form['Notes'],
            #source=data['Source'][''.join(form['Source'])] if form['Source'] else None
            #source=data['Source'][''.join(form['Source'])]
            )



def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
