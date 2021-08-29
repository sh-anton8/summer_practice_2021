import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download("stopwords")
english_stopwords = set(stopwords.words('english'))
russian_stopwords = set(stopwords.words("russian"))

# english tokenizer
lemmatizer = WordNetLemmatizer()
def lemma_tokenizer(text):
    sents = sent_tokenize(text)
    ans = []
    for sent in sents:
        clean_sent = sent.lower().translate(str.maketrans('', '', string.punctuation))
        toks = word_tokenize(clean_sent)
        for tok in toks:
            if tok not in english_stopwords:
                ans.append(lemmatizer.lemmatize(tok))
    return ans

# russian tokenizer
stemmer = SnowballStemmer("russian") 
def stem_tokenizer(text):
    sents = sent_tokenize(text)
    ans = []
    for sent in sents:
        clean_sent = sent.lower().translate(str.maketrans('', '', string.punctuation))
        toks = word_tokenize(clean_sent)
        for tok in toks:
            if tok not in russian_stopwords:
                ans.append(stemmer.stem(tok))
    return ans