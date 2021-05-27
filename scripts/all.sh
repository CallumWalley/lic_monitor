#!/bin/bash -e
module load Python/3.9.5-gimkl-2020a

cd "${BASH_SOURCE%/*}" || exit

echo "Merging..."
./merge_lic_wrapper.sh
echo "Checking tokens..."
./all_slurm_token_from_conf.sh
echo "Starting Soak"
python slurm_token_soak.py