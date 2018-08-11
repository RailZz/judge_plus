import time

import string
import pymysql
import time
import datetime

import os
import os.path

db = pymysql.connect("localhost", "ejudge", "ejudge", "ejudge", charset="utf8")
cursor = db.cursor()

par = ['A', 'B', 'C', 'D']

cursor.execute('select logins.login, users.username, runs.contest_id, runs.prob_id, runs.status, runs.run_id, runs.create_time from logins, users, runs where logins.user_id=users.user_id and logins.user_id=runs.user_id and runs.user_id != 1 order by -runs.create_time LIMIT 400')

data = cursor.fetchall()
#print(*data, sep = '\n')


template = """
<html>
<head>
<title>Последние посылки</title>
<style type="text/css">
   BODY {
    background: white; /* Цвет фона веб-страницы */
   }
   TABLE {
    width: 300px; /* Ширина таблицы */
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
<a href="standings.htm" target="_blank">Таблица результатов</a></br>
<a href="last.htm">Список посылок</a></br>
<a href="lastA.htm">Список посылок параллели A</a></br>
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
    if status == 0:
        return "00FF00"
    elif status in [2, 3, 4, 5]:
        return "FF0000"
    else:
        return "0000FF"

def colorByParal(par):
    if par == 'A':
        return "FF4500"
    elif par == 'B':
        return "008000"
    elif par == 'C':
        return "00FFFF"
    return "FF00FF"

verdicts = {0:"OK", 2:"RT", 3:"TL", 4:"PE", 5:"WA", 6: "FAIL", 12:"ML", 13:"SE", 15:"WTL", 18:"SK", 9:"IG", 1: "CE", 7: "PT", 8: "AC", 10: "DQ", 11: "PD", 14: "SV", 16: "PR", 17: "RJ", 22: 'KEK'}
table = ''

table += '<tr><td>{}</td></tr>\n'.format(timeNow.strftime('%d %h %H:%M'))
tables = [table for i in range(len(par))]
#for login, username, contest_id, prob_id, status, run_id in data:
for r in data:
    row = '<tr>{}</tr>'
    login, username, c_id, p_id, stat, run_id, time=[i for i in r]
    links = open('/home/judges/nums/' + str(c_id)).readline().strip().split('#')

    contestInfo = open('/home/judges/info/' + str(c_id))
    c_fulldata = [i.strip() for i in contestInfo.readlines()]
    c_name = c_fulldata[0][10:]
    c_data = []
    for i in c_fulldata[1:]:
        j = i.split('#')
        c_data.append((int(j[0]), j[1], j[2]))
    #c_data = [(int(i[0]), i[1], i[2]) for i.split('#') in c_fulldata[1:]]
    #print(c_data)
    c_data.sort()
    #print(c_data)
    #time += datetime.timedelta(0, 3600)
    row = row.format('<td nowrap align="center">'+time.strftime('%d %h %H:%M')+'</td>{}')
    for i in range(2):
        row = row.format('<td>'+str(r[i])+'</td>{}')
    row = row.format('<td nowrap bgcolor='+colorByParal(c_name[0])+'>'+str(c_id)+': '+c_name+'</td>{}')
    row = row.format('<td nowrap>'+string.ascii_uppercase[p_id - 1]+': '+c_data[p_id - 1][2]+'</td>{}')
    if stat not in verdicts:
        verdicts[stat] = 'ERROR'
    wrong_test = ''
    if stat in [2, 3, 4, 5]:
        filePath = '/var/www/html/scripts/lastruns/'+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.wa'
        if os.path.isfile(filePath):
            wrong_test = open(filePath).readline()
    row = row.format('<td align="center" bgcolor='+colorByStatus(stat)+'>'+verdicts[stat]+wrong_test+'</td>{}')
    row = row.format('<td nowrap><a href="'+links[0]+'#ch'+links[p_id]+'" target="_blank">Statement</a></br>{}')
    row = row.format('<td nowrap><a href="scripts/lastruns/'+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.code" target="_blank">Code</a></td>{}')
    row = row.format('<td nowrap><a href="scripts/lastruns/'+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.rp" target="_blank">Report</a></td>{}')
    row = row.format('<td nowrap><a href="scripts/lastruns/'+str(c_id)+'/'+('0'*6+str(run_id))[-6:]+'.rpt" target="_blank">Full report</a></td>{}')
    row = row.format('<td><a href="http://192.168.10.16/new-master?contest_id='+str(c_id)+'&locale_id=0&role=6" target="_blank">Администратор</a></td>{}')
    row = row.format('<td nowrap target="_blank">' + str(run_id) + ' ' + str(stat) + '</td>{}')
    row = row.format('')
    #tables[ord(c_name[0]) - ord('A')] += row + '\n'
    #print(c_name, c_fulldata[0])
    if c_name[0] in par:
        tables[par.index(c_name[0])] += row + '\n'
    else:
        pass
    table += row + '\n'

templates = [template for i in range(len(par))]
template = template % (table)
s = []
for i in range(len(par)):
    templates[i] = templates[i].replace('Последние посылки', 'Последние посылки ' + par[i])
    templates[i] = templates[i] % (tables[i])
    open('/var/www/html/last' + par[i] + '.htm', 'w').write(templates[i])
#print(template)
open('/var/www/html/last.htm', 'w').write(template)

