from __future__ import print_function

import boto3
import json
import os
import btr3baseball

jobTable = os.environ['JOB_TABLE']
jobQueue = os.environ['JOB_QUEUE']
queue = boto3.resource('sqs').get_queue_by_name(QueueName=jobQueue)
jobRepo = btr3baseball.JobRepository(jobTable)
dsRepo = btr3baseball.DatasourceRepository()

def main(event, context):
    method = event['method']
    if 'data' in event:
        data = event['data']
    else:
        data = None

    print(data)

    if method == 'submitJob':
        return submitJob(data, context)
    elif method == 'getJob':
        return getJob(data, context)
    elif method == 'listDatasources':
        return listDatasources(data, context)
    elif method == 'getDatasource':
        return getDatasource(data, context)
    else:
        return None

def submitJob(event, context):
    # Put initial entry in dynamo db
    jobId = jobRepo.createJob(event)

    # Put the job ID on the SQS queue
    response = queue.send_message(MessageBody=jobId)

    # Update the DB entry with sqs message ID for traceability
    return jobRepo.updateWithMessageId(jobId, response.get('MessageId')) 

def getJob(event, context):
    return jobRepo.getJob(event['jobId'])

def listDatasources(event, context):
    return dsRepo.listDatasources()

def getDatasource(event, context):
    return dsRepo.getDatasource(event['datasourceId'])