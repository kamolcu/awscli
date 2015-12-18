import argparse
import subprocess
import sys
import json

def write_items_file(file_name, contents):
    f = open(file_name, "w")
    f.write(json.dumps(contents))
    f.close()

parser = argparse.ArgumentParser(description='Count row of target DynamoDB table')
parser.add_argument('table_name', help='DynamoDB Table Name')

args = parser.parse_args()
export_command = 'aws dynamodb scan --table-name %s --no-consistent-read --cli-input-json file://scan-count.json' % (args.table_name)
print('Command to run => [%s]' % export_command)
p = subprocess.Popen(export_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(ret, err) = p.communicate()

if err is not None and len(err.strip()) > 0:
    sys.exit(err)

print('Scan Table [%s] OK.' % args.table_name)
jj = json.loads(ret)
print('Current total row found = %s' % jj['Count'])