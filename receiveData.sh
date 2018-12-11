#!/usr/bin/env bash

curl -X GET "https://locdb-analyze-json-dump.bib.uni-mannheim.de/locdb-analyze-json-dump/bibliographicResources" -H  "accept: application/json" -o data.json
