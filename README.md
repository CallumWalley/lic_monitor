This is intended to be a central location for storing information about licence usage on the cluster.
--
## Structure

In this directory is...

### conf/lic.yml
licence information.
### conf/_default_lic.yml
will be used for missing values.
### conf/_lic.yml
Values that diverge from default.


### util/merge_lic.py
`merge_lic.py input1.yml input2.yml output.yml`
merges .yml files. 

### slurm_tokens_from_conf.py
`slurm_token_from_conf.py licences.yml token_1@server token_2@server token_n@server`
Creates/validates slurm token resources.



### merge_lic_wrapper.sh
Merges _lic.ym with _default_lic.yml into lic.yml

### all_slurm_tokens_from_conf.sh
Runs `slurm_tokens_from_conf.py` for all licences.


## Format
Details about keys can be found in _default.yml

## Usage
Currently the conf file here is used b...

### ../Monitoring/monitor_license.py
- Tracks flexlm usage.
### ../ModuleTracker
- Records software (and lic) info.

