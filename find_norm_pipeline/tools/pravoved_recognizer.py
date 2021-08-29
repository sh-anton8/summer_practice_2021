import re
import sys
import os
import tools.codexes_process_tools as coll
import json


class Request:
    def __init__(self, theme, question, answer):
        self.theme = theme
        self.question = question
        self.answer = answer
        self.norm = []
        self.codex = []

    def __str__(self):
        return 'question:{}\n\nanswer:{}\n\ncodex: {}\nnorm: {}\n-------------\n'\
            .format(self.question, self.answer, self.codex, self.norm)

    def create_dict(self):
        request_dict = {'theme': self.theme, 'question': self.question, 'answer': self.answer, 'codex': self.codex,
                        'norm': self.norm}
        return request_dict

    @staticmethod
    def load(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)


class Separator:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def editor(self):                   #деление текста на запросы
        file = open(self.path_to_file, 'r', encoding='utf-8')
        file = file.read().lower()
        file = file.replace('\xa0', "")
        a = re.split('\n(?!\t)', file)
        return a

    def sep_by_requests(self):    #деление запросов на тема-вопрос-ответ
        ed = self.editor()      #возвращает массив классов Request
        ans = []
        for k in ed:
            x1 = k.find('\t')
            x2 = k.find('\t\t', x1)
            x3 = k.find('\t\t\t', x2)
            if x3 == -1:
                s = Request(k[:x1], k[x1 + 1: x2], k[x2 + 2:])
                ans.append(s)
        return ans

    def list_of_codexes(self):  #возвращает распространненые аббревиатуры кодексов
        codex_names = ['УИК ', 'КАС', 'СК ', 'ЖК ', 'АПК ', 'УПК ', 'ГПК ', 'ук ', 'НК ', 'ТК ', 'ГК ', 'КоАП ', 'зк '
                       , 'бк']
        for i in range(len(codex_names)):
            codex_names[i] = codex_names[i].lower()
        return codex_names

    def fill_requests(self):   #заполняет класс Request найденной нормой и названием кодекса
        codexes_requests = []
        codexes = self.list_of_codexes()
        requests = self.sep_by_requests()
        reg_for_artcicle = ['стать[\w\.]*? [\d\.]*', 'ст\.\s?[\d\.]*']
        reg_for_codex = '\w*? кодекс'
        for r in requests:
            for art in reg_for_artcicle:
                article = re.findall(art, r.answer)
                if article:
                    r.norm.extend(article)
            cod = re.findall(reg_for_codex, r.answer)
            if cod:
                for c in cod:
                    if c.find('настоящ') == -1:
                        r.codex.append(c)
            for a in codexes:
                abbr = re.findall(a + 'рф', r.answer)
                if abbr != []:
                    r.codex.extend(abbr)
            if len(r.codex) == len(r.norm) == 1:
                codexes_requests.append(r)
        return codexes_requests


def dict_codexes_creator():
    codexes = dict()
    codexes[('нк', 'налогов')] = [1, 2]
    codexes[('гк', 'граждан')] = [3, 4, 5, 6]
    codexes[('тк', 'трудов')] = [7]
    codexes[('коап', 'администрат')] = [8]
    codexes[('земел', 'зк')] = [9]
    codexes[('жилищ', 'жк')] = [12]
    codexes[('апк', 'арбитраж')] = [14]
    codexes[('уголов', 'ук')] = [16]
    codexes[('семейн', 'ск')] = [17]
    codexes[('процессуальн', 'упк')] = [20]
    codexes[('водн', 'вк')] = [23]
    codexes[('лесн', 'лк')] = [26]
    poss_codexes = ['тк', 'кввт', 'воздушн', 'взк', 'нк', 'налог', 'гк', 'граждан',
                    'коап', 'администрат', 'земел', 'зк', 'тк', 'трудов', 'жилищ', 'жк',
                    'бюджет', 'бк', 'процессульальн', 'упк', 'уголовн', 'ук', 'лесн', 'лк',
                    'семейн', 'ск', 'водн', 'вк', 'гпк', 'ктм', 'уик', 'апк', 'арбитраж']
    return codexes, poss_codexes


def norms_codexes_to_normal(codex_directory, save_to_json=False):
    s = Separator(os.path.join("./data", "pravoved_articles.txt"))
    codexes_requests = s.fill_requests()
    codexes_out = []
    codexes, poss_codexes = dict_codexes_creator()
    names = list(codexes.keys())
    for cr in codexes_requests:
        finded = 0
        if re.search('\d', cr.norm[0]) is None:
            continue
        for n in names:
            if type(n) is tuple:
                if str(cr.codex[0]).find(n[0]) != -1 or str(cr.codex[0]).find(n[1]) != -1:
                    finded = 1
            else:
                if str(cr.codex[0]).find(n) != -1:
                    finded = 1
            if finded == 1:
                cr.codex = codexes[n]
                codexes_out.append(cr)
                break

    for co in codexes_out:
        co_norm1 = re.search('\d+[\.\d]*', co.norm[0])[0]
        if co_norm1.endswith('.'):
            co_norm1 = co_norm1[:-1]
        co.norm = co_norm1

    set_numbers = set()
    for files in os.listdir(codex_directory):
        file_path = os.path.join(codex_directory, files)
        a, b = coll.iter_pravoved(file_path)
        set_numbers.update(list(a.keys()))

    for co in codexes_out:
        for cod in co.codex:
            if (str(cod), co.norm) in set_numbers:
                co.codex = str(cod)
        if isinstance(co.codex, list):
            del co

    if save_to_json:
        json_codexes = []
        for co in codexes_out:
            json_codexes.append(co.create_dict())
        with open(os.path.join("./data", 'pravoved_one_answer.json'), 'w', encoding='utf-8') as f:
            json.dump(json_codexes, f, indent=2, ensure_ascii=False)
    print(len(codexes_out))

    return codexes_out


norms_codexes_to_normal(os.path.join("./data", "codexes"), save_to_json=True)