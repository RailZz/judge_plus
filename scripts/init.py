import json
from config import *
import sys

if __name__ == "__main__":
    info = json.load(open(info_path))
    pars = sys.argv
    len_pars = len(pars)
    for i in range(2, len_pars, 2):
        info[pars[i]] = {}
        info[pars[i]][StartContest] = int(pars[i + 1])
        info[pars[i]][RegisterContest] = int(pars[1])
        info[pars[i]][Contests] = []
        info[pars[i]][HTMLComment] = ""
        info[pars[i]][Users] = []
    json.dump(info, open(info_path, 'w'))
