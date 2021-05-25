#!/bin/bash

module load Python

cd "${BASH_SOURCE%/*}" || exit
./merge_lic.py _default_lic.yml _lic.yml lic.yml lic.json