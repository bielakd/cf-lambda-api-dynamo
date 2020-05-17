echo "---*** Packaging Lambda"
echo $1
BUCKET_NAME=bia-cf-python-aws
S3_KEY=LambdaArtifact
ODW=$PWD

# ----- DO NOT CHANGE BELOW THIS LINE ------------------------------- #
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
S3_BUCKET="$BUCKET_NAME-$ACCOUNT_ID"


#sh ./lambda_package.sh

cd ../target
FILE_NAME=$(ls *:latest.zip)
cd $ODW

KEY="$S3_KEY/$FILE_NAME"
sh ./deployToS3.sh $S3_BUCKET $KEY $FILE_NAME
sh ./deploystack.sh -o $1 $S3_BUCKET $KEY

