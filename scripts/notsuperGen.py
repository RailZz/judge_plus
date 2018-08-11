
import string
import pymysql
import time
import datetime
import os

timeNow = datetime.datetime(123, 1, 1)
timeNow = timeNow.fromtimestamp(time.time())

cellWidth = 35

def getCell(i):
    global timeNow
    if type(i) != type([]):
        strLen = len(str(i))
        if str(i)[0].isdigit():
            return '<td align="center" nowrap width="%s">%s</td>' % (cellWidth, str(i))
        else:
            return '<td align="center" nowrap width="%s" nowrap>%s</td>' % (strLen * 10, str(i))
    res = '<td align="center" nowrap width="%s" {} </td>' % cellWidth
    res = res.format(' title="' + i[3] +  ' - ' + i[4].replace('{}', '') + '" {}')
    #print(res)
    s = '{}'
    #if True or i[2] != -1 and timeNow - i[2] < datetime.timedelta(24 * 60 * 60):
    #res = res.format('bordercolor="0000FF" {}')

    if i[0] != 0:
        if i[0] == 1:
            res = res.format('bgcolor="00FF00"> {}')        
        elif i[0] == 2:
            print('PR', i)
            res = res.format('bgcolor="FFFF00"> {}')        
        else:
            res = res.format('bgcolor="0000FF"> {}')        
        if i[1] > 0:
            if i[1] < 10:
                s = s.format('+{}')
                s = s.format(str(i[1]) + '{}')
            else:
                s = s.format('☹️{}')
        else:
            s = s.format('+{}')
    elif i[1] != 0:
        res = res.format('bgcolor="FF0000"> {}')
        if i[1] < 10:
            s = s.format(' -{}')
            s = s.format(str(i[1]) + '{}')
        else:
            s = s.format('☹️{}')
    else:
        res = res.format('> {}')
        s = s.format(' -{}')
         
    s = s.format('')
    #res = res.format('<table border=1px width="100%" cellpadding="2" cellspacing="1" bordercolor="0000FF">{}</table>')
    if i[2] != -1 and timeNow - i[2] < datetime.timedelta(1):    
        #print('left: {}, right: {}'.format(timeNow - i[2], datetime.timedelta(24)))
        minutes = int((timeNow - i[2]).total_seconds()) // 60
        #color = "0000" + hex(255 - minutes * 256 // (60 * 24)).upper()[-2:]
        cnum = minutes * 2 ** 8 // (60 * 24)
        color = hex(cnum).upper()[-2:] + "0F" + hex(256-cnum).upper()[-2:]
        #print(color, minutes)
        #res = res.format('<table border=2 frame="void" width="100%" cellpadding="2" cellspacing="1" bordercolor="0000FF"><tr><td>{}</td></tr></table>')
        res = res.format('<table border=2 rules="none" width="100%" height="100%" cellpadding="4" cellspacing="1" bordercolor="'+color+'"><tr><td nowrap align="center">{}</td></tr></table>')
    res = res.format(s)
    return res

data = [i.split('#') for i in open('/var/www/html/data/info.txt', 'r').read().split('\n') if i != '']


db = pymysql.connect("localhost", "ejudge", "ejudge", "ejudge", charset="utf8")
cursor = db.cursor()

tables = []

conName = {}
conXml={}

for i in range(5000):
    path = '/home/judges/info/' + str(i)
    if os.path.isfile(path):
        #print(i)
        d = open(path).read().split('\n')
        #print(i, d[1:])
        conXml[i] = {int(i[0]): [i[1], i[2]] for i in [j.split('#') for j in d[1:] if j != '']}
        conName[i] = d[0]
