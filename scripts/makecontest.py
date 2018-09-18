
from parsestatements import StatementsParser
from manager import Problem
import logging
import string
import json
from config import *
import os 
import zipfile
from printInfo import printInfo
from setcontestname import setContestXML
from UpdateHTML import genHTML

printDict = printInfo.printDict

logging.basicConfig(level = logging.INFO)

class ContestMaker:
    problemTemplate = """[problem]
type = "standard"
scoring_checker = 0
interactive_valuer = 0
manual_checking = 0
check_presentation = 0
use_stdin
input_file = "input.txt"
combined_stdin
use_stdout
output_file = "output.txt"
combined_stdout
binary_input = 0
ignore_exit_code = 0
test_sfx = ""
test_pat = "%02d"
use_corr
corr_sfx = ""
corr_pat = "%02d.a"
use_info = 0
info_sfx = ""
info_pat = ""
use_tgz = 0
tgz_sfx = ""
tgz_pat = ""
tgzdir_sfx = ""
tgzdir_pat = ""
autoassign_variants = 0
disable_auto_testing = 0
disable_testing = 0
enable_compilation = 0
valuer_sets_marked = 0
disable_stderr = 0
normalization = "nl"
time_limit_millis = 2000
real_time_limit = 5
max_vm_size = 256M
max_stack_size = 256M
enable_text_form
"""
    def __init__(self, ejudgeID, statements_path, par = None, num = None):
        self.ejudgeID = ejudgeID
        self.LETTERS = list(string.ascii_uppercase) +  sum([[fl + sl for sl in string.ascii_uppercase] for fl in string.ascii_uppercase], [])
        statements_filename = os.path.split(statements_path)[-1] 
        info = json.load(open(info_path))
        if par is None:
            best_contest = None
            for p in sorted(info.keys()):
                if int(info[p][StartContest]) <= self.ejudgeID:
                    if par is None:
                        par = p
                        best_contest = int(info[p][StartContest])
                    elif int(info[p][StartContest]) > best_contest:
                        par = p
                        best_contest = int(info[p][StartContest])
            if par is None:
                par = 'S'
        if num is None:
            nm = statements_filename[1:].split('.')[0]
            if not nm.isdigit():
                raise Exception("contest number is not specified")
            num = int(nm)
        self.parallel = par
        self.registerContest = info[self.parallel][RegisterContest]
        self.contestNum = num
        self.strEjudgeID = (6 * '0' + str(ejudgeID))[-6:]
        self.statements_path = statements_path
        self.serveConfigPath = os.path.join('/home/judges', self.strEjudgeID, 'conf', 'serve.cfg')

    def process(self):
        self.statement_parser = StatementsParser(path=self.statements_path, apply=False)
        
        self.name = self.statement_parser.get_contest_name() 

        self.problems = []
        for problemID in self.statement_parser.task_nums:
            self.problems.append(Problem(problemID))
        
        print('\n'.join([i.get_problem_info() for i in self.problems]))
        if not all([i.check_problem() for i in self.problems]):
            print('Not all problems are ready, exiting')
            return False

        problemFolder = os.path.join('/home/judges', self.strEjudgeID, 'problems')
        if not os.path.isdir(problemFolder):
            os.makedirs(problemFolder)
        
        previous_problems = os.listdir(problemFolder)
        if len(previous_problems) > 0:
            print("Some garbage (or previous problems) detected, exiting")
            return False
        
        self.statement_parser.apply()

#def setContestXML(contest, name, registerContest = None, name_en = 'Contest'):        

        setContestXML(contest=self.ejudgeID, 
            name='Группа ' + self.parallel + '. ' + self.name, 
            name_en="Contest. Parallel " + self.parallel,
            registerContest=self.registerContest)


        for index, prob in enumerate(self.problems):
            self.add_problem(prob, index + 1)

        statement_name = self.parallel + str(self.contestNum) + '.htm'
        self.data_statements_path = os.path.join(html_directory, statement_name)
        os.system('cp "{}" "{}"'.format(self.statements_path, self.data_statements_path))
        self.statement_link = statement_name
        return True

    

    def add_problem(self, problem, probID):
        problemName = self.LETTERS[probID - 1]
        problemPath = os.path.join('/home/judges', self.strEjudgeID, 'problems', problemName)
        if not os.path.isdir(problemPath):
            os.makedirs(problemPath)
        else:
            raise Exception('problem already set')
        zipfile.ZipFile(problem.archive_path).extractall(problemPath)    
        problem.ejudgeID = probID
        problem.problemLetter = problemName
        probCfg = ContestMaker.problemTemplate
        probCfg += "id = " + str(probID) + '\n'
        probCfg += 'short_name = "{}"\n'.format(problemName)
        if problem.checker_type == Problem.standart_checker_type: 
            probCfg += 'standard_checker = "{}"\n'.format(problem.checker_description)
            if 'double' in problem.checker_description:
                probCfg += 'checker_env = "EPS=1e-3"\n'
        else:
            curPath = os.path.realpath('.')
            os.chdir(problemPath)
            files = os.listdir('.')    
            if problem.checker_type == Problem.archive_checker_type:
                if 'checker.dpr' in files:
                    logging.info('Found checker.dpr, compiling...')
                    os.system('cp "/home/ejudge/archives/testlib.pas" ./')
                    os.system('fpc checker.dpr > fpcOutput.txt')
                    probCfg += 'check_cmd = "checker"\n'
                    logging.info('Ok, set non-standart checker')
                elif 'checker.cpp' in files:
                    logging.info('Found checker.cpp, compiling...')
                    os.system('cp "/home/ejudge/archives/testlib.h" ./')
                    os.system('g++ checker.cpp -o checker > gccOutput.txt')
                    probCfg += 'check_cmd = "checker"\n'
                    logging.info('Ok, set non-standart checker')
                elif 'checker.pas' in files:
                    logging.info('Found checker.pas, compiling...')
                    os.system('cp "/home/ejudge/archives/testlib.pas" ./')
                    os.system('fpc checker.pas > fpcOutput.txt')
                    probCfg += 'check_cmd = "checker"\n'
                    logging.info('Ok, set non-standart checker')
            elif problem.checker_type == Problem.custom_checker_type:
                os.system('cp {} ./'.format(problem.checker_path))
                os.system('cp "/home/ejudge/archives/testlib.h" ./')
                os.system('g++ {} -o checker > gccOutput.txt'.format(problem.checker_path))
                probCfg += 'check_cmd = "checker"\n'
                logging.info('Ok, set non-standart checker')
            else:
                logging.error("No checker for problem\n" + problem.get_problem_info())
            os.chdir(curPath)

        if problem.name is not None:
            probCfg += 'long_name = "{}"\n'.format(problem.name)
        open(self.serveConfigPath, 'a').write(probCfg)
    
    def getJSON(self):
        d = {"EjudgeID": self.ejudgeID, "ContestName": self.name, "StatementLink": self.statement_link}
        d["Problems"] = [i.getJSON() for i in self.problems]
        return d
        

def makeContest(ejudgeID, statement_path):
    logging.info('starting make contest')
    contestmaker = ContestMaker(ejudgeID, statement_path)
    if contestmaker.process():
        info = json.load(open(info_path))
        if contestmaker.parallel not in info:
            raise Exception("run init for info.json first")
        info[contestmaker.parallel]["Contests"].append(contestmaker.getJSON())
        printDict(info)
        json.dump(info, open(info_path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
        genHTML()
    else:
        logging.error('failed')


##############################################
#  info.json structure
# "буква параллели": Лежат параллели. Параллель содержит:
    # Contests: Список контестов. Контест содержит:
        # EjudgeID: Номер контеста в ejudge ()
        # ContestName: Название контеста
        # Problems: список задач
            # EjudgeID: ID задач в ejudge
            # InformaticsID: ID задач в информатиксе
            # Name: Названия задач
            # Letter: буква в условии
        # StatementLink: Ссылки на условия (относительно корня html)
    # HTMLComment: Что будет написано внизу странички html
    # users: список юзеров
        # login -- логин в ejudge
        # name: ФИ
        # uid: ejudge user ID
        # group: название группы
#

if __name__ == "__main__":
    import argparse
    aparser = argparse.ArgumentParser()
    aparser.add_argument('ejudgeID', help="ejudge contest ID", type=int)
    aparser.add_argument('statementPath', help="statement's path", type=str)

    args = aparser.parse_args()
    makeContest(args.ejudgeID, args.statementPath)
