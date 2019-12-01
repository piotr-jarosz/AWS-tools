import boto3


#TEMPORARY CONFIGURATION
profile = 'default'


def aws_client(account):
  if account == 'default':
    session = boto3.Session()
  else:
    session = boto3.Session(profile_name=account)
  client = session.client('iam', region_name = 'eu-central-1')
  return client