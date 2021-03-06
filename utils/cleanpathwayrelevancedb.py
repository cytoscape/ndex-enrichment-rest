#! /usr/bin/env python

import sys
import json

if len(sys.argv) < 3:
    sys.stderr.write('\nThis program cleans the '
                     'databaseresults.json pathway '
                     'relevance database\n')
    sys.stderr.write('by removing data generated during '
                     '--mode createdb call\n\n')
    sys.stderr.write('Usage: ' +
                     sys.argv[0] +
                     ' <input databaseresults.json> <cleaned json>\n')
    sys.exit(1)

# load data
with open(sys.argv[1], 'r') as f:
    data = json.load(f)

# clear out data generated by --mode createdb 
data['universeUniqueGeneCount'] = 0
data['totalNetworkCount'] = 0
data['databaseUniqueGeneCount'] = {}
data['networksToExclude'] = []
data['geneMapList'] = []
data['idfMap'] = {}
data['networkToGeneToNodeMap'] = {}

# clear out networks list under results and
# build a map of UUID => database name 
# so we can update networkset id field
# under databaseConnectionMap 
uuid_to_db_name = {}
for entry in data['results']:
    entry['networks'] = []
    entry['numberOfNetworks'] = '0'
    uuid_to_db_name[entry['uuid']] = entry['name']

# iterate through databaseConnectionMap and
# update user, server, and password to text denoting
# ENTER X 
# set networkSetId to ENTER NETWORK SET ID for <NAME> ie UUID... 
for ckey in data['databaseConnectionMap'].keys():
    if ckey not in uuid_to_db_name:
        sys.stderr.write(ckey + ' in "databaseConnectionMap" does NOT '
                                'have an entry under "results" skipping\n')
        continue
    con_entry = data['databaseConnectionMap'][ckey]
    con_entry['user'] = '<ENTER NDEX USERNAME>'
    con_entry['password'] = '<ENTER PASSWORD FOR NDEX ACCOUNT>'
    con_entry['server'] = 'public.ndexbio.org'

with open(sys.argv[2], 'w') as f:
    json.dump(data, f, indent=2)
