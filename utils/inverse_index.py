import os
import pickle
from tqdm import tqdm
import pandas as pd
from collections import Counter
from tqdm import tqdm


class InverseIndex:
    def __init__(self, tokenizer):
        self.inv_ind = {}
        self.doc_ids = []
        self.doc_lens = {}
        self.tokenizer = tokenizer

    def build_on(self, corpus, tokenized=True):
        """
        Построить обратный индекс по корпусу.
        tokenized: если True, то считаем что подается уже токенизированный
        корпус (тем же токенайзером что задан в init)
        """
        for doc_id, doc_text in tqdm(corpus):
            doc_num = len(self.doc_ids)
            self.doc_ids.append(doc_id)

            tokens = doc_text if tokenized else self.tokenizer(doc_text)
            tokens = set(tokens)  # важно - не учитываем повторы токенов

            self.doc_lens[doc_id] = len(tokens)

            for token in tokens:
                if token not in self.inv_ind:
                    self.inv_ind[token] = []
                # в обратный индекс записываем не сам doc_id, а его номер,
                # это делается для оптимизации памяти и скорости
                self.inv_ind[token].append(doc_num)

    def search(self, query, topN=10, threshold=0.5, metric='recall'):
        """
        Поиск по запросу.
        topN - сколько документов оставить после ранжирования по релевантности
        threshold - порог отсечения по релевантности
        metric - тип релевантности: точность, полнота или F1
        """
        assert metric in ['precision', 'recall', 'f_measure']

        tokens = set(self.tokenizer(query))
        qlen = len(tokens)

        # заполняем счетчик количества токенов запроса в данном "документе" корпуса
        query_tokens_counter = Counter()
        for token in tokens:
            doc_num_list = self.inv_ind.get(token, [])
            query_tokens_counter.update(doc_num_list)

        result = []
        for doc_num in query_tokens_counter:
            found = query_tokens_counter[doc_num]

            recall = found / qlen
            precision = found / self.doc_lens[self.doc_ids[doc_num]]

            if precision + recall != 0.0:
                f_measure = 2 * precision * recall / (precision + recall)
            else:
                f_measure = 0.0

            if metric == 'recall':
                rel = recall
            elif metric == 'precision':
                rel = precision
            elif metric == 'f_measure':
                rel = f_measure

            if rel < threshold:
                continue

            result.append([self.doc_ids[doc_num], rel])

        if result:
            df_res = pd.DataFrame(result, columns=['doc_id', 'rel'])
            df_res = df_res.sort_values('rel', ascending=False)

            # в результатах поиска может быть много документов  с минимальной
            # релевантностью, но надо их не потерять и взять все, а не только topN
            min_rel_topN = df_res['rel'][:topN].min()
            df_res = df_res[df_res['rel'] >= min_rel_topN]
            result = df_res.values.tolist()

        return result

    def save(self, file):
        print('Saving index to: {}'.format(file))
        with open(file, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(file):
        print('Loading index from: {}'.format(file))
        with open(file, 'rb') as f:
            return pickle.load(f)