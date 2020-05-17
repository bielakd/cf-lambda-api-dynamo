#!/usr/bin/env bash


#!/usr/bin/env bash
set -e
commit=$(git rev-parse --verify HEAD)
echo "$commit"
echo "--===Starting packaging of Lambda code==---"
echo "@@ Preparing environment|$s $(date -u)"
if [ ! -d "../target" ]; then
  mkdir ../target
fi
cd ../src
rm -rf v-env
python3 -m venv v-env
source v-env/bin/activate
echo "@@ Installing dependencies|$s $(date -u)"
pip install -r ../prod_requirements.txt

echo "@@ Running tests|$s $(date -u)"

pip install -r ../dev_requirements.txt

python -m pytest tests/ -vvv

pip uninstall -r ../dev_requirements.txt -y
deactivate

echo "@@ Packaging...|$s $(date -u)"
OLDPWD=$PWD
cd v-env/lib/python3.7/site-packages
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip app.py
zip -r function.zip dynamo_db
ls


mv function.zip ../target/function:${commit}:latest.zip
FILE_NAME=function:${commit}:latest.zip

for f in ../target/*:latest.zip; do
  if ! [[ $f =~ $commit ]]; then
    mv "$f" "${f%:latest.zip}.zip"
  fi
done
echo "@@ Packaging done...|$s $(date -u)"
echo "$FILE_NAME"