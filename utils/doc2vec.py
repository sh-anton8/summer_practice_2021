import collections
import numpy as np

class Doc2Vec:
    def __init__(self, w2v_model, tfidf_model=None, tokenizer=None):
        self.w2v = w2v_model.wv
        self.tfidf = tfidf_model
        self.use_weights = False
        if self.tfidf is not None:
            self.use_weights = True
        self.tokenizer = tokenizer
        
    def get_sentence_vector(self, sent, is_sent_tokenized=False):
        sentence = sent
        if not is_sent_tokenized:
            sentence = self.tokenizer(sent)
            
        vector = np.zeros(len(self.w2v[list(self.w2v.vocab)[0]]))
        cnt = collections.Counter(sentence)
        for token, token_cnt in cnt.items():
            if token not in self.w2v.vocab:
                continue
            if self.use_weights:
                if token not in self.tfidf.id2word.token2id:
                    continue
                vector += self.w2v[token] * self.tfidf.idfs[self.tfidf.id2word.token2id[token]] * self.tfidf.wlocal(token_cnt)
            else:
                vector += (1.0 / len(cnt)) * self.w2v[token]
        
        return vector
