# Export DynamoDB table and upload to S3
# table_name = "wms-d-dym-pds-variants"
# s3bucket = ""

# https://docs.python.org/2/library/argparse.html
# https://docs.python.org/2/library/subprocess.html
# https://github.com/bchew/dynamodump/blob/master/dynamodump.py
import argparse
import subprocess
import sys
import json
import gzip

def write_items_file(file_name, contents):
    f = open(file_name, "w")
    f.write(json.dumps(contents))
    f.close()

parser = argparse.ArgumentParser(description='Export DynamoDB table')
parser.add_argument('table_name', help='DynamoDB Table Name')

args = parser.parse_args()
export_command = 'aws dynamodb scan --table-name %s' % (args.table_name)
print('Command to run => [%s]' % export_command)
p = subprocess.Popen(export_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(ret, err) = p.communicate()

if err is not None and len(err.strip()) > 0:
    sys.exit(err)

print('Scan Table [%s] OK.' % args.table_name)
jj = json.loads(ret)
print('Total row found = %s' % jj['Count'])
# Create output file
items = jj['Items']
output_file_name = '%s_export.txt' % args.table_name
write_items_file(output_file_name, items)
