#ssh -i ~/.ssh/ec2key.pem ubuntu@ec2-50-16-62-250.compute-1.amazonaws.com

import sys, site
site.addsitedir('/home/timmyt/.virtualenvs/smarttypes/lib/python%s/site-packages' % sys.version[:3])
sys.path.insert(0, '/home/timmyt/projects/smarttypes')

from smarttypes.config import *

#ubuntu amis: http://alestic.com/
image_map = {
    'ubuntu_clean':'ami-2ec83147',
}

instance_types = [
    'm1.small','m1.large','m1.xlarge',
    'c1.medium','c1.xlarge',
    'm2.xlarge','m2.2xlarge','m2.4xlarge',
    'cc1.4xlarge','t1.micro',
]

#connect and start instance
from boto.ec2.connection import EC2Connection
conn = EC2Connection(AWS_ACCESS_KEY, AWS_ACCESS_SECRET)

#ssh and execute command
conn.run_instances(image_map['ubuntu_1004_64_ebs_snapshot'], instance_type='t1.micro')






