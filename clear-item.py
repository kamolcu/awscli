import argparse
import subprocess
import sys
import json
import gzip

def write_items_file(file_name, contents):
    f = open(file_name, "w")
    f.write(json.dumps(contents))
    f.close()

parser = argparse.ArgumentParser(description='Clear all items in specified DynamoDB table')
parser.add_argument('table_name', help='DynamoDB Table Name e.g. wms-dym-pds-table')
parser.add_argument('primary_key', help='Partition Key(Hash Key) Name e.g. row_id')
args = parser.parse_args()

temp_key_file_json = 'keys.json'
delete_command = 'aws dynamodb batch-write-item --request-items file://%s' % temp_key_file_json

target_command = 'aws dynamodb scan --table-name %s' % (args.table_name)
print('Command to run => [%s]' % target_command)
p = subprocess.Popen(target_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(ret, err) = p.communicate()

if err is not None and len(err.strip()) > 0:
    sys.exit(err)

print('Scan Table [%s] OK.' % args.table_name)
jj = json.loads(ret)
print('Total row found = %s' % jj['Count'])
items = jj['Items']

MAX_BATCH_WRITE = 25
del_requests = []
for ii in items:
    print('Deleting item key %s' % ii[args.primary_key])
    del_requests.append({"DeleteRequest": {"Key": {args.primary_key: ii[args.primary_key]}}})
    if len(del_requests) == MAX_BATCH_WRITE:
        json_obj = {args.table_name: del_requests}
        write_items_file(temp_key_file_json, json_obj)
        p = subprocess.Popen(delete_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (ret, err) = p.communicate()
        if err is not None and len(err.strip()) > 0:
            sys.exit(err)
        del del_requests[:]

if(len(del_requests) > 0):
    json_obj = {args.table_name: del_requests}
    write_items_file(temp_key_file_json, json_obj)
    p = subprocess.Popen(delete_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (ret, err) = p.communicate()
    if err is not None and len(err.strip()) > 0:
        sys.exit(err)
