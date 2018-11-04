Data Analytics Project Evaluation using Github Metrics as Key Performance Indicators (KPIs)

# Instructions
1. Clone the repository
2. Add the csv file with all github project repo URLs in ```data/``` folder
3. Run ```code/update_repos.py``` to clone/pull latest changes in each repository
4. Run ```code/get_stats.py``` to print all metrics on terminal and store results in ```output/``` folder

# Metrics
### Overall Indicators
total number of:
- commits
- issues

### Per Student Indicators 
1. % of commits
project contribution distribution
how well did they use version control

2. Use of Version Control
lesser % commits -> check LOC. if more, poor usage (bulk edits), if less, good usage (granular)
more % of commits -> check LOC. if more, poor usage (bulk edits), if less, good usage (granular)

3. commit frequency
shows consistency of contribution

4. % of issues assigned
how well were the tasks distributed amongst members

5. average time spent per issue - lead time
time between when issue was opened and closed
lesser lead time, better is the member's efficiency

6. total time spent on all issues - coding hours
total contribution in terms of time

7. average importance of an issue - code churn
It is the percentage of a developer’s own code representing an edit to their own recent work. 
LOC - modified, added and deleted
number of files edited

# PS
- ignore changes in dataset files (.csv etc)
- Files matching MIME type image, binary should be ignored