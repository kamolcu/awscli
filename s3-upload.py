import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description='Upload specified files to a target S3 bucket (not support exclude and include feature yet)')
parser.add_argument('file_path', help='File full path or directory full path')
parser.add_argument('bucket_name', help='S3 bucket name e.g. images')
parser.add_argument('--recursive', action='store_true', help='Recursive flag, use with directory full path argument')
args = parser.parse_args()

# aws s3 cp /tmp/foo/ s3://bucket/ --recursive --exclude "*" --include "*.jpg" --include "*.txt"
command = 'aws s3 cp %s s3://%s/ %s' % (args.file_path, args.bucket_name, '--recursive' if args.recursive else '')
print('Command to run => [%s]' % command)
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(ret, err) = p.communicate()

# Possible errors:
# The user-provided path <file_path> does not exist.
# upload failed: ... A client error (AccessDenied) occurred when calling the PutObject operation: Access Denied
if err is not None and len(err.strip()) > 0:
    sys.exit(err)

print('Upload to S3 OK.')
