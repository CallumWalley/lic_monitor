#!/bin/bash

module load Python

cd "${BASH_SOURCE%/*}" || exit

cp -v ../conf/_lic.yml ../conf/._lic.yml.bkp
cp -v ../conf/_default_lic.yml ../conf/._default_lic.yml.bkp
cp -v ../conf/lic.yml ../conf/.lic.yml.bkp
cp -v ../conf/lic.json ../conf/.lic.json.bkp

cmd="../util/merge_lic.py ../conf/_default_lic.yml ../conf/_lic.yml ../conf/lic.yml ../conf/lic.json"
echo "$cmd"
$cmd

