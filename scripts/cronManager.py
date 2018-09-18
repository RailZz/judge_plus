#!/usr/bin/python3



def launchCron():
    from datetime import datetime
    time1 = datetime.now()
    
    from parseSubmits import parseSubmits
    from generateStatements import generateStatements
    from config import script_directory
    

    parseSubmits()
    generateStatements()
    import updateSource
    import lastGen
    time2 = datetime.now()
    open(script_directory + 'cronlog.txt', 'a').write(str(time2) + ' ' + str(time2 - time1) + '\n')




if __name__ == "__main__":
    launchCron()