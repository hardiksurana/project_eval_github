# import dependencies
import pandas as pd
import os
import sh
import subprocess

# read each project URL from csv file

# clone the project and pull the master branch

# get total number of commits and issues

# get list of all contributing authors
# git log --format='%aN' | sort -u

# get number of files changed, insertions and deletions
p = subprocess.Popen(['./test.sh'], stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
print(output)