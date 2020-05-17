echo "DEPLOYING TO S3"
set -e

cd ../target

echo $1
echo $2
echo $3
# Setting required variables

CF_TEMPLATE=stack/s3.yaml
CF_STACK_NAME=S3-ARTIFACTORY

S3_BUCKET=$1
KEY=$2
FILE_NAME=$3


echo "$S3_BUCKET"

echo "Checking if $S3_BUCKET Exists"
echo $(aws s3 ls "s3://$S3_BUCKET")
if aws s3 ls "s3://$S3_BUCKET" 2>&1 | grep -q "NoSuchBucket" ; then
  cd ../cf
  echo "---*** Trying to create bucket stack"
  aws cloudformation create-stack --template-body file://$CF_TEMPLATE \
  --stack-name $CF_STACK_NAME \
  --parameters ParameterKey=BucketName,ParameterValue=$S3_BUCKET || \
  echo "---*** Trying to update stack" \ ||
  aws cloudformation update-stack --template-body file://$CF_TEMPLATE \
  --stack-name $CF_STACK_NAME \
  --parameters ParameterKey=BucketName,ParameterValue=$S3_BUCKET || \
  echo "---*** DELETING STACK" \ ||
  aws cloudformation delete-stack --stack-name $CF_STACK_NAME || \
  echo "---*** Finally creating stack" \ ||
  aws cloudformation stack-delete-complete --stack-name $CF_STACK_NAME ||
  aws cloudformation create-stack --template-body file://$CF_TEMPLATE \
  --stack-name $CF_STACK_NAME \
  --parameters ParameterKey=BucketName,ParameterValue=$S3_BUCKET
  cd ../target
fi

echo "---*** Checking if bucket exists"
aws s3api wait bucket-exists --bucket $S3_BUCKET
echo "---*** $S3_BUCKET is ALIVE!!!!"
aws s3api put-object \
--bucket $S3_BUCKET \
--key $KEY \
--body "./$FILE_NAME"

echo "---*** Deploying stack to S3"
cd ../cf
aws s3 cp --recursive stack "s3://$S3_BUCKET/stack"

echo $KEY



