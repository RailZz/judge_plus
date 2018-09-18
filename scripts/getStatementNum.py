#!/usr/bin/python3
import sys

if len(sys.argv) < 3:
    print("Not enough args")
    exit(0)

filename = sys.argv[1]
contest_num = sys.argv[2]
statement = open(filename).read()
task_num = [sys.argv[1]]
pos = 0
while True:
    pos = statement.find('#ch', pos)
    if pos == -1:
        break
    fin_pos = pos + 3
    while statement[fin_pos].isdigit():
        fin_pos += 1
    task_num.append(statement[pos + 3:fin_pos])
    pos = fin_pos
open('/home/judges/nums/' + str(contest_num), "w").write('#'.join([i for i in task_num]))
