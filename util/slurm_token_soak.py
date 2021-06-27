import yaml
import sys
import subprocess
import time
from NeSI.data import prometheus as P


def run_cmd(cmd_str):
    print(f"Running command '{cmd_str}'.")
    time.sleep(3) # No crashing slurm sb allowed
    output = subprocess.check_output(cmd_str.split(" ")).decode().strip()
    return output

args = sys.argv

ld=yaml.load(open(args[1]), Loader=yaml.FullLoader)

update_strings={}

for l in ld:
    for f in l['tracked_features']:
        if f['slurm_soak']:
            try:
                lic_issued = P.query(
                    f"sum(flexlm_licenses_issued{{feature=\"{f['feature_name']}\", owner=\"{l['licence_owner']}\"}})").sum()
                lic_free = P.query(
                    f"sum(flexlm_licenses_free{{feature=\"{f['feature_name']}\", owner=\"{l['licence_owner']}\"}})").sum()
                lic_claimed = lic_issued - lic_free
                print(f"{f['feature_name']}@{l['licence_owner']}: {int(lic_claimed)}/{int(lic_issued)} licenses USED")
                for cluster in l["allowed_clusters"]:
                    tok_claimed = P.query(
                        f"sum(squeue_license_count{{feature=\"{f['feature_name']}\", cluster=\"{cluster}\", owner=\"{l['licence_owner']}\"}})").sum()
                    tok_res = max(lic_claimed - tok_claimed,0)
                    print(f"    {cluster}: {int(tok_claimed)} + ({int(tok_res)}) = {int(lic_claimed)}")
                    if cluster not in update_strings:
                        update_strings[cluster]=""
                    update_strings[cluster]+=f"{f['feature_name']}@{l['licence_owner']}:{int(tok_res)},"

                # For if you feel like doing it the old fasioned way.
                #     total_running = subprocess.check_output(f"squeue -h -M {cluster} --format=\"%u|%C|%t|%r|%S|%N|%W\" -t R -L {f['feature_name']}@{l['licence_owner']}")
            except Exception as e:
                raise Exception(f"Could not get '{f['feature)name']}' total from promethius. Check licence file is up to date and server is up.\n {e}")

for cluster, update_string in update_strings.items():
    reservation_name=f"LicenceSoak_{cluster}"
 
    print(f"Attempting to update {reservation_name}")
    # See if slurmdb needs to be bothered.
    # Ew
    with open(f".{cluster}_res", "r") as last_update_file:
        if last_update_file.read() == update_string:
            print(f"...no change needed.")
            continue
    with open(f".{cluster}_res", "w+") as last_update_file:
        last_update_file.write(update_string)

    try:
        cmd=["scontrol", "update", "-M", cluster, f"ReservationName={reservation_name}","Flags=LICENSE_ONLY",f"licenses={update_string}"]
        #print(" ".join(cmd))
        scntl_out=(subprocess.check_output(cmd).decode().strip())
        print(f"... updated to '{update_string}'")
    except subprocess.CalledProcessError:
        print(" ".join(cmd))
        print("Could not update reservation, attempting to create.")
        cmd=["scontrol", "create", "-M", cluster, f"ReservationName=={reservation_name}","StartTime=now","Duration=infinite","Users=root","Flags=LICENSE_ONLY",f"licenses={update_string}"]
        #print(" ".join(cmd))
        scntl_out=(subprocess.check_output(cmd).decode().strip())
        print(f"... created new reservation with '{update_string}'")
