import os
import re
import codecs
import sys
import nltk
import glob
from collections import defaultdict
unigram = defaultdict(int)

def load_corpus(data):
	book_filenames = sorted(glob.glob(data+"/*.txt"))
	print(book_filenames)
	corpus_raw = u""
	for book_filename in book_filenames:
	    print("Reading '{0}'...".format(book_filename))
	    with codecs.open(book_filename, "r", "utf-8") as book_file:
	        corpus_raw += book_file.read()
	    print("Corpus is now {0} characters long".format(len(corpus_raw)))
	    print()
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	raw_sentences = tokenizer.tokenize(corpus_raw)
	#sentence where each word is tokenized
	sentences = []
	for raw_sentence in raw_sentences:
	    if len(raw_sentence) > 0:
	        sentences.append(sentence_to_wordlist(raw_sentence))
	token_count = sum([len(sentence) for sentence in sentences])
	print("The book corpus contains {0:,} tokens".format(token_count))

	# print(sentences)

def sentence_to_wordlist(raw):
	clean = re.sub("[^a-zA-Z]"," ", raw)
	words = clean.split()
	for word in words:
		word = word.lower()
		if word in unigram:
			unigram[word] += 1
		else:
			unigram[word] = 1
	return words

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Insufficient arguments provided")
		print("python3 extract_domain_specific_stopwords.py data stopwords.txt")
	data = sys.argv[1]
	output = sys.argv[2]
	load_corpus(data)
	print("Total length of unigram tokens {}".format( len(unigram)))

	with open(output,'w', encoding='utf-8') as f:
		for w in sorted(unigram, key=unigram.get, reverse=True):
			f.write(w + "\t" + str(unigram[w]) + "\n")
