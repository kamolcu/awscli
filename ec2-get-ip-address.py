import subprocess
import sys
import json

# Name awsa-mpds-apibe,awsa-mmch-apibe
alpha_api_tags = ['wlx-b-th-d-minv-apiap', 'wlx-b-th-d-mprc-apiap', 'wlx-b-th-d-mpds-apiap', 'wlx-b-th-d-mmch-apiap','wlx-b-th-d-mfin-apiap', 'wlx-b-th-d-mauth-apiap','wlx-b-th-d-mcrt-apiap','wlx-th-d-jenkins','wlx-b-th-d-mweb-apiap','wlx-b-th-d-mort-apiap']
command_template = 'aws ec2 describe-instances --filters "Name=tag:Name,Values=%s"'

ec_two_s = []
for tag in alpha_api_tags:
    target_command = command_template % tag
    p = subprocess.Popen(target_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (ret, err) = p.communicate()
    if err is not None and len(err.strip()) > 0:
        sys.exit(err)
    jj = json.loads(ret)
    ec_two_list = jj['Reservations']
    for ec_two_inst in ec_two_list:
        ec_two_s.append(ec_two_inst)

for ec_two in ec_two_s:
    try:
        for tag in ec_two['Instances'][0]['Tags']:
            if(tag['Key'] == 'Name'):
                instance_name = tag['Value']
                print '%s <-> %s' % (instance_name, ec_two['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddresses'][0]['PrivateIpAddress'])
    except Exception, e:
        pass
    else:
        pass
    finally:
        pass

