#!/usr/bin/python3

import boto3

client = boto3.client('ce', region_name='us-east-1')

response = client.get_cost_and_usage_with_resources.filter(
    TimePeriod={
        'Start': '2023-01-01',
        'End': '2023-02-01'
    },
    Granularity='MONTHLY',
    Metrics=[
        'AmortizedCost',
    ]
)

print(response)