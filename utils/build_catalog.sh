#!/bin/bash

source ./venv/bin/activate
cd ../content/tamus.edu/
oscal-cli profile resolve --overwrite --to=yaml TAMUS_profile.yaml TAMUS_resolved-profile_catalog.yaml
python3 ../../utils/merge_profile_back_matter.py ../texas.gov/TX_DIR_profile.yaml TAMUS_resolved-profile_catalog.yaml --inplace
python3 ../../utils/merge_profile_back_matter.py TAMUS_profile.yaml TAMUS_resolved-profile_catalog.yaml --inplace
cd ../../utils/
deactivate
