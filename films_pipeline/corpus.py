from nltk.tokenize import sent_tokenize, word_tokenize
from utils.tokenizers import lemma_tokenizer

class PlotCorpus:
    def __init__(self, plots, tokenizer=lemma_tokenizer):
        self.plots = plots
        self.tokenizer = tokenizer
        
    def iterate(self, return_plot_id=False):
        for plot_id, plot in enumerate(self.plots):
            sents = sent_tokenize(plot)
            for sent in sents:
                toks = self.tokenizer(sent)
                ret_val = (plot_id, toks) if return_plot_id else toks
                yield ret_val
                
    def __iter__(self):
        for el in self.iterate(return_plot_id=False):
            yield el