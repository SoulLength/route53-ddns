import os
from dotenv import load_dotenv
load_dotenv()

AWS_HOSTED_ZONE_ID=os.environ["AWS_HOSTED_ZONE_ID"]
AWS_DOMAIN_NAME=os.environ["AWS_DOMAIN_NAME"]