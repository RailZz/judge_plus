#!/usr/bin/python3

from config import archive_directory, checkers_directory, standart_checker_directory, problem_name_directory
import os
import zipfile



#
# Чекеры:
# * Стандартные (cmp_long_long и т. п.) -- standart
# * Встроенные в архив 
# * Самописные -- custom




class Problem:
    archive_checker_type = "archive checker"
    standart_checker_type = "standart checker"
    custom_checker_type = "custom checker"
    no_checker_type = "no checker"

    def __init__(self, problemID):
        self.problemID = problemID
        self.name = None
        self.name_path = None
        self.checker_type = None
        self.checker_path = None
        self.checker_description = None
        self.archive_path = None
        self.archive_exists = None

    def get_archive_path(self):
        if self.archive_path is None:
            self.archive_path = os.path.join(archive_directory, 
                'archive_{}.zip'.format(self.problemID))
        return self.archive_path

    def check_archive_exists(self):
        if self.archive_exists is None:
            self.archive_exists = os.path.isfile(self.get_archive_path())
        return self.archive_exists

    def check_checker_in_archive(self):
        arhive_path = self.get_archive_path()
        zf = [i.filename for i in zipfile.ZipFile(open(arhive_path, 'rb')).filelist if i.filename.lower().startswith('checker')]
        if 'checker.dpr' in zf:
            return True
        if 'checkerNone' in zf:
            return False
        print("Unexpected type of checker in archive")
        exit(1)
        

    def get_custom_checker_path(self):
        return os.path.join(checkers_directory, "checker_{}.cpp".format(self.problemID))

    def check_checker_custom(self):
        return os.path.isfile(self.get_custom_checker_path())
        
    def get_standart_checker_path(self):
        return os.path.join(standart_checker_directory, str(self.problemID))

    def check_standart_checker(self):
        return os.path.isfile(self.get_standart_checker_path())

    def check_checker_exists(self, comment=False):
        """
        This functions assumes that archive exists
        """
        if self.checker_type is None:
            if self.check_standart_checker():
                self.checker_path = self.get_standart_checker_path()
                self.checker_type = Problem.standart_checker_type
                self.checker_description = open(self.checker_path).read()
                return
            if self.check_checker_in_archive():
                self.checker_path = self.get_archive_path()
                self.checker_type = Problem.archive_checker_type
                self.checker_description = None
                return

            if self.check_checker_custom():
                self.checker_path = self.get_custom_checker_path()
                self.checker_type = Problem.custom_checker_type
                self.checker_description = None
                return
            self.checker_type = Problem.no_checker_type
        return self.checker_type != Problem.no_checker_type

    def check_problem(self):
        return self.check_archive_exists() and self.check_checker_exists() and self.check_name_exists()

    def get_problem_info(self):
        s = ""
        s += "informatics ID: {}\n".format(self.problemID)
        if self.check_archive_exists():
            s += "Have archive; "
            self.check_checker_exists()
            s += self.checker_type
            if self.checker_description is not None:
                s += "; " + self.checker_description
            s += '\n'
        else:
            s += "No archive\n"
        if self.check_name_exists():
            s += 'Problem name: "{}"\n'.format(self.get_name())
        return s

    def get_problem_name_path(self):
        if self.name_path is None:
            self.name_path = os.path.join(problem_name_directory, str(self.problemID))
        return self.name_path    


    def check_name_exists(self):
        return os.path.isfile(self.get_problem_name_path())

    def get_name(self):
        if self.name is None:
            if self.check_name_exists():
                self.name = open(self.get_problem_name_path()).read()
            else:
                self.name = ""
        return self.name

    


def save_standart_checkers_from_stdin():
    while True:
        prob, checker = input().split()
        
        if not prob.isdigit():
            print(prob, "not a number")
            continue
        prob = int(prob)
        problem = Problem(prob)
        if problem.check_checker_exists():
            if problem.checker_type == Problem.standart_checker_type:
                if problem.checker_description != checker:
                    print("Previous checker differ for", prob, ": had ", problem.checker_description, "found new", checker)
                    print('Please check it manually')
                else:
                    print("Have same for", prob)
            else:
                print('Already have ' + problem.checker_type) 
        else:
            open(problem.get_standart_checker_path(), 'w').write(checker)
            print('save new checker for', prob)
    
def check_problems_exists_from_stdin():
    while True:
        prob = int(input())
        print(Problem(prob).get_problem_info())

if __name__ == "__main__":
    import argparse

    aparser = argparse.ArgumentParser()
    aparser.add_argument('-save-checkers', help='Save standart checkers from stdin', action="store_true")
    aparser.add_argument('-check', help='Check problems', action="store_true")
    args = aparser.parse_args()
    
    if args.save_checkers:
        save_standart_checkers_from_stdin()

    if args.check:
        check_problems_exists_from_stdin()

    #save_standart_checkers_from_stdin()
    #check_problems_exists_from_stdin()

    aparser.print_help()
    exit(0)
