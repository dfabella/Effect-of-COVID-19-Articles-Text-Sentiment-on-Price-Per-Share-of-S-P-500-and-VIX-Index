from nltk.tokenize import PunktSentenceTokenizer,word_tokenize,sent_tokenize
from nltk.corpus import state_union

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")
custom_sent_tokenizer = PunktSentenceTokenizer.train(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)