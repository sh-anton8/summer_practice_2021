import pickle
import os
from tqdm import tqdm
from collections import OrderedDict


class SimpleCorp:
    """
    Простейший корпус, состоящий из списка элементов вида (doc_id, doc_text).
    doc_text может быть произвольным по типу - например строка или список токенов...
    """
    def __init__(self, corpus=OrderedDict()):
        self.corpus = {doc_id: doc_text for doc_id, doc_text in corpus}

    def __len__(self):
        return len(self.corpus)

    def get_doc(self, doc_id):
        return self.corpus.get(doc_id, None)
        
    def get_doc_ids(self):
        return list(self.corpus.keys())
        
    def iterate(self):
        """
        Основной итератор корпуса
        """
        for doc_id, doc_text in self.corpus.items():
            yield doc_id, doc_text

    def __iter__(self):
        return self.iterate()

    def add_doc(self, doc_id, doc_text):
        self.corpus.setdefault(doc_id, doc_text)

    def make_from(self, source_corpus, tokenizer=None):
        """
        Создать корпус из внешнего корпуса, возможно применив токенизацию
        """
        iterator_ = source_corpus.iterate()
        for doc_id, doc_text in tqdm(iterator_, total=len(source_corpus)):
            if tokenizer:
                self.add_doc(doc_id, tokenizer(doc_text))
            else:
                self.add_doc(doc_id, doc_text)


    def save(self, fname, path):
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/{fname}", 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(fname, path):
        with open(f"{path}/{fname}", 'rb') as f:
            return pickle.load(f)