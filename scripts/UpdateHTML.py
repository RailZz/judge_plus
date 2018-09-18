from config import *
import json



def genLink(link, name, blank = True):
    return '<a href="' + link + ('" target="_blank"' if blank else '"') + '>' + name + '</a>'

def genNum(s, l):
    return ('0' * l + str(s))[-l:]

def genHTML():
    template = """
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>{}</title>
</head>
<body>"""
    info = json.load(open(info_path))
    for par in sorted(info.keys()):
        html = template.format("Группа " + par)
        html += '\n{}'
        html = html.format('<font size="1">' + genLink('/cgi-bin/serve-control', 'admin') + '</font>\n{}')
        html = html.format('<h1>Группа ' + par + '</h1>\n<p></p>\n{}')
        html = html.format(genLink('index.html', 'Назад', False) + '\n<p></p>\n{}')
        html = html.format('<table border="1">\n{}')
        for cont in info[par][Contests]:
            html = html.format('<tr>\n{}')
            html = html.format('<td>' + genLink("/cgi-bin/new-client?contest_id=" + genNum(cont["EjudgeID"], 6), cont["ContestName"]) + '</td>\n{}')
            html = html.format('<td>' + genLink(cont["StatementLink"], "Условия") + '</td>\n{}')
            html = html.format('</tr>\n{}')
        html = html.format('</table>\n<p></p>\n{}')
        html = html.format(genLink("standings" + par + ".html", "Таблица результатов") + '\n<p></p>{}')
        html = html.format(info[par][HTMLComment] + '{}')
        html = html.format('</body>\n</html>')
        open(html_directory + "index" + par + ".htm", "w").write(html)
    print('generated')


if __name__ == "__main__":
    genHTML()

        
