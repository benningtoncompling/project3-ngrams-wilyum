#!/usr/bin/env python3
'''
William Bowers
build_ngram_model.py
takes in an input file and outputs a file with the probabilities for each unigram, bigram, and trigram of the input text
3/25/2019
'''
import sys
import math
import time

input_file = sys.argv[1]
output_file = sys.argv[2]

#open file, split on new line, lowercase, start of sentence tags, end of sentence tags, split on each word
with open(input_file,'r') as text_file:
	lines = text_file.read().split('\n')
	lines = ['<s> ' + line.lower() + ' </s>' for line in lines]
	words = [word.split() for word in lines]


word_dict = {}
def unigrams():
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

	#sort unigrams by abc's then by value
	unigrams_sorted_abc = sorted(word_dict, key=lambda x: x)
	unigrams_sorted = sorted(unigrams_sorted_abc, key=lambda x: word_dict[x], reverse = True)

	unigrams_list = []
	for unigram in unigrams_sorted:
		unigram_count = word_dict[unigram]
		probability = unigram_count/unigram_tokens #number of unigram occurance over tokens in text
		unigram_log = math.log10(probability)
		to_append = (unigram_count, probability, unigram_log, unigram)
		unigrams_list.append(to_append)
	
	return unigrams_list, unigram_types, unigram_tokens



#Make bigrams w/o nltk
bigram_dict = {}
def bigrams():
	bigram_list = []
	flattened_bigram_list = []
	bigram_tokens = 0

	#make list of bigram lists
	for line in words:
		for word in range(len(line)-1):
			bigram_list.append([[line[word]], [line[word+1]]])
	#use that list in a dictionary 
	# but we gotta go from [['<s>'], ['i']] to ('<s>', 'i') to use tuples as dict keys
	#to do so w/o nltk:
	#FIRST: flatten the lists
	for x in bigram_list:
		for y in x:
			flattened_bigram_list.append(y)
	#SECOND:list comprehension
	y= [''.join(x) for x in flattened_bigram_list]
	#THIRD: rewriting bigram_list and grouping the flattened_bigram_list by two to create immutable tuple for bigram_dict key
	bigram_list = list(zip(*[iter(y)] * 2))
	#FOURTH: Add to Dicitonary
	for bigram in bigram_list:
		bigram_tokens += 1
		if bigram in bigram_dict:
			bigram_dict[bigram] += 1
		else:
			bigram_dict[bigram] = 1

	bigram_types = len(bigram_dict)


	#sort bigrams by abc's then by value
	bigrams_sorted_abc = sorted(bigram_dict, key=lambda x: x)
	bigrams_sorted = sorted(bigrams_sorted_abc, key=lambda x: bigram_dict[x], reverse = True)

	
	#getting onegram values to use for bigram probabailty
	onegrams_list = [word[0] for word in bigram_list] #should be equal to the original unigram_token count but isnt
	onegrams_dict = {}
	for onegram in onegrams_list:
		if onegram in onegrams_dict:
			onegrams_dict[onegram] += 1
		else:
			onegrams_dict[onegram] = 1
	

	bigrams_list = []
	for bigram in bigrams_sorted:
		bigram_count = bigram_dict[bigram]
		#print(bigram_count)
		onegram_count = onegrams_dict[bigram[0]] 
		#print(onegram_count)
		probability = bigram_count/onegram_count #count of the bigram over the count of the first word in the bigram
		bigram_log = math.log10(probability)
		to_append = (bigram_count, probability, bigram_log, bigram)
		bigrams_list.append(to_append)

	return bigrams_list, bigram_types, bigram_tokens


trigram_dict = {}
def trigrams():
	trigram_list = []
	flattened_trigram_list = []
	trigram_tokens = 0

	for line in words:
		for word in range(len(line)-2):
			trigram_list.append([[line[word]], [line[word+1]], [line[word+2]]])

	#from [['<s>'], ['i'], ['a']] to ('<s>', 'i', 'a') to use tuples as dict keys
	for x in trigram_list:
		for y in x:
			flattened_trigram_list.append(y)
	y= [''.join(x) for x in flattened_trigram_list]
	trigram_list = list(zip(*[iter(y)] * 3))
	

	for trigram in trigram_list:
		trigram_tokens += 1
		if trigram in trigram_dict:
			trigram_dict[trigram] += 1
		else:
			trigram_dict[trigram] = 1
	trigram_types = len(trigram_dict)


	#sort bigrams by abc's then by value
	trigrams_sorted_abc = sorted(trigram_dict, key=lambda x: x)
	trigrams_sorted = sorted(trigrams_sorted_abc, key=lambda x: trigram_dict[x], reverse = True)
	
	#getting twograms to use for the trigram probability
	twograms_list = [(word[0], word[1]) for word in trigram_list] #should be equal to the original unigram_token count but isnt
	twograms_dict = {}
	for twogram in twograms_list:
		if twogram in twograms_dict:
			twograms_dict[twogram] += 1
		else:
			twograms_dict[twogram] = 1

	trigrams_list = []
	for trigram in trigrams_sorted:
		trigram_count = trigram_dict[trigram]
		twogram_count = twograms_dict[trigram[0], trigram[1]] #need to get first 2 values of tuple
		probability = trigram_count/twogram_count
		trigram_log = math.log10(probability)
		to_append = (trigram_count, probability, trigram_log, trigram)
		trigrams_list.append(to_append)

	return trigrams_list, trigram_types, trigram_tokens

#WRITE OUTPUTS TO FILE
def writer(unigrams_list, unigram_types, unigram_tokens, bigrams_list, bigram_types, bigram_tokens, trigrams_list, trigram_types, trigram_tokens):
	
	with open(output_file, 'w') as output:
		#data
		output.write('\\data\\\n')
		output.write('ngram 1: type=' + str(unigram_types) + ' token=' + str(unigram_tokens) + '\n')
		output.write('ngram 2: type=' + str(bigram_types) + ' token=' + str(bigram_tokens) + '\n')
		output.write('ngram 3: type=' + str(trigram_types) + ' token=' + str(trigram_tokens) + '\n' + '\n')

		#unigrams
		output.write('\\1-grams:' + '\n')
		for line in unigrams_list:
			line = ' '.join(map(str, line))
			output.write(str(line) + '\n')

		#bigrams
		output.write('\n' + '\\2-grams:' + '\n')
		for line in bigrams_list:
			line = ' '.join(map(str, line))
			output.write(str(line) + '\n')

		#trigrams
		output.write('\n' + '\\3-grams:' + '\n')
		for line in trigrams_list:
			line = ' '.join(map(str, line))
			output.write(str(line) + '\n')
		output.close()


total_start = time.time()

unigrams_start = time.time()
unigrams_list, unigram_types, unigram_tokens = unigrams()
print("Unigrams:" , time.time() - unigrams_start, "seconds")

bigrams_start = time.time()
bigrams_list, bigram_types, bigram_tokens = bigrams()
print("Bigrams:" , time.time() - bigrams_start, "seconds")

trigrams_start = time.time()
trigrams_list, trigram_types, trigram_tokens = trigrams()
trigrams()
print("Trigrams:" , time.time() - trigrams_start, "seconds")

writer_start = time.time()
writer(unigrams_list, unigram_types, unigram_tokens, bigrams_list, bigram_types, bigram_tokens, trigrams_list, trigram_types, trigram_tokens)
print("Write:" , time.time() - writer_start, "seconds")

print("TOTAL TIME:" , time.time() - total_start, "seconds")