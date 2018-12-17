#!/usr/bin/env bash

curl -X GET "https://locdb.bib.uni-mannheim.de/locdb/bibliographicResources" -H  "accept: application/json" -o data.json
