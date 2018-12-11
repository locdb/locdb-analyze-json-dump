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
    output = "" + title(br) + " (" + date(br) + ")" + "   " + br["_id"]
    return output


# read JSON data
with open('data.json', encoding='utf8') as f:
    fullData = json.load(f)
# clean it up
data = []
for br in fullData:
    data.append(cleanup(br))

print("There are currently", len(data), "entries in this data dump.")
types = {}
for i in range(len(data)):
    if data[i]["type"] in types:
        types[data[i]["type"]] += 1
    else:
        types[data[i]["type"]] = 1
print("Type statistics", types)

print("Show one entry:", json.dumps(data[0], indent=4))

for k in range(10):
    print("Show one entry:", json.dumps(data[k], indent=4))
    print("Short format of this entry:\n   ", citation(data[k]))
#
# for k in range(3000):
#     autString = authors(cleanedData[k])
#     if autString != "":
#         print(autString)

mappingIdentifiers = {}
for i in range(len(data)):
    id = data[i]["_id"]
    mappingIdentifiers[id] = i

print("Show one entry by id:", json.dumps(data[mappingIdentifiers["5b4386c13f6d9d57f6aec70a"]], indent=4))#5bab9d7fc3bd212c2435638d

# look for duplicate ids
seen = {}
for i in range(len(data)):
    for field in data[i]:
        if field.endswith("_identifiers"):
            for id in data[i][field]:
                if "scheme" in id and "literalValue" in id:
                    key = id["scheme"] + ":" + id["literalValue"]
                    if key in seen:
                        print("Duplicate found", key, "is in", seen[key], "and", data[i]["_id"])
                    else:
                        seen[key] = data[i]["_id"]
                else:
                    print("Error with identifiers in", i, id)


# add reverse property children from partOf relation
for i in range(len(data)):
    id = data[i]["_id"]
    if "partOf" in data[i] and data[i]["partOf"] != "":
        if data[i]["partOf"] in mappingIdentifiers:
            parentElement = data[mappingIdentifiers[data[i]["partOf"]]]
            if "children" in parentElement:
                parentElement["children"].append(id)
            else:
                parentElement["children"] = [id]
        else:
            print("WARNING: Key", data[i]["partOf"], "not found but given as partOf in", id)

# list all resources with its children or as standalone
data.sort(key=lambda br: title(br).lower())
for i in range(len(data)):
    if "children" in data[i]:
        print("\n+ " + citation(data[i]))
        for child in data[i]["children"]:
            print("|_", citation(data[mappingIdentifiers[child]]))
    else:
        if "partOf" not in data[i]:
            print("\n- " + citation(data[i]))
