# import dependencies
import pandas as pd
import os

# read each project URL from csv file
df = pd.read_csv('../data/Project Update Form.csv', sep=',')
projects = list(df['GitHub link to Repository'])

# set project folder as pwd
cwd = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(cwd)
os.chdir(parent + '/repos')

project_root = os.getcwd()

# clone the project
if len(os.listdir(project_root)) == 0:
    print("Cloning all projects...")
    for project in projects:
        os.system('git clone ' + project)

# pull latest code from the master branch
else:
    print("Pulling latest code from master branch of all projects...")
    repo_names = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]
    for repo in repo_names:
        os.chdir(project_root + "/" + repo)
        os.system("git pull origin master")
