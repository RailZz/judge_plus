#!/usr/bin/python3
from config import contest_trash_directory, info_path, getContestNum
import json
import os

def deleteContest(ejudgeID):
    print(""" !!!!!!!!!!!!!!!!
You are going to delete contest {}
Retype contest number to confirm operation: """.format(ejudgeID))

    confirmed_EjudgeID = int(input())

    if confirmed_EjudgeID != ejudgeID:
        print("Operation canceled")
        return
    else:
        print("Deleting contest {}...".format(ejudgeID))

    info = json.load(open(info_path))

    contest_info_backup = None

    for parallel in info:
        for index, contest in enumerate(info[parallel]["Contests"]):
            if contest["EjudgeID"] == ejudgeID:
                contest_info_backup = contest
                info[parallel]["Contests"].pop(index)
                break
    if contest_info_backup is None:
        raise Exception("no contest with ejudgeID=" + str(ejudgeID))
    json.dump(info, open(info_path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
    contestNum = getContestNum(ejudgeID)

    json.dump(contest_info_backup, open(os.path.join(contest_trash_directory, contestNum + '.info.json'), 'w'))

    os.system('mv "{}" "{}"'.format(
        os.path.join("/home/judges/", contestNum),
        contest_trash_directory))
    
    os.system('mv "{}" "{}"'.format(
        os.path.join("/home/judges/data/contests/", contestNum + '.xml'),
        contest_trash_directory))

    

    print('Ok, moved all to ' + contest_trash_directory)


if __name__ == "__main__":
    import argparse

    aparser = argparse.ArgumentParser()
    aparser.add_argument('ejudgeID', help="ejudge contest ID", type=int)
    args = aparser.parse_args()
    deleteContest(args.ejudgeID)