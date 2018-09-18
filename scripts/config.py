
script_directory = "/home/judges/judge_plus/scripts/"
data_directory = "/home/judges/judge_plus/data/"
info_path = "/home/judges/judge_plus/data/info.json"
html_directory = "/home/judges/judge_plus/data/html/"
archive_directory = "/home/ejudge/archives/" 
problem_name_directory = "/home/ejudge/archives/names" 
checkers_directory = "/home/ejudge/checkers/"
standart_checker_directory = "/home/judges/judge_plus/data/standart_checkers"
Contests = "Contests"
StartContest = "StartContest"
StatementLink = "StatementLink"
Users = "Users"
HTMLComment = "HTMLComment"
EjudgeID = "EjudgeID"
InformaticsID = "InformaticsID"
RegisterContest = "RegisterContest"
Name = "Name"
Problems = "Problems"
ContestName = "ContestName"
Letter = "Letter"
submits_path = "/home/judges/judge_plus/data/submits.json"
lastruns_path = "/home/judges/judge_plus/data/html/lastruns/"
contest_trash_directory = "/home/judges/contestTrash/"


def getContestNum(contest, sz = 6):
    return ('0' * sz + str(contest))[-sz:]
