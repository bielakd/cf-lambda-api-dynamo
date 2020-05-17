#!/usr/bin/env bash
set -e

echo "---*** Starting deployment of CF Stack"
echo "---*** Setting Variables"

usage() {
  echo "Usage: $0 [-o <create|update|delete>]" 1>&2
  exit 1
}
while getopts ":o:" s; do
  case "${s}" in
  o)
    u=${OPTARG}
    ;;
  *)
    usage
    ;;
  esac
done
# setting the case to UPPER

cd ../cf
check=$(echo "$u" | tr '/a-z/' '/A-Z/')
CF_TEMPLATE=main.yaml
CF_STACK_NAME=CF-PYTHON-API-DYNAMO-EXAMPLE
S3Name=$3
LambdaArtifactKey=$4
echo "$LambdaArtifactKey"

if [ $check == "UPDATE" ]; then
  echo "---*** Starting direct UPDATE"
  echo "---*** Preparing params"

  echo "---*** Executing Stack UPDATE"
  aws cloudformation update-stack --template-body file://$CF_TEMPLATE \
    --parameters ParameterKey=S3BucketName,ParameterValue=$S3Name \
    ParameterKey=LambdaArtifactKey,ParameterValue=$LambdaArtifactKey \
    --stack-name $CF_STACK_NAME \
    --capabilities CAPABILITY_IAM

elif [ $check == "CREATE" ]; then
  echo "---*** Starting CREATE the stack"
  echo "---*** Preparing parameters"
  echo "---*** Executing Stack CREATE"
  aws cloudformation create-stack --template-body file://$CF_TEMPLATE \
    --parameters ParameterKey=S3BucketName,ParameterValue=$S3Name \
    ParameterKey=LambdaArtifactKey,ParameterValue=$LambdaArtifactKey \
    --stack-name $CF_STACK_NAME \
    --capabilities CAPABILITY_IAM

elif [ $check == "DELETE" ]; then
  echo "Deleteing stack $CF_STACK_NAME"
  aws cloudformation delete-stack --stack-name $CF_STACK_NAME
else
  usage
fi
