import sys
import os
import logging

# todo: use regular expression insted of find

class StatementsParser:
    def __init__(self, path=None, apply=True):
        self.path = path
        self.data = open(self.path, "r").read()
        self.task_nums = None
        self.name = None

        self.delete_print_decription()
        self.get_contest_info()
        self.get_contest_name()

        if apply:
            self.apply()


    # try run same as convertStatement
    def delete_print_decription(self):

        if '<div class=statements_info><table>' in self.data:
            position = self.data.index('<div class=statements_info><table>')
        elif '<div class="statements_info"><table>' in self.data:
            position = self.data.index('<div class="statements_info"><table>')
        else:
            logging.error("No statements print tabel found")
            return
        b = self.data.index('</table></div>') + len('</table></div>')
        self.data = self.data[:position] + self.data[b:]

    def get_contest_info(self, force=False):
        if self.task_nums is not None and not force:
            return self.task_nums
        self.task_nums = []
        pos = 0
        while True:
            pos = self.data.find('#ch', pos)
            if pos == -1:
                break
            fin_pos = pos + 3
            while self.data[fin_pos].isdigit():
                fin_pos += 1
            self.task_nums.append(int(self.data[pos + 3:fin_pos]))
            pos = fin_pos
        return self.task_nums

    def get_contest_name(self):
        if self.name is None:
            name_begin = self.data.find('<title>')
            name_end = self.data.find('</title>')
            if name_begin == -1 or name_end == -1:
                raise Exception("No title found")
            tmp_name = self.data[name_begin + 7:name_end]
            if len(tmp_name) >= 12 and tmp_name[:13] in ['Параллель ' + i + '. ' for i in ['A', 'B', 'C', 'D', 'A', 'В', 'С']]: #checking that contest name starts with words "Параллель "
                tmp_name = tmp_name[13:]
            self.name = tmp_name
        return self.name

    def apply(self):
        open(self.path, 'w').write(self.data)

