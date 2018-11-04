# import dependencies
import pandas as pd
import os
import sh
import subprocess
import json
import requests
from metrics import *
from difflib import get_close_matches
import re

# set project folder as pwd
cwd = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(cwd)
os.chdir(parent + '/repos')
project_root = os.getcwd()

# test on sample repo
os.chdir(project_root + "/404-NA")
'''
repo_names = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]
for repo in repo_names:
    os.chdir(project_root + "/" + repo)

    # call all metric colletion functions here
    
'''

total_commit_count = get_total_commits()
total_issue_count = get_total_issues()
authors = get_contributing_authors()
commit_contributions = commits_by_each_user()

# final dataframe with all parameters per user
res = pd.DataFrame(columns=['commit count', 'percentage of commits', 'Commit Frequency', 'Files Changed', 'LOC Inserted', 'LOC Deleted'], index=authors)

for contrib in commit_contributions:
    res.loc[contrib[1]]['commit count'] = int(contrib[0])
    res.loc[contrib[1]]['percentage of commits'] = (int(contrib[0]) / total_commit_count) * 100

def file_manipulations():
    with open('../../code/loc.sh') as f:
        line = f.readlines()[0]
        p = subprocess.Popen([line], stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()

        # user, files changed, insertions, deletions
        output = output.decode("utf-8").split("\n")[:-1]
        for opt in output:
            opt_split = [o.strip() for o in opt.split(":")]
            r = re.compile(opt_split[0])
            l = list(filter(r.match, get_contributing_authors()))

            if(len(l) is 0):
                print('author not found')
            else:
                res.loc[l[0]]['Files Changed'] = int(opt_split[1])
                res.loc[l[0]]['LOC Inserted'] = int(opt_split[2])
                res.loc[l[0]]['LOC Deleted'] = int(opt_split[3])

# get number of files changed, insertions and deletions
file_manipulations()

freq = get_commit_frequency()
for k, v in freq.items():
    if v != 0:
        res.loc[k]['Commit Frequency'] = res.loc[k]['commit count'] / v
    else:
        res.loc[k]['Commit Frequency'] = 0

print(res)