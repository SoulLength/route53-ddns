import boto3
import requests
from constants import AWS_HOSTED_ZONE_ID, AWS_DOMAIN_NAME
from time import sleep
client = boto3.client('route53')

def get_route53_ip():
    response = client.list_resource_record_sets(
        HostedZoneId=AWS_HOSTED_ZONE_ID,
        StartRecordName=AWS_DOMAIN_NAME,
        StartRecordType='A',
        MaxItems="1"
    )
    return response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']

def get_my_ip():
    return requests.get('https://api.ipify.org').text

def set_route53_ip(ip_address):
    client.change_resource_record_sets(
            HostedZoneId=AWS_HOSTED_ZONE_ID,
            ChangeBatch={
                'Comment': 'Update A record to new IP address',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': AWS_DOMAIN_NAME,
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': ip_address}]
                        }
                    }
                ]
            }
        )
    
route53_cache_ip = ""
while True:
    try:
        my_ip = get_my_ip()
        if my_ip != route53_cache_ip:
            if my_ip != get_route53_ip():
                set_route53_ip(my_ip)
                print(f"IP updated to: {my_ip}")
            route53_cache_ip = my_ip
    except:
        print("Connection error!")
    sleep(1800)
