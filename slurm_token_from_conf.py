import yaml
import math
import sys
import subprocess
import time
from NeSI.data import prometheus as P

def run_cmd(cmd_str):
    print(f"Running command '{cmd_str}'.")
    time.sleep(3)
    output = subprocess.check_output(cmd_str.split(" ")).decode().strip()
    return output

args = sys.argv
with open(args[1]) as licf:
    try:
        feature, owner = args[2].split("@")
    except Exception as e:
        raise f"Could not parse '{args[2]}', should be formatted 'feature@owner'"

    token_name = args[2].lower()
    lics = yaml.load(licf, Loader=yaml.FullLoader)
    feature, owner = token_name.split("@")

    # Pull out the licence this matches from the config. And the server it is on.
    for server in filter(lambda x: 'licence_owner' in x and owner == x['licence_owner'] and 'tracked_features' in x, lics):
        matches = list(filter(lambda x: feature ==
                              x['feature_name'].lower(), server["tracked_features"]))
        if matches:
            conf_server = server
            conf_lic = matches[0]
            if not conf_lic["slurm_track"]:
                raise Exception(
                    f"'{token_name}' is in config, but 'slurm_track' is disabled. Change this.")
            break
    else:
        raise Exception(f"Could not find '{token_name}' in licence conf.")

# Total lic on server.
try:
    total_issued = P.query(
        f"sum(flexlm_licenses_issued{{feature=\"{feature}\", owner=\"{owner}\"}})").sum()
except Exception as e:
    raise Exception(
        f"Could not get '{token_name}' total from promethius. Check licence file is up to date and server is up.\n {e}")

# Converts sacctgr output into dict.
clusters = []
for line in run_cmd("sacctmgr show resource withclusters -np").split("\n"):
    ls = line.split("|")
    if token_name == f"{ls[0]}@{ls[1]}":
        clusters.append(ls[6])

n_clusters = len(conf_server["allowed_clusters"])
percent_allowed = math.floor(100 / n_clusters)  # Must round down.
metatotal = max(math.ceil(100*total_issued/(percent_allowed)),1)



if len(clusters) < n_clusters:
    print(f"'{token_name}' licence doesn't exists. Adding new Licence Token")
    # For each missing cluster run command.
    for cluster in list(set(conf_server["allowed_clusters"]) -  set(clusters)):
        run_cmd(
            f"sacctmgr -i add resource Name={feature} Server={owner} ServerType={conf_server['server_poll_method']} cluster={cluster} percentallowed={percent_allowed} type=License count={metatotal}")
    print(f"'{token_name}' added succesfully.")
else:
    print(f"'{token_name}' licence exists. Checking values")
    run_cmd(
        f"sacctmgr -i modify resource set count={metatotal} where name={feature} server={owner}")
    for cluster in clusters:
        run_cmd(
            f"sacctmgr -i modify resource set percentallowed={percent_allowed} where name={feature} server={owner} cluster={cluster}")
    print(f"'{token_name}' matches config.")
