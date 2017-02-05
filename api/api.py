from __future__ import print_function

import boto3
import json
import os
import btr3baseball

jobTable = os.environ['JOB_TABLE']
jobQueue = os.environ['JOB_QUEUE']
queue = boto3.resource('sqs').get_queue_by_name(QueueName=jobQueue)
jobRepo = btr3baseball.JobRepository(jobTable)
dsRepo = btr3baseball.DatasetRepository()

def main(event, context):
    method = event['method']
    if 'data' in event:
        data = event['data']
    else:
        data = None

    print(data)

    if method == 'getOutputImage':
        return getOutputImage(data, context)
    elif method == 'submitJob':
        return submitJob(data, context)
    elif method == 'validateJob':
        return validateJob(data, context)
    elif method == 'getJob':
        return getJob(data, context)
    elif method == 'listDatasets':
        return listDatasets(data, context)
    elif method == 'getDataset':
        return getDataset(data, context)
    else:
        return None

def getOutputImage(event, context):
    jobId = event['jobId']

def submitJob(event, context):
    # Validate configuration object
    configValidator = btr3baseball.ConfigValidator(configObj = event)
    configValidator.validateConfig()

    # Put initial entry in dynamo db
    jobId = jobRepo.createJob(event)

    # Put the job ID on the SQS queue
    response = queue.send_message(MessageBody=jobId)

    # Update the DB entry with sqs message ID for traceability
    return jobRepo.updateWithMessageId(jobId, response.get('MessageId')) 

def validateJob(event, context):
    res = {}

    # Validate configuration object
    configValidator = btr3baseball.ConfigValidator(configObj = event)
    configValidator.validateConfig()

    res['result'] = True
    return res

def getJob(event, context):
    return jobRepo.getJob(event['jobId'])

def listDatasets(event, context):
    return dsRepo.listDatasets()

def getDataset(event, context):
    return dsRepo.getDataset(event['datasourceId'])
