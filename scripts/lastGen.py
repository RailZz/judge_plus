import time

import string
# import pymysql
import time
import datetime

import os
import os.path

import json

from config import *

import pickle

# db = pymysql.connect("localhost", "ejudge", "ejudge", "ejudge", charset="utf8")
# cursor = db.cursor()


#par = ['A', 'B', 'C', 'D']

# cursor.execute('select logins.login, users.username, runs.contest_id, runs.prob_id, runs.status, runs.run_id, runs.create_time from logins, users, runs where logins.user_id=users.user_id and logins.user_id=runs.user_id and runs.user_id != 1 order by -runs.create_time LIMIT 400')

# data = cursor.fetchall()
#print(*data, sep = '\n')

info = json.load(open(info_path))
par = list(sorted(info.keys()))
full_pars = {}
full_links = {}
full_data = {}
names = {}
stat_link = {}
for p in par:
    for c in info[p][Contests]:
        full_pars[c[EjudgeID]] = p
        stat_link[c[EjudgeID]] = c[StatementLink]
        full_links[c[EjudgeID]] = []
        full_data[c[EjudgeID]] = []
        names[c[EjudgeID]] = 'Параллель ' + p + ': ' + c[ContestName]
        for prob in c[Problems]:
            full_links[c[EjudgeID]].append(str(prob[InformaticsID]))
            let = ''
            if Letter not in prob.keys():
                let = chr(ord('A') + prob[EjudgeID])
            else:
                let = prob[Letter]
            full_data[c[EjudgeID]].append((prob[EjudgeID], let, prob[Name]))

template = """
<html>
<head>
<title>Последние посылки</title>
<style type="text/css">
   BODY {
    background: white; /* Цвет фона веб-страницы */
   }
   TABLE {
    /*width: 300px;*/ /* Ширина таблицы */
    border-collapse: collapse; /* Убираем двойные линии между ячейками */
   }
   TD, TH {
    padding: 3px; /* Поля вокруг содержимого таблицы */
    border: 1px solid maroon; /* Параметры рамки */
    text-align: left; /* Выравнивание по левому краю */
   }
  </style>
</head>
<body>
<a href="standings.html" target="_blank">Таблица результатов</a></br>
<a href="last.htm">Список посылок</a></br>
<a href="lastB.htm">Список посылок параллели B</a></br>
<a href="lastC.htm">Список посылок параллели C</a></br>
<a href="lastD.htm">Список посылок параллели D</a></br>
<table border=1>
%s
</table>

</body>
</html>
"""

timeNow = datetime.datetime(123, 1, 1)
timeNow = timeNow.fromtimestamp(time.time())
#timeNow += datetime.timedelta(0, 3600) * 2


def colorByStatus(status):
    d = {0:"00DD00", 1:"4169E1", 2:"FF8243", 3:"1F75FE", 4:"735184", 5:"E83042", 9:"AAAAAA", 10:"000000", 12:"9370D8", 13:"FC89AC", 14:"1FCECB", 15:"1F75FE", 16:"FFFF00", 17:"7F4134", 22:"991199"}
    if status in d:
        return d[status]
    return "FFFFFF"

def colorByParal(par):
    if par == 'A':
        return "FF4500"
    elif par == 'B':
        return "8CDD73"
    elif par == 'C':
        return "8DF2EE"
    return "FC89AC"

verdicts = {0:"OK", 2:"RT", 3:"TL", 4:"PE", 5:"WA", 6: "FAIL", 12:"ML", 13:"SE", 15:"WTL", 18:"SK", 9:"IG", 1: "CE", 7: "PT", 8: "AC", 10: "DQ", 11: "PD", 14: "SV", 16: "PR", 17: "RJ", 22: "KEK"}
table = ''

table += '<tr><td>{}</td></tr>\n'.format(timeNow.strftime('%d %h %H:%M'))
tables = [table for i in range(len(par))]
#for login, username, contest_id, prob_id, status, run_id in data:

submits = pickle.load(open(submits_path, 'rb'))[:800]

user_by_uid = dict()
for parallel in info:
    for user in info[parallel]["Users"]:
        user_by_uid[user["uid"]] = user

for c_id, p_id, run_id, uid, stat, time in submits:
    row = '<tr>{}</tr>'
    # login, username, c_id, p_id, stat, run_id, time=[i for i in r]
    if uid in user_by_uid:
        user = user_by_uid[uid]
        login = user['login']
        username = user['name']
    else:
        login = str(uid)
        username = str(uid)
    if c_id not in full_links.keys():
        continue
    links = full_links[c_id]

    c_name = names[c_id]
    c_data = full_data[c_id]
    #c_data = [(int(i[0]), i[1], i[2]) for i.split('#') in c_fulldata[1:]]
    #print(c_data)
    c_data.sort()
    #print(c_data)
    #time += datetime.timedelta(0, 3600)
    row = row.format('<td nowrap align="center">'+time.strftime('%d %h %H:%M')+'</td>{}')
    for i in [login, username]:
        row = row.format('<td>'+i+'</td>{}')
    row = row.format('<td width=250 bgcolor='+colorByParal(full_pars[c_id])+'>'+str(c_id)+': '+c_name+'</td>{}')
    row = row.format('<td width=250>'+string.ascii_uppercase[p_id - 1]+': '+c_data[p_id - 1][2].format('', '')+'</td>{}')
    if stat not in verdicts:
        verdicts[stat] = 'ERROR'
    wrong_test = ''
    if stat in [2, 3, 4, 5]:
        filePath = lastruns_path+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.wa'
        if os.path.isfile(filePath):
            wrong_test = open(filePath).readline()
    row = row.format('<td align="center" bgcolor='+colorByStatus(stat)+'>'+verdicts[stat]+wrong_test+'</td>{}')
    row = row.format('<td nowrap><a href="'+stat_link[c_id]+'#ch'+links[p_id - 1]+'" target="_blank">Statement</a></br>{}')
    row = row.format('<td nowrap><a href="lastruns/'+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.code" target="_blank">Code</a></td>{}')
    row = row.format('<td nowrap><a href="lastruns/'+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.rp" target="_blank">Report</a></td>{}')
    row = row.format('<td nowrap><a href="lastruns/'+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.rpt" target="_blank">Full report</a></td>{}')
    row = row.format('<td><a href="/new-master?contest_id='+str(c_id)+'&locale_id=0&role=6" target="_blank">Администратор</a></td>{}')
    row = row.format('<td nowrap target="_blank">' + str(run_id) + ' ' + str(stat) + '</td>{}')
    row = row.format('')
    #tables[ord(c_name[0]) - ord('A')] += row + '\n'
    #print(c_name, c_fulldata[0])
    if full_pars[c_id] in par:
        tables[par.index(full_pars[c_id])] += row + '\n'
    else:
        pass
    table += row + '\n'

templates = [template for i in range(len(par))]
template = template % (table)
s = []
for i in range(len(par)):
    templates[i] = templates[i].replace('Последние посылки', 'Последние посылки ' + par[i])
    templates[i] = templates[i] % (tables[i])
    open(html_directory + 'last' + par[i] + '.htm', 'w').write(templates[i])
#print(template)
open(html_directory + 'last.htm', 'w').write(template)

