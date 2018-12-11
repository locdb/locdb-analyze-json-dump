# locdb-analyze-json-dump

First, receive the current data from locdb (production system) with the following bash script:
```bash
./receiveData.sh
```
This will download one JSON file with all the data.
Be aware that this file is currently 24 MB large!
You should only download it if you need the new data.

Second, analyze the local JSON file now with
```bash
./analyze.py
```
