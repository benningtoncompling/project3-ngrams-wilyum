#!/usr/bin/env python3
'''
William Bowers
build_ngram_model.py
takes in an input file and outputs a file with the probabilities for each unigram, bigram, and trigram of the input text
3/25/2019
'''
import sys
import nltk
import math

input_file = sys.argv[1]
output_file = sys.argv[2]

#open file, split on new line, lowercase, start of sentence tags, end of sentence tags, split on each word
with open(input_file,'r') as text_file:
	lines = text_file.read().split('\n')
	lines = ['<s> ' + line.lower() + ' </s>' for line in lines]
	words = [word.split() for word in lines]

#dictionary of word count in text
word_dict = {}
#count of tokens in text
unigram_tokens = 0
#nested loop since words is a list of lists
for line in words:
	for word in line:
		unigram_tokens += 1
		if word in word_dict:
			word_dict[word] += 1
		else:
			word_dict[word] = 1

unigram_types = len(word_dict)


def unigram_probability():
	unigram_count = unigram
	probability = word_dict/unigram_tokens
	unigram_log = math.log10(probability)
	unigram = unigram
	unigrams = [unigram_count, probability, unigram_log, ]






unigram_list = []
bigram_list = []
trigram_list = []
