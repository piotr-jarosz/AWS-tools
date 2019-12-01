import boto3
import argparse
import os


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
  default=None
  )
parser.add_argument(
  '--access-key-id', 
  help='AWS AccessKey ID', 
  default=None
  )
parser.add_argument(
  '--access-key', 
  help='AWS AccessKey', 
  default=None)

parser.add_argument('--debug', action='store_true', 
  help=argparse.SUPPRESS, default=False
  )

args = parser.parse_args()

def log(message):
    if args.debug:
        print(message)

log(args)


if args.old_password == None:
  args.old_password = input('Please, provide your old password:')

if args.old_password == '':
  print('You need to provide your old passord.')
  os._exit(1)



os.environ['HOME']


def aws_client(profile):
  if profile == 'default':
    session = boto3.Session()
  else:
    session = boto3.Session(profile_name=profile)
  client = session.client('iam', region_name = 'eu-central-1')
  return client