#!/bin/bash
module load Python
while read lic;do 
    echo "'python slurm_token_from_conf.py lic.yml $lic'"
    python slurm_token_from_conf.py lic.yml $lic
    sleep 5
done < <(python - <<-EOF
import yaml
ld=yaml.load(open("lic.yml"), Loader=yaml.FullLoader)
for l in ld:
    for f in l['tracked_features']:
        if f['slurm_track']:
            print(f['feature_name']+'@'+l['licence_owner'])
EOF)