import os
import os.path

def c(x):
    if x < 10:
        return str(x)
    return chr(ord('A') + x - 10)

def getPath(run):
    first = run // (36 * 36 * 32)
    run %= (36 * 36 * 32)
    second = run // (36 * 32)
    run %= (36 * 32)
    third = run // 32
    return c(first) + '/' + c(second) + '/' + c(third) + '/'

def corr_name(name):
    return ('0' * 6 + str(name))[-6:]

def makeGoodRp(c_id, r_id):
    filename = '/var/www/html/scripts/lastruns/' + c_id + '/' + corr_name(r_id)
    data = open(filename + '.rpt').read()
    if data.find('WA') == -1 and data.find('TL') == -1 and data.find('PE') == -1 and data.find('RT') == -1 and data.find('WTL') == -1:
        if data.find('CE') != -1:
            open(filename + '.rp', 'w').write(data)
        else:
            open(filename + '.rp', 'w').write("OK")
    else:
        wrong_test = data.count('<input')
        pos1 = data.rfind('<input')
        pos2 = data.rfind('<stderr')
        #print(pos1, pos2)
        #print(data[pos1:pos2])
        open(filename + '.rp', 'w').write(data[pos1:pos2])
        open(filename + '.wa', 'w').write(str(wrong_test))

def copyFile(c_id, r_id, fold, ext):
    f_path = getPath(int(r_id))
    path = '/home/judges/' + corr_name(c_id) + '/var/archive/' + fold + f_path + corr_name(r_id)
    print(path)
    n_path = '/var/www/html/scripts/lastruns/' + c_id + '/' + corr_name(r_id)
    if os.path.isfile(path):
        os.system('cp ' + path + ' ' + n_path + ext)
    elif os.path.isfile(path + '.gz'):
        os.system('cp ' + path + '.gz ' + n_path + '.gz')
        os.system('gunzip ' + n_path + '.gz')
        os.system('mv ' + n_path + ' ' + n_path + ext)
    else:
        return False
    if ext =='.rpt':
        makeGoodRp(c_id, r_id)
    return True
        

def copyRuns(contest):
    nextrun = int(open('/var/www/html/scripts/lastruns/' + contest + '.num').readline())
    c_num = int(contest)
    glob_path = '/home/judges/' + ('0' * 6 + contest)[-6:] + '/var/archive/'
    print(glob_path)
    fullp = '/var/www/html/scripts/lastruns/'
    while True:
        c_f = copyFile(contest, str(nextrun), 'runs/', '.code')
        r_f = copyFile(contest, str(nextrun), 'xmlreports/', '.rpt')
        if c_f == False and r_f == False:
            open(fullp + contest + '.num', "w").write(str(nextrun))
            break
        nextrun += 1



contests_data = [i.strip().split('#')[2] for i in open("/var/www/html/scripts/info.txt").readlines()]
contest = []
for i in contests_data:
    contest += [j.split()[0] for j in i.split(',')]
print(contest)
for i in contest:
    filePath = '/var/www/html/scripts/lastruns/' + i + '.num'
    if os.path.isfile(filePath) == False:
        open(filePath, "w").write('0')
        os.system('mkdir /var/www/html/scripts/lastruns/' + i)
    copyRuns(i)
