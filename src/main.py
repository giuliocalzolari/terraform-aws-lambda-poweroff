
from datetime import datetime, timedelta, time
from logging import shutdown
import boto3

TIME = {
    'eu-central-1': {
        'description':  'Europe(Frankfurt)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+1'
    },
    'eu-north-1': {
        'description':  'Europe(Stockholm)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+1'
    },
    'eu-west-1': {
        'description':  'Europe(Ireland)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+0'
    },
    'eu-west-2': {
        'description':  'Europe(London)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+0'
    },
    'eu-west-3': {
        'description':  'Europe(Paris)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+1'
    },
    'eu-south-3': {
        'description':  'Europe(Milan)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+1'
    },
    'me-south-1': {
        'description':  'Middle East(Bahrain)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+3'
    },
    'ca-central-1': {
        'description':  'Canada(Central)',
        'permitted_execution_time': '8-19',
        'utc_offset': '-5'
    },
    'us-east-1': {
        'description':  'US East(N. Virginia)',
        'permitted_execution_time': '8-19',
        'utc_offset': '-5'
    },
    'us-east-2': {
        'description':  'US East(Ohio)',
        'permitted_execution_time': '8-19',
        'utc_offset': '-5'
    },
    'us-west-1': {
        'description':  'US West(N. California)',
        'permitted_execution_time': '8-19',
        'utc_offset': '-8'
    },
    'us-west-2': {
        'description':  'US West(Oregon)',
        'permitted_execution_time': '8-19',
        'utc_offset': '-8'
    },
    'ap-southeast-1': {
        'description':  'Asia Pacific(Singapore)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+8'
    },
    'ap-southeast-2': {
        'description':  'Asia Pacific(Sydney)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+10'
    },
    'ap-southeast-3': {
        'description':  'Asia Pacific(Jakarta)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+7'
    },
    'ap-northeast-1': {
        'description':  'Asia Pacific(Tokyo)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+9'
    },
    'ap-northeast-2': {
        'description':  'Asia Pacific(Seoul)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+9'
    },
    'ap-northeast-3': {
        'description':  'Asia Pacific(Osaka)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+9'
    },
    'ap-east-1': {
        'description':  'Asia Pacific(Hong Kong)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+8'
    },
    'ap-south-1': {
        'description':  'Asia Pacific(Mumbai)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+5.5'
    },
    'sa-east-1': {
        'description':  'South America(Sao Paulo)',
        'permitted_execution_time': '8-19',
        'utc_offset': '-3'
    },
    'af-south-1': {
        'description':  'Africa(Cape Town)',
        'permitted_execution_time': '8-19',
        'utc_offset': '+2'
    },
}


def range_region_time(region_name):
    begin_time_s, end_time_s = TIME[region_name]['permitted_execution_time'].split('-')
    tz = TIME[region_name]['utc_offset']
    tz_now = datetime.utcnow() + timedelta(hours=float(tz))

    begin_time = datetime(tz_now.year, tz_now.month,
                          tz_now.day, int(begin_time_s), 0)
    end_time = datetime(tz_now.year, tz_now.month,
                        tz_now.day, int(end_time_s), 0)
    print('time {} in region {}'.format(tz_now, region_name))
    if begin_time < tz_now < end_time:
        # print("BETWEEN!")
        return True
    else:
        # print("NOT!")
        return False


def shutdown_ec2(region):
    print('searching EC2 in region {} - {}'.format(region, TIME[region]['description']))
    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print('Stopping EC2 {} in region {}'.format(instance.id, region))
    ec2.instances.stop()


def shutdown_rds(region):
    print('searching RDS in region {} - {}'.format(region,TIME[region]['description']))
    rds = boto3.client('rds', region_name=region)
    instances_rds = rds.describe_db_instances().get('DBInstances', [])
    for instance_rds in instances_rds:
        if instance_rds['DBInstanceStatus'] == 'available':
            rds_id = instance_rds['DBInstanceIdentifier']
            print('Stopping RDS {} in region {}'.format(rds_id, region))
            rds.stop_db_instance(DBInstanceIdentifier=rds_id,)


def lambda_handler(event, context):
    client = boto3.client('ec2')
    ec2_regions = [region['RegionName']
                   for region in boto3.client('ec2').describe_regions()['Regions']]
    for region in ec2_regions:
        if not range_region_time(region):

            shutdown_ec2(region)
            shutdown_rds(region)


if __name__ == '__main__':
    event = {
        'account': '123456789012',
        'region': u'us-east-1',
        'detail': {},
        'detail-type': 'Scheduled Event',
         'source': 'aws.events',
         'time': '1370-01-01T00:00:00Z',
         'id': 'cdc73f9d-aea9-11e3-9d5a-835b769c0d9c',
         'resources': ['arn:aws:events:us-east-1:123456789012:rule/my-schedule']
        }
    lambda_handler(event,'')