#print(conName, conXml)
for name, logins, contest in data:

    logins = logins.split(',')
    contests = [[int(j) for j in i.split()][0] for i in contest.split(',')]
    marked = [[int(j) for j in i.split()][1:] for i in contest.split(',')]
    
    print(name, logins, contests, marked)

    probnum = sum([len(conXml[i]) for i in contests])
    #print(probnum)
    lines = dict()
    
    usernames = dict()
    for user in logins:
        cursor.execute('select users.username from logins, users where logins.user_id=users.user_id and logins.login="{}"'.format(user))
        username = cursor.fetchall()
        if (len(username) == 0):
            print("can't find user ", user)
            exit(1)
        username = str(username[0][0])
        usernames[user] = username

    for user in logins:
        lines[user] = [0] * probnum

    for user in logins:
        for cnum in contests:
            for probID in conXml[cnum]:
                command = 'select runs.status, runs.create_time from runs, logins where runs.prob_id=%s and runs.user_id=logins.user_id and logins.login="%s" and contest_id="%s" order by runs.create_time' % (probID, user, cnum)
                #print(command)
                cursor.execute(command)
                data = cursor.fetchall()
                #print(user, usernames[user], contests[i][0], data)
                #previous = sum([len(conXml[i]) for i in contests if i < cnum])
                previous = sum([len(conXml[i]) for i in contests[0:contests.index(cnum)]])
                isOK = 0
                attempts = 0
                lastTime = -1
                
                for stat, time in data:
                    if stat == 0:
                        isOK = 1
                    if stat == 16:
                        isOK = 2
                    if stat == 17:
                        isOK = 3
                    if isOK == 0:
                        attempts += 1
                    lastTime = time
                j = sum([1 for i in conXml[cnum] if i < probID])
                #print(user, usernames[user], data, isOK, attempts, lastTime)
                #print(user, previous, j, len(lines[user]), cnum, probID)
                lines[user][previous + j] = [isOK, attempts, lastTime, usernames[user], conXml[cnum][probID][1]]
            
    lines = [[usernames[i],i] + lines[i] for i in lines]
    for j in range(len(lines)):
        #print(lines[j])
        lines[j].append(str(sum([i[0] for i in lines[j] if type(i)==type([]) and i[0] == 1])))
        lines[j].append(str(sum([i[1] for i in lines[j] if type(i)==type([]) and i[0] == 1])))
    #lines = [i for i in lines if any([j[0] != 0 or j[1] != 0 for j in i])]
    #lines = [i for i in lines if any([j[0] != 0 for j in i if type(i) == type([])])]
    lines = [i for i in lines if i[-2] != '0']
    lines.sort(key = lambda x : (-int(x[-2]), int(x[-1])))
   
    letter = name[-1]
    link = ''
    if letter in 'ABCD':
        link = 'index' + letter + '.html'
    
    wrapCell = lambda x , args='': '<td ' + args + ' >' + x +  '</td>'
    header = [wrapCell(i) for i in ['Имя', 'login']]
    
    for ci, i in enumerate(contests):
        task_nums = open('/home/judges/nums/'+str(i)).readline().split('#')
        for j in conXml[i]:
            clr = 'FFFFFF'
            if j in marked[ci]:
                clr = '77FFFF'
            #print(conXml[i])
            #print(task_nums, j, len(task_nums))
            header.append(wrapCell('<a href="' + task_nums[0] + '#ch' + task_nums[j] + '" target="_blank">' + conXml[i][j][0] + '</a>', 'bgcolor="' + clr + '"'))

    header.append(wrapCell('sum')) 
    header.append(wrapCell('штраф'))
    realHeader = '<tr align="center">' + ' '.join(header) + '</tr>'
    #print(realHeader)
    table = lines
    #print(*table, sep = '\n')
    ch = '<tr>{}</tr>' 
    ch = ch.format('<td colspan=2 align="center"> <b> <a href="' + link + '" target="_blank">'+ name + '</a> </b> </td> {}')
    for i in contests:
        cntName = conName[i]
        if cntName.lower().startswith('парал'):
            cntName = cntName[cntName.index('.') + 1:].strip()
        link = '/new-client?contest_id=' + str(i)
        #print(i, conXml)
        cell = '<td colspan=' + str(len(conXml[i])) + ' align="center">{}</td>'
        cell = cell.format('<a href="' + link + '" target="_blank">{}</a>')
        cell = cell.format(cntName)
        ch = ch.format(cell + '{}')
    
    ch = ch.format('')
    p = ch + realHeader + '\n'.join(['<tr height="35">' + ''.join([getCell(i) for i in line]) + '</tr>\n' for line in table])
    tables.append("<table border=1>\n %s \n</table>\n" % p)

fullTable = ''.join(tables)
template = """
<html>
<head>
    <title>Таблица результатов</title>
</head>
<body>

%s

</body>
</html>
""" % (fullTable)
open('/var/www/html/data/standings.htm', 'w').write(template)

let = 'ABCD'
for i in range(4):
    template = """
    <html>
    <head>
        <title>Таблица результатов """ + let[i] + """</title>
    </head>
    <body>
    
    %s
    
    </body>
    </html>
    """
    template = template % tables[i]
    fileWay = '/var/www/html/data/standings' + let[i] + '.htm'
    open(fileWay, 'w').write(template)
