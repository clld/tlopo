# Releasing the tlopo webapp

```shell
git clone https://github.com/clld/tlopo
git clone --branch v0.1.1 --depth 1 https://github.com/lexibank/tlopo tlopo-cldf
git clone --branch v2.0 --depth 1 https://github.com/glottography/wurm1981pacific
cd tlopo
pip install -e .[test]
```

recreate app db:

```shell
clld initdb development.ini --cldf ../../lexibank/tlopo/cldf/cldf-metadata.json
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
pg_dump -xO --compress gzip:9 tlopo > tlopo.sql.gz
```

