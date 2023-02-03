#!/usr/bin/python3

import boto3

AWS_REGION = "us-east-1"
ec2 = boto3.resource('ec2',region_name=AWS_REGION)
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id, instance.instance_type)