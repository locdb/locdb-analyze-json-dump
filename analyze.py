#!/usr/bin/env python3

import json


def cleanup(br):
    out = {}
    for field in br:
        if br[field] != [] and br[field] != "":
            out[field] = br[field]
    return out


def title(br):
    for field in br:
        if field.endswith("_title"):
            return br[field]
    return "[Not Title found]"


def date(br):
    for field in br:
        if field.endswith("_publicationDate"):
            # Only output the year, i.e. first 4 characters
            return br[field][:4]
    return "s.d."


def type(br):
    for field in br:
        if field == "type":
            # Only output
            words = br[field].split("_")
            starts = [c[0] for c in words]
            return "[" + ''.join(starts) + "]"
    return "[]"


def authors(br):
    for field in br:
        if field.endswith("_contributors") and br[field] != []:
            authorsArray = []
            for contributor in br[field]:
                if "roleType" in contributor and contributor["roleType"] == "AUTHOR":
                    if "heldBy" in contributor:
                        if "nameString" in contributor["heldBy"]:
                            authorsArray.append(contributor["heldBy"]["nameString"])
                        else:
                            authorsArray.append("[no nameString]")
            return ' / '.join(authorsArray)


def citation(br):
    output = "" + type(br) + " " + title(br) + " (" + date(br) + ")" + "   " + br["_id"]
    return output


# read JSON data
with open('data.json', encoding='utf8') as f:
    fullData = json.load(f)
# clean it up and save in a dict by its id
data = {}
for br in fullData:
    id = br["_id"]
    data[id] = cleanup(br)

# some statistic
print("There are currently", len(data), "entries in this data dump.")
types = {}
for i in data:
    if data[i]["type"] in types:
        types[data[i]["type"]] += 1
    else:
        types[data[i]["type"]] = 1
print("Type statistics", types)

# show single entry by id
print("Show one entry by id:",
      json.dumps(data["5a5e0aaf26f6bc19fe209546"], indent=4))
print("Show one entry by id:",
      json.dumps(data["5bab9d86c3bd212c24356625"], indent=4))  # 5bab9d7fc3bd212c2435638d

# look for duplicate ids
seen = {}
for i in data:
    for field in data[i]:
        if field.endswith("_identifiers"):
            for id in data[i][field]:
                if "scheme" in id and "literalValue" in id:
                    if id["scheme"] == "ISSN" or id["scheme"] == "ZDB_ID" or id["scheme"] == "ISBN":
                        break
                    key = id["scheme"] + ":" + id["literalValue"]
                    if key in seen:
                        print("Duplicate found", key, "is in", seen[key], "and", data[i]["_id"])
                    else:
                        seen[key] = data[i]["_id"]
                else:
                    print("Error with identifiers in", i, id)

# add reverse property children from partOf relation
for i in data:
    if "partOf" in data[i] and data[i]["partOf"] != "":
        if data[i]["partOf"] in data:
            parentElement = data[data[i]["partOf"]]
            if "children" in parentElement:
                parentElement["children"].append(i)
            else:
                parentElement["children"] = [i]
        else:
            print("WARNING: Key", data[i]["partOf"], "not found but given as partOf in", i)

# list all resources with its children or as standalone
dataList = sorted(data.items(), key=lambda kv: title(kv[1]).lower())
for key, element in dataList:
    if "children" in element:
        print("\n+ " + citation(element))
        for child in element["children"]:
            print("|_", citation(data[child]))
    else:
        if "partOf" not in element:
            print("\n- " + citation(element))
