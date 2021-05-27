#!/bin/bash
module load Python

cd "${BASH_SOURCE%/*}" || exit


while read lic;do 
    echo "'python slurm_token_from_conf.py lic.yml $lic'"
    python ../util/slurm_token_from_conf.py ../conf/lic.yml $lic
    sleep 5
done < <(python - <<-EOF
import yaml
ld=yaml.load(open("../conf/lic.yml"), Loader=yaml.FullLoader)
for l in ld:
    for f in l['tracked_features']:
        if f['slurm_track']:
            print(f['feature_name']+'@'+l['licence_owner'])
EOF)