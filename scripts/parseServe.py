import os
import argparse
from config import *

def parseServe(contest):
    serve = [i.strip() for i in open('/home/judges/' + getContestNum(contest) + '/conf/serve.cfg').readlines()]
    problems = []
    start_pos = 0
    for i in range(serve.count('[problem]')):
        pos = serve.index('[problem]', start_pos)
        cur_id = int(serve[pos + 1][5:])
        cur_name = serve[pos + 3][13:-1]
        problems.append((cur_id, cur_name))
        start_pos = pos + 1
    return problems


if __name__ == "__main__":
    aparser = argparse.ArgumentParser()
    aparser.add_argument('ejudgeID', help='ejudge contest ID', type=int)
    args = aparser.parse_args()
    print(parseServe(args.ejudgeID))
