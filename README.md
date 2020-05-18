# General

This repository contains CloudFormation templates and bash scripts to  
create the following resources:
* S3 bucket - this serves as the artifactory 
* DynamoDB Table - very simple table.
* Lambda  - to insert data to DynamoDB and return the same data element
* API Gateway - to call the Lambda and return the json message.

## Structure:
`cf` here are the CloudForamtion scritps used in this deployment
`scripts` here are the deployment scripts
`src` codebase and tests

## Deployment 
From scripts run the following command
* To Create `./main.sh create`
* To Update `./main.sh update`
* To Delete `./main.sh delete`


CREATE:
* packages the lambda code and stores the function in the `target` directory
* creates the S3 Artifactory bucket and pushes the artifact to this location
* creates the main stack (DynamoDb, Lambda, Api Gateway)

UPDATE:
* packages the code
* deploys artifact to the S3 bucket
* updates main stack

DELETE
* removes the main stack

## Notes
This is very brute force and can benefit from lots of improvements
* API allows any user to access it - no authentication and authorization in place
* API does not require API Key, as one is not created.
* API does not have any usage plans in place.
* Policies can be restricted further. 