
recreate CLDF dataset

cldfbench lexibank.makecldf ...


re-render the HTML pages:

cldfbench tlopo.render


recreate app db:

clld initdb development.ini --cldf ../../lexibank/tlopo/cldf/cldf-metadata.json

