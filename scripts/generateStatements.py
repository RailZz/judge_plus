from config import *
import pickle
import json
from collections import defaultdict
import string
import os




def make_cell(text, link=None, colspan=1, color=None, title=None, cls="none", width=None, super_title=None):
    args = []
    args.append('class="{}"'.format(cls))
    if colspan > 1:
        args.append("colspan=" + str(colspan))
    if color is not None:
        args.append('bgcolor="{}"'.format(color))
    # if title is not None:
    #     args.append('title="{}"'.format(title))
    if width is not None:
        args.append('nowrap width="{}"'.format(width))
    if link is not None:
        cell = '<a target="_blank" href="{}">{}<a>'.format(link, text)
    else:
        # cell = '<b>' + text + '</b>'
        cell = text
    super_title = title
    if super_title is not None:
        tooltip = '<span class="tooltip">{}<span class="tooltiptext">{}</span></span>'.format(cell, super_title)
        s = '<td ' + ' '.join(args) + ' align="center">' + tooltip + '</td>'
        return s
    s = '<td ' + ' '.join(args) + ' align="center">' + cell + '</td>'
    return s

# def colorByStatus(statuses):
#     if status == 0:
#         return "00FF00"
#     elif status in [2, 3, 4, 5]:
#         return "FF0000"
#     elif status == 16:
#         return "FFFF00"
#     else:
#         return "0000FF"
verdicts = {0:"OK", 2:"RT", 3:"TL", 4:"PE", 5:"WA", 6: "FAIL", 12:"ML", 13:"SE", 15:"WTL", 18:"SK", 9:"IG", 1: "CE", 7: "PT", 8: "AC", 10: "DQ", 11: "PD", 14: "SV", 16: "PR", 17: "RJ", 22: 'KEK', 96: "JUDGE"}

def get_cell_by(sbm, title, userDict):
    if len(sbm) == 0:
        return make_cell("-", title=title)
    srt = sorted([[sbm[i][1], sbm[i][0]] for i in sbm])
    statuses = [v for t, v in srt]

    # title += '\n' + '\n'.join([str(sbm[i][1]) + ' ' + verdicts[sbm[i][0]] for i in sbm])
    # print(srt)
    title += '\n<br>\n' + '\n<br>\n'.join([str(t) + ' ' + verdicts[v] for t, v in srt]) # + '\n'.join([str(i) + 'kek' for i in range(100)])
    cls = "None"
    isOK = False
    if 0 in statuses:
        isOK = True
        cls = "ac"
    elif 16 in statuses:
        isOK = True
        cls = "pending"
    elif 17 in statuses:
        cls = "rj"
    else:
        cls = "wa"
    text = ''
    if isOK:
        text = '+'
    else:
        text = '-'
    # amount = len(statuses) - statuses.count(0) - statuses.count(16) - statuses.count(1) - statuses.count(17)
    amount = sum([statuses.count(i) for i in [2, 3, 4, 5, 12, 13, 15, 7, 23]])
    if amount > 0:
        text += str(amount)
    if userDict is not None:
        if 0 in statuses:
            userDict['sum'] += 1
            userDict['penalty'] += amount
    return make_cell(text, cls=cls, title=title)

def generate_table(parallel, info, data):
    """
            parallel link         #     day1  #     day2      # ... 
         Name     # sum # penalty # A # B # C # A # B # C # D # ...
    Kek Lavr      # 100 # 100000  # + #   # -1# ...
    """
    rows = []
    # generate top
    days = []
    days.append(make_cell("Параллель " + parallel, "index{}.htm".format(parallel), colspan=3))
    for contest in info[parallel]["Contests"]:
        days.append(make_cell(contest["ContestName"], 
                    "/new-client?contest_id=" + str(contest["EjudgeID"]), 
                    colspan=len(contest["Problems"])))

    rows.append(''.join(days))
    
    second_row = []
    second_row.append(make_cell("Имя (логин)", width=210))
    second_row.append(make_cell("Сумма", width = 30))
    second_row.append(make_cell("Штраф", width = 30))
    for contest in info[parallel]["Contests"]:
        for problem in contest["Problems"]:
            letter = problem["Letter"] if "Letter" in problem else string.ascii_uppercase[problem["EjudgeID"] - 1]
            second_row.append(make_cell(letter, link=contest["StatementLink"] + "#ch" + str(problem["InformaticsID"]), title=problem["Name"], width=19))

    rows.append(''.join(second_row))

    score_rows = []
    for user in info[parallel]["Users"]:
        row = []
        name = ''
        if 'name' in user:
            if 'group' in user:
                name = user['name'] + ' [{}]'.format(user['group']) 
            else:
                name = user['name']    
        elif 'login' in user:
            name = user['login']
        else:
            name = user['uid']
        row.append(make_cell(name, title=str(user)))
        row.append(make_cell('0'))
        row.append(make_cell('0'))
        userDict = {"sum": 0, "penalty": 0}
        for contest in info[parallel]["Contests"]:
            for problem in contest["Problems"]:
                user_submits = data[parallel][user["uid"]][contest["EjudgeID"]][problem["EjudgeID"]]
                title = name + ' - ' + problem['Name']
                row.append(get_cell_by(user_submits, title, userDict))
        row[1] = make_cell(str(userDict["sum"]))
        row[2] = make_cell(str(userDict["penalty"]))
        score_rows.append([-userDict["sum"], userDict["penalty"], ''.join(row)])
        # rows.append(''.join(row))
    score_rows.sort()
    rows += [i[2] for i in score_rows]
    # print(*score_rows, sep = '\n')
    # print('\n\n\n')
    # print(len(rows))
    table = '<table class="results" cellpadding="0" cellspacing="0">' +  '\n'.join(['<tr>' + i + '</tr>' for i in rows]) + '</table>'
    return table

