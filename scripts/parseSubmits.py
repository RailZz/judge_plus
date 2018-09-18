from config import *
import json
import pickle
###############################
# submits data json
# Список посылок, посылка:
#0   contestID
#1   problemID
#2   runID
#3   uid: -- user ejudge ID
#4   result
#5   time 

# Deprecated
#   [codePath] -- путь к файлу с кодом из корня /
#   [reportPath]
#   [FullReportPath]
#
 
#TODO try increase perfomance changing few execute to one with big statement

def parseSubmits():
    info = json.load(open(info_path))
    # assume that all submits from given contest are neccecary

    result = []

    import pymysql
    db = pymysql.connect("localhost", "ejudge", "ejudge", "ejudge", charset="utf8")
    cursor = db.cursor()
    data = []
    for parallel in info:
        for contest in info[parallel]["Contests"]:
            cursor.execute('select runs.contest_id, runs.prob_id,  runs.run_id, runs.user_id, runs.status, runs.create_time from logins, users, runs where logins.user_id=users.user_id and logins.user_id=runs.user_id and runs.user_id != 1 and runs.contest_id=' + str(contest["EjudgeID"]))
            data += [i for i in cursor.fetchall()]



    data.sort(key=lambda x : x[5], reverse=True) # sort by time, newest at begining

    pickle.dump(data, open(submits_path, 'wb'))
    # print(*data, sep = '\n')