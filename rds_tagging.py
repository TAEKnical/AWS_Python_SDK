#Reg : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances

import boto3
import json
from bson import json_util

client = boto3.client('rds')

dev_db_list = []
staging_db_list = []
prd_db_list = []

for dbInstance in client.describe_db_instances(MaxRecords=100)["DBInstances"]:
    if "dev" in dbInstance["DBInstanceIdentifier"]:
        dev_db_list.append(dbInstance["DBInstanceArn"])
 
    elif "staging" in dbInstance["DBInstanceIdentifier"]:
        staging_db_list.append(dbInstance["DBInstanceArn"])

    else:
        prd_db_list.append(dbInstance["DBInstanceArn"])

print("dev : ", dev_db_list)
print("staging : ", staging_db_list)
print("prd : ", prd_db_list)

def create_tag(db_list, env, client):
    for name in db_list:
        client.add_tags_to_resource(
            ResourceName = name,
            Tags=[
                {
                    'Key' : 'Environment',
                    'Value' : env
                }
            ]
        )

create_tag(dev_db_list,"development",client)
create_tag(staging_db_list,"staging",client)
create_tag(prd_db_list,"production",client)