def wrap_table(table):
    #white-space:nowrap; in table.results td    
    pageTemplate = """
    <html>
    <head>
    <style>
    table.results{
    border-left:1px solid black;
    border-top:1px solid black;
    background:white;
    margin-top:10px;
    }
    table.results td{
    border-right:1px solid black;
    border-bottom:1px solid black;
    padding-left:3px;
    padding-right:3px;
    padding-top:2px;
    padding-bottom:2px;
    }
    td.contest, td.problem{
    text-align:center;
    }
    td.ac, td.wa, td.none, td.pending, td.rj {
    text-align:center;
    }
    td.ac{
    background:#aaffbb;
    }
    td.wa{
    background:#ffaaaa;
    }
    td.rj{
    background:#aaaaff;
    }
    td.dq{
    background:#000000;
    }
    td.last{
    background:#aaffbb;
    text-align:center;
    border-right:1px solid red;
    border-bottom:1px solid red;
    border-left:1px solid red;
    border-top:1px solid red;
    padding-left:3px;
    padding-right:3px;
    padding-top:2px;
    padding-bottom:2px;
    }
    td.ac2 {
    background: #44ff44;
    font-weight: bold;
    font-family: "Courier New";
    
    }
    td.solved, td.penalty, td.weight, td.styleErrs{
    text-align:right;
    }
    td.ac:after{
        content: attr(data-title);
        display: none;position: absolute;
        bottom: 130%;
        left: 0px;
        background-color: #fff;
        color: #3aaeda;
        padding: 5px;
        text-align: center;
        -moz-box-shadow: 0 1px 1px rgba(0,0,0,.16);
        -webkit-box-shadow: 0 1px 1px rgba(0,0,0,.16);
        box-shadow: 0 1px 1px rgba(0,0,0,.16);font-size: 12px;
    }
    td.ac:hover:after{ 
        display: block;
    }
    table.results td.name{
    padding-right:10px;
    }
    td.weight{
    font-weight: bold;
    }
    td.probstat{
    text-align:right;
    }
    td.pending{
    background:#ffff77;
    }
    .tooltip {
    position: relative;
    display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #FC89AC;
        color: #000;
        text-align: left;
        padding: 5px 5px;
        position: absolute;
        z-index: 1;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
    }

    </style>
        <title>Таблица результатов</title>
    </head>
    <body>



    """
        
    page = pageTemplate + table + """
    </body>
    </html> """    
    return page


def generateStatements():


    info = json.load(open(info_path))
    submits = pickle.load(open(submits_path, 'rb'))

    data = dict()
    #["A"][uid][contestID][probID] [runID] = [data]
    def get_super_default_dict():
        return defaultdict(get_super_default_dict)

    data = defaultdict(get_super_default_dict)
    user_by_uid = dict()

    for parallel in info:
        for user in info[parallel]["Users"]:
            user_by_uid[user["uid"]] = user
            user_by_uid[user["uid"]]["parallel"] = parallel


    for contestID, problemID, runID, uid, result, t in submits:
        if uid in user_by_uid:
            data[user_by_uid[uid]["parallel"]][uid][contestID][problemID][runID] = [result, t]
    tables = [generate_table(parallel, info, data) for parallel in sorted(info.keys())]

    # for parallel in sorted(info.keys()):
    #     tables += '\n\n' + generate_table(parallel, info, data)
    page = wrap_table('\n\n'.join(tables))

    open(os.path.join(html_directory, 'standings.html'), 'w').write(page)

    for index, parallel in enumerate(sorted(info.keys())):
        open(os.path.join(html_directory, 'standings{}.html'.format(parallel)), 'w').write(wrap_table(tables[index]))





if __name__ == "__main__":
    generateStatements()
