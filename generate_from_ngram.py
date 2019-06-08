#!/usr/bin/env python3
'''
William Bowers
generate_from_ngram.py
takes in a language model (output from build_ngram_model.py) and generates uni/bi/trigram sentences
3/25/2019
'''
import sys, random, time


input_file = sys.argv[1]
output_file = sys.argv[2]

#open file, split on new line, lowercase, start of sentence tags, end of sentence tags, split on each word
with open(input_file,'r') as text_file:
	lines = text_file.read().split('\n')
	

#establishing boundaries within the text using index of identifying line in the dickens_model.txt file
unigram_start = lines.index('\\1-grams:') #index at 5
bigram_start = lines.index('\\2-grams:') #index at 43,885
trigram_start = lines.index('\\3-grams:') #index at 613,523
end = lines.index('\\end\\') #index at 2,217,785


#UNIGRAMS
'''
Process:
- start with <s>
- generate random float to use as a target number
- iterate through the list of n-grams, adding probabilites together until the random target number is met.
- add that word to sentence until </s> is generated
- make sure it starts on the start tag <s>
- another start tag <s> cannot exist until there is an end tag </s>
'''
#generating unigram based on random float
def generate_unigram(random):
	probability_sum = 0.0
	for line in lines[unigram_start + 1:bigram_start - 1]:
		words = line.split(' ')
		probability_sum += float(words[1])
		unigram = words[3]
		if probability_sum >= random:
			return unigram
	return None #if all unigrams have been iterated over and the random condition isnt satisfied

#stringing together unigrams to make a sentence
def unigram_sentence():
	beg_sentence = '<s> '
	sentence = beg_sentence + ''
	current_word = ''
	while current_word != '</s>':
		current_word = generate_unigram(random.random())
		if current_word != '<s>':
			sentence += current_word + ' '
	return sentence


#BIGRAMS
'''
Process:
- start with <s>
- generate random float to use as a target number
- iterate through the list of n-grams, adding probabilites of the 2nd word (given <s>) in bigram together until the random target number is met.
- when target is met, add word to sentence, then repeat with bigrams that start with that generated word
- make sure it starts on the start tag <s>
- another start tag <s> cannot exist until there is an end tag </s>
'''
#how do i make the condition read that <s> is given 

#generates the second word of bigram, given the first
def generate_bigram(random, reduced_lines):
	probability_sum = 0.0
	for line in reduced_lines:
		words = line.split(' ')
		probability_sum += float(words[1])
		if probability_sum >= random:
			return words[4]
	return None		

#generate sentence
def bigram_sentence():
	sentence = ['<s>']
	while sentence[-1] != '</s>':
		#find all bigrams with the most recent word as the first word
		reduced_lines = list(filter(lambda x: x.split(' ')[3] == sentence[-1], lines[bigram_start + 1:trigram_start - 1]))
		next_word = generate_bigram(random.random(), reduced_lines)
		if next_word != '<s>' and next_word != None:
			sentence.append(next_word)
	return sentence


#TRIGRAMS
'''
Process:
- same as bigram
- use the bigram generator to find the first word after the <s>
'''
def generate_trigram(random, reduced_lines):
	probability_sum = 0.0
	for line in reduced_lines:
		words = line.split(' ')
		probability_sum += float(words[1])
		if probability_sum >= random:
			return words[5]
	return None	

def trigram_sentence():
	sentence = ['<s>']
	#find the bigrams of the trigram
	while len(sentence) < 2:
		reduced_lines = list(filter(lambda x: x.split(' ')[3] == sentence[-1], lines[bigram_start + 1:trigram_start - 1]))
		next_word = generate_bigram(random.random(), reduced_lines)
		if next_word != '<s>' and next_word != None:
			sentence.append(next_word)
	#find the 3rd word of trigram
	while sentence[-1] != '</s>':
		#filter based of two already coexisting words in a trigram
		reduced_lines = list(filter(lambda x: x.split(' ')[3] == sentence[-2] and x.split(' ')[4] == sentence[-1], lines[trigram_start + 1:end - 1]))
		next_word = generate_trigram(random.random(), reduced_lines)
		if next_word != '<s>' and next_word != None:
			sentence.append(next_word)
	return sentence


#call functions and write outputs to file
def writer():
	with open(output_file, 'w') as output:
		begin = time.time()
		output.write('\\1 grams:' + '\n')
		for i in range(0,5):
			output.write(unigram_sentence() + '\n')
		print('Unigrams:', time.time() - begin)

		output.write('\n' + '\\2 grams:' + '\n')
		for i in range(0,5):
			output.write(' '.join(bigram_sentence()) + '\n')
		print('Bigrams:', time.time() - begin)

		output.write('\n' + '\\3 grams:' + '\n')
		for i in range(0,5):
			output.write(' '.join(trigram_sentence()) + '\n')
		print('Trigrams:', time.time() - begin)

writer()