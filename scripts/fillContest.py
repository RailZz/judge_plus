#!/usr/bin/python3
import zipfile
import os
import sys
import random
import string

if '-h' in sys.argv:
    print("""Usage:
contestID""")
print(sys.argv)

probNames = sum([[j + str(i) for j in string.ascii_uppercase] for i in [''] + list(range(10))], [])


#exit()
#problemFile = "/home/ejudge/Downloads/archive_646_93349.zip"
#problemName = "propGraph"
#contestID = "000017"

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
if (len(sys.argv) < 2):
    print('Not enought args')
    exit()

contestID = (6 * '0' + sys.argv[1])[-6:]
index = 1
if len(sys.argv) > 2:
    index = int(sys.argv[2])
print('Now enter ID and checker')
while(1):
    dat = input().split()
    archivePath = os.path.join('/home', 'ejudge', 'archives', 
        'archive_%s.zip' % dat[0])
    zf = zipfile.ZipFile(archivePath)
    #problemName = string.ascii_uppercase[index - 1]
    problemFolder = os.path.join(contestID, 'problems')
    problemName = 'error'
    probIndex = -1
    if not os.path.isdir(problemFolder):
        os.makedirs(problemFolder)
    prev = os.listdir(problemFolder)
    for index, i in enumerate(probNames):
        if i not in prev:
            problemName = i
            probIndex = index + 1
            break
    print('\ncreate problem with {} name and id={}\n'.format(problemName, str(probIndex)))
    
    path = os.path.join(contestID, 'problems', problemName)
    
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        print('Contest already have problem with this ID')
        quit()
        break
    zf.extractall(path)

    probID = probIndex
    servePath = os.path.join(contestID, 'conf', 'serve.cfg')
    serveFile = open(servePath, 'r').read()
    probCfg = problemTemplate
    probCfg += "id = " + str(probID) + '\n'
    probCfg += 'short_name = "{}"\n'.format(problemName)
    if (len(dat) > 1):
        if dat[1] != '-': 
            probCfg += 'standard_checker = "{}"\n'.format(dat[1])
            if 'double' in dat[1]:
                probCfg += 'checker_env = "EPS=1e-3"\n'
        else:
            curPath = os.path.realpath('.')
            os.chdir(path)
            files = os.listdir('.')    
            if 'checker.dpr' in files:
                print('Found checker.dpr, compiling...')
                os.system('cp "/home/ejudge/archives/testlib.pas" ./')
                os.system('fpc checker.dpr > fpcOutput.txt')
                probCfg += 'check_cmd = "checker"\n'
                print('Ok, set non-standart checker')
            elif 'checker.cpp' in files:
                print('Found checker.cpp, compiling...')
                os.system('cp "/home/ejudge/archives/testlib.h" ./')
                os.system('g++ checker.cpp -o checker > gccOutput.txt')
                probCfg += 'check_cmd = "checker"\n'
                print('Ok, set non-standart checker')
            elif 'checker.pas' in files:
                print('Found checker.pas, compiling...')
                os.system('cp "/home/ejudge/archives/testlib.pas" ./')
                os.system('fpc checker.pas > fpcOutput.txt')
                probCfg += 'check_cmd = "checker"\n'
                print('Ok, set non-standart checker')
            else:
                checkPath = os.path.join('/home/ejudge/checkers/', 'checker_{}.cpp'.format(dat[0]))
                if os.path.isfile(checkPath):
                    os.system('cp {} ./'.format(checkPath))
                    os.system('cp "/home/ejudge/archives/testlib.h" ./')
                    os.system('g++ checker_{}.cpp -o checker > gccOutput.txt'.format(dat[0]))
                    probCfg += 'check_cmd = "checker"\n'
                    print('Ok, set non-standart checker')
                else:
                    print('no checker for this problem error path\n', checkPath)

            os.chdir(curPath)

    titlePath = '/home/ejudge/archives/names/' + dat[0]
    if os.path.isfile(titlePath):
        probCfg += 'long_name = "{}"\n'.format(open(titlePath).read().strip())
    open(servePath, 'a').write(probCfg)
    index += 1



