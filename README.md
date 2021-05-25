This is intended to be a central location for storing information about licence usage on the cluster.
--
## Structure

In this directory is...

### lic.yml
- licence information.
### _default_lic.yml
- will be used for missing values.
### _lic.yml
- Values that diverge from default.
### merge_lic.py
- merges .yml files.
### merge_lic_wrapper.sh
- Merges _lic.ym with _default_lic.yml into lic.yml


## Format
Details about keys can be found in _default.yml

## Usage
Currently the conf file here is used b...

### ../Monitoring/monitor_license.py
- Tracks flexlm usage.
### ../LicSoak/
- Slurm lic integration
### ../ModuleTracker
- Records software (and lic) info.

