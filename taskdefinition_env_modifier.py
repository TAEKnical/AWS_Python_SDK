import boto3
import json
from bson import json_util

CLUSTER_NAME = "-"

client = boto3.client('ecs')
paginator = client.get_paginator('list_services')

listServices = []

for page in paginator.paginate(
    cluster=CLUSTER_NAME
):
    listServices.extend(page['serviceArns'])

n = 10 
listServices = [listServices[i*n:(i+1)*n] for i in range((len(listServices) + n-1) // n)] # describe_services api의 services 파라미터 max가 10이므로 10개단위로 분할하였음

services = []
for listService in listServices:
    tmp = client.describe_services(
        cluster = CLUSTER_NAME,
        services = listService
        )
    services.extend(tmp['services'])

taskDefinitions_arn = []
for service in services:
    taskDefinitions_arn.append(service['taskDefinition'])

taskDefinitions_list = []

for taskDef in taskDefinitions_arn:
    taskDefinitions_list.append(client.describe_task_definition(
        taskDefinition=taskDef
    ))

result = []

for taskDefinition in taskDefinitions_list:
    taskDefinition = taskDefinition['taskDefinition']
    for containerDef in taskDefinition['containerDefinitions']:
        if("logConfiguration" not in containerDef):
            continue
        options = containerDef["logConfiguration"]
        if "dd_env" in options:
            result.append(taskDefinition['taskDefinitionArn'])

result = list(set(result))


for i in result:
    print(i)