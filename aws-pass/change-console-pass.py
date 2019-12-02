import boto3
import argparse
import os

# ARGS 
parser = argparse.ArgumentParser(
  description="""Script to change expired AWS console password.
  It's based on your acces key. You could provide it via:
  -profile name (aws cli config)
  -directly putting your access key with propper switches
  -environmen variables (same as for AWS CLI)"""
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
parser.add_argument('--quiet', '-q', action='store_true', 
  help='Do not ask about user input. Assume as "yes"', default=False
  )

args = parser.parse_args()

# PARSING ARGS
def log(message):
    if args.debug:
        print(message)


if args.old_password == None:
  if not args.quiet:
    args.old_password = input('Please, provide your old password:')
  else:
    args.old_password = ''

if args.old_password == '':
  print('You need to provide your old passord.')
  os._exit(1)

if not args.profile or ( not args.access_key_id and not args.access_key ):
  if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_ACCESS_KEY_ID' in os.environ:
    args.access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    args.access_key = os.environ['AWS_SECRET_ACCESS_KEY']
  elif 'default' in boto3.Session().available_profiles:
    args.profile = 'default'
  else:
    print("""
      No API credentials found :( 
      Please configure AWS CLI or provide AWS access key directly,
      you could also set propper environment variables.
      """)
    parser.print_help()
    os._exit(1)

log(args)

if args.profile:
  session = boto3.Session(profile_name=args.profile)
elif args.access_key_id and args.access_key:
  session = boto3.Session(aws_access_key_id=args.access_key_id, aws_secret_access_key=args.access_key)

client = session.client('sts')
acc_id = client.get_caller_identity().get('Account')
username = client.get_caller_identity().get('Arn').split('/')[-1]
if not args.quiet:
  answer = ""
  while answer not in ["y", "n"]:
    answer = input("Are you sure you want to change password for " + username + " on account " + acc_id + " [Y/N]? ").lower()
else:
  answer = "y"
if answer == "y":
  client = session.client('iam')
  response = client.change_password(
            OldPassword=args.old_password,
            NewPassword=args.new_password
        )
else:
  print('Ok, maybe You will try later?')