# import dependencies
import json
from metrics import *
import os
import pandas as pd
import re
import requests
import sh
import subprocess
from tabulate import tabulate

def file_manipulations():
    with open('../../code/loc.sh') as f:
        line = f.readlines()[0]
        p = subprocess.Popen([line], stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()

        # user, files changed, insertions, deletions
        output = output.decode("utf-8").split("\n")[:-1]
        for opt in output:
            opt_split = [o.strip() for o in opt.split(":")]

            l = []

            for author in get_contributing_authors():
                if(opt_split[0][:-1] in author):
                    l.append(author)
            # r = re.compile(opt_split[0])
            # l = list(filter(r.match, get_contributing_authors()))

            if(len(l) is 0):
                print('{0} - author not found'.format(opt_split[0]))
            else:
                res.loc[l[0]]['Files Changed'] = int(opt_split[1])
                res.loc[l[0]]['LOC Inserted'] = int(opt_split[2])
                res.loc[l[0]]['LOC Deleted'] = int(opt_split[3])


# set project folder as current working directory
cwd = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(cwd)
os.chdir(parent + '/repos')
project_root = os.getcwd()

# get names of all repositories
repo_names = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]
print(repo_names)

for repo in repo_names:
    # enter into project's directory
    os.chdir(project_root + "/" + repo)

    # call all metric colletion functions here
    total_commit_count = get_total_commits()
    authors = get_contributing_authors()
    commit_contributions = commits_by_each_user()

    # final dataframe with all parameters per user
    res = pd.DataFrame(columns=['commit count', 'percentage of commits', 'Commit Frequency', 'Issue Count', 'Percentage of issues', 'Files Changed', 'LOC Inserted', 'LOC Deleted'], index=authors)

    for contrib in commit_contributions:
        res.loc[contrib[1]]['commit count'] = int(contrib[0])
        res.loc[contrib[1]]['percentage of commits'] = (int(contrib[0]) / total_commit_count) * 100

    # get commit frequency - number of commits per week
    freq = get_commit_frequency()
    for k, v in freq.items():
        if v != 0:
            res.loc[k]['Commit Frequency'] = res.loc[k]['commit count'] / v
        else:
            res.loc[k]['Commit Frequency'] = 0

    # get total number of issues
    df = pd.read_csv('../../data/Project Update Form.csv')
    repo_link = df[df['GitHub link to Repository'].str.contains(repo)]['GitHub link to Repository'].values[0]

    if 'https://github.com/' in repo_link:
        owner, repo_name = repo_link.replace('https://github.com/', '').split('/')
    elif 'https://gitlab.com/' in repo_link:
        owner, repo_name = repo_link.replace('https://gitlab.com/', '').split('/')

    total_issue_count = get_total_issues(owner, repo_name)

    # get issues assigned to a user
    for author in authors:
        total_issue_count_by_user = get_issues_by_user(owner, repo_name, author)
        res.loc[author]['Issue Count'] = total_issue_count_by_user

        if total_issue_count != 0:
            res.loc[author]['Percentage of issues'] = total_issue_count_by_user / total_issue_count
        else:
            res.loc[author]['Percentage of issues'] = 0
    
    # get number of files changed, insertions and deletions
    file_manipulations()

    # display results
    print('\n\n\n')
    print('-' * 200)
    print("Repository Name = ", repo)
    print("Repository URL = ", repo_link)
    print('Authors = ' , authors)
    print('Total #commits = ', total_commit_count)
    print('Total #issues = ', total_issue_count)
    print(tabulate(res, headers='keys', tablefmt='psql'))
    print('-' * 200)

    res.to_csv('../../output/' + repo + '.csv')