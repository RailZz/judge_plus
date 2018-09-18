from config import *
import json

class printInfo:

    def __init__(self):
        pass
    
    @staticmethod
    def printDict(info):     
        print(json.dumps(info, indent=4, sort_keys=True, ensure_ascii=False))
        #tab = '\t'
        #for par in sorted(info.keys()):
        #    print(par, ':', sep = '') 
        #    print(tab, StartContest, ': ', info[par][StartContest], sep = '')
        #    print(tab, Contests, ':',  sep = '')
        #    for c in info[par][Contests]:
        #        print(tab * 2, info[par][Contests], sep = '')
        #    print(tab, Users, ': ', info[par][Users], sep = '')



if __name__ == "__main__":
    info = json.load(open(info_path))
    test = printInfo()
    test.printDict(info)

