#!/usr/bin/env python3

# Merges $1 and $2 into $3
# .yml

import sys
import yaml
import json

class log():
    """Placeholder. Should be replaced with actual notification"""
    debug = info = warning = error = print

if __name__ == '__main__':
    if len(sys.argv) < 3: 
        raise Exception("Not enough inputs")
    if sys.argv[1][-4:] != ".yml" or sys.argv[2][-4:] != ".yml":
        raise Exception("Inputs need to be yml files.")

    default_lic = yaml.load(open(sys.argv[1]), Loader=yaml.FullLoader)[0]
    special_lics = yaml.load(open(sys.argv[2]), Loader=yaml.FullLoader)

    default_feature = default_lic["tracked_features"][0]
    combind_lics = list(map(lambda x: {**default_lic, **x}, special_lics))

    # Each tracked feature also needs defaults.
    for lic in combind_lics:
        lic["tracked_features"]=list(map(lambda x: {**default_feature, **x}, lic["tracked_features"]))

    for output in sys.argv[3:]:
        if output[-4:] == ".yml":
            with open(output, "w+") as f: 
                f.write(f"# This file was made by merging '{sys.argv[1]}' and '{sys.argv[1]}'.\n# DONT MAKE CHANGES HERE\n")
                yaml.dump(list(combind_lics), f, sort_keys=True)
        elif output[-5:] == ".json":
            with open(output, "w+") as f: 
                f.write(json.dumps(list(combind_lics),sort_keys=True))
        else:
            raise Exception("Outputs need to be json/yml files.")
