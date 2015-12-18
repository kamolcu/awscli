import argparse
import subprocess
import sys
import json

def write_items_file(file_name, contents):
    f = open(file_name, "w")
    f.write(json.dumps(contents))
    f.close()

parser = argparse.ArgumentParser(description='Import DynamoDB table from file')
parser.add_argument('table_name', help='DynamoDB Table Name')
parser.add_argument('items_file_to_import', help='File that contains items from export.py')

args = parser.parse_args()
export_command = 'aws dynamodb scan --table-name %s' % (args.table_name)
print('Command to run => [%s]' % export_command)
p = subprocess.Popen(export_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(ret, err) = p.communicate()

if err is not None and len(err.strip()) > 0:
    sys.exit(err)

print('Scan Table [%s] OK.' % args.table_name)
jj = json.loads(ret)
print('Current total row found = %s' % jj['Count'])
temp_key_file_json = 'import-keys.json'
put_item_command = 'aws dynamodb batch-write-item --request-items file://%s' % temp_key_file_json
MAX_BATCH_WRITE = 25
put_item_requests = []
items_from_file = json.load(open(args.items_file_to_import))
for item in items_from_file:
    print('Importing item = %s' % item)
    put_item_requests.append({"PutRequest": {"Item": item}})
    if len(put_item_requests) == MAX_BATCH_WRITE:
        json_obj = {args.table_name: put_item_requests}
        write_items_file(temp_key_file_json, json_obj)
        p = subprocess.Popen(put_item_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (ret, err) = p.communicate()
        if err is not None and len(err.strip()) > 0:
            sys.exit(err)
        del put_item_requests[:]

if len(put_item_requests) > 0:
        json_obj = {args.table_name: put_item_requests}
        write_items_file(temp_key_file_json, json_obj)
        p = subprocess.Popen(put_item_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (ret, err) = p.communicate()
        if err is not None and len(err.strip()) > 0:
            sys.exit(err)
