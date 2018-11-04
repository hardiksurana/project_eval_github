import subprocess
import re
from datetime import datetime

# get total number of commits 
def get_total_commits():
    p = subprocess.Popen("git rev-list --count HEAD", stdout = subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    total_commit_count = int(output.decode("utf-8").split("\n")[0])
    return total_commit_count

# get total number of issues
def get_total_issues():
    return 0

# get list of all contributing authors
def get_contributing_authors():
    p = subprocess.Popen("git log --format='%aN' | sort -u", stdout = subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    authors = output.decode("utf-8").split("\n")[:-1]
    return authors

# find commits made by each user
def commits_by_each_user():
    p = subprocess.Popen("git shortlog -s -n --all --no-merges", stdout = subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    commit_contributions = output.decode("utf-8").split("\n")
    commit_contributions = [contrib.strip().split("\t") for contrib in commit_contributions][:-1]
    return commit_contributions

def get_commit_frequency():
    authors = get_contributing_authors()
    freq = {}
    for author in authors:
        p = subprocess.Popen("git log --pretty='%ct' --author='" + author + "'", stdout = subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        opt = output.decode("utf-8").split("\n")[:-1]
        first = datetime.utcfromtimestamp(int(opt[-1])).strftime('%Y-%m-%d')
        first = datetime.strptime(first, "%Y-%m-%d")
        last = datetime.utcfromtimestamp(int(opt[0])).strftime('%Y-%m-%d')
        last = datetime.strptime(last, "%Y-%m-%d")
        freq[author] = int((last-first).days / 7)
    return freq

