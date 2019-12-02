import boto3
import argparse
import os

# ARGS 
parser = argparse.ArgumentParser(
  description='Change expired AWS console password.',
  epilog="It's based on your tokens in AWS CLI config path"
  )

parser.add_argument(
  '--old-password', '-o', 
  help='Old password to AWS console, \
  if not provided script will ask you interactively about it.', 
  default=None
  )
parser.add_argument(
  '--new-password', '-n', 
  help='New password to AWS console, \
  when no value provided it will be generated', 
  default='generate'
  )
parser.add_argument(
  '--profile', '-p', 
  help='AWS profile name', 
  default=False
  )
parser.add_argument(
  '--access-key-id', 
  help='AWS AccessKey ID', 
  default=False
  )
parser.add_argument(
  '--access-key', 
  help='AWS AccessKey', 
  default=False)

parser.add_argument('--debug', action='store_true', 
  help=argparse.SUPPRESS, default=False
  )

args = parser.parse_args()

# PARSING ARGS
def log(message):
    if args.debug:
        print(message)


if args.old_password == None:
  args.old_password = input('Please, provide your old password:')

if args.old_password == '':
  print('You need to provide your old passord.')
  os._exit(1)

if not args.profile or ( not args.access_key_id and not args.access_key ):
  if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_ACCESS_KEY_ID' in os.environ:
    args.access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    args.access_key = os.environ['AWS_SECRET_ACCESS_KEY']
  elif boto3.Session().available_profiles:
    args.profile = 'default'
  else:
    print("""
      No API credentials found :( 
      Please configure AWS CLI or provide AWS access key directly,
      you could also set propper environment variables.""")
    os._exit(1)

log(args)


def aws_client(profile):
  if profile == 'default':
    session = boto3.Session()
  else:
    session = boto3.Session(profile_name=profile)
  client = session.client('iam', region_name = 'eu-central-1')
  return client