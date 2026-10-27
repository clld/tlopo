# Releasing the tlopo webapp

```shell
git clone https://github.com/clld/tlopo
git clone https://github.com/lexibank/tlopo tlopo-cldf
cd tlopo-cldf
git checkout v0.1
cd ../tlopo
pip install -e .[test]
```

recreate app db:

```shell
clld initdb development.ini --cldf ../tlopo-cldf/cldf/cldf-metadata.json
```

```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO tlopo > tlopo.sql
zip tlopo.sql.zip tlopo.sql
rm tlopo.sql
```

