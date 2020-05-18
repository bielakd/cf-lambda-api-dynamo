set -e

echo "---*** Packaging Lambda"
echo $1

BUCKET_NAME=bia-cf-python-aws
S3_KEY=LambdaArtifact
ODW=$PWD

# ----- DO NOT CHANGE BELOW THIS LINE ------------------------------- #


# uppercase so that input can be case insensitive

usage() {
  echo "Usage: $0 [<create|update|delete>]" 1>&2
  exit 1
}

ops=$(echo "$1" | tr '/a-z/' '/A-Z/')
echo $ops

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
S3_BUCKET="$BUCKET_NAME-$ACCOUNT_ID"

if [ $ops == "CREATE" ] || [ $ops == "UPDATE" ]; then
  echo "---*** ${ops}ING  STACK"
  sh ./lambda_package.sh

  cd ../target
  FILE_NAME=$(ls *:latest.zip)
  cd $ODW

  KEY="$S3_KEY/$FILE_NAME"
  sh ./deployToS3.sh $S3_BUCKET $KEY $FILE_NAME
  sh ./deploystack.sh -o $1 $S3_BUCKET $KEY
elif [ $ops == "DELETE" ]; then
  echo "---*** DELETING STACK"
  sh ./deploystack.sh -o $1 $S3_BUCKET $KEY
else
  usage
fi




#
#
#sh ./lambda_package.sh
#
#cd ../target
#FILE_NAME=$(ls *:latest.zip)
#cd $ODW
#
#KEY="$S3_KEY/$FILE_NAME"
#sh ./deployToS3.sh $S3_BUCKET $KEY $FILE_NAME
#sh ./deploystack.sh -o $1 $S3_BUCKET $KEY

