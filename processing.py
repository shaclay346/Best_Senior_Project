# processing.py
# Performs all the preproccessing required on plaintext for use with the SVM

from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords, wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
import openpyxl as pyxl
import numpy as np
import math, os, re, pdb

ROOT = os.path.dirname(os.path.abspath(__file__))

def process(sentence):
	'''Processes the string 'sentence' in such a way that it can be used with the SVM'''

	# Invalid sentence type
	if not isinstance(sentence, str):
		raise Exception("Processing Error: Invalid type: must be str")
		return # unnecessary return but maintains my sanity


	# Convert to Lowercase
	sentence = sentence.lower()

	# Replace Nonletter Characters with Spaces
	sentence = re.sub('[^a-z]', " ", sentence)

	# Tokenize Sentence
	sentence = [word for word in sentence if word != ' ' and len(word) > 1]

	# Remove Stop Words
	stop_words = set(stopwords.words("english"))
	sentence = [word for word in sentence if word not in stop_words]

	# Lemmatize
	sentence = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in sentence]

	# Calculate TF-IDF Score
	tfidf_vectorizer = TfidfVectorizer(lowercase=False)

	sentence = tfidf_vectorizer.fit_transform(" ".join(sentence))
	sentence = np.asarray(sentence.todense())

	return np.array(sentence)		


def preprocess():
	'''Performs all the preprocessing necessary to train the SVM (we don't want to train it every time we run the VA)'''
	# Load Data from intents.xlsx
	wb = pyxl.load_workbook('intents.xlsx')
	sheet = wb.active

	labels = []
	data = []
	
	# Iterate Col by Col
	for col in sheet.iter_cols(min_row=1, max_col=sheet.max_column, max_row=sheet.max_row, values_only=True):
		labels.append(col[0])
		data.append([a for a in col[1:] if a])


def get_wordnet_pos(word):
	'''Maps the given word to its (simplified) part of speech for use in lemmatization'''
	tag = pos_tag([word])[0][1][0].upper()

	tag_dict = {"J": wordnet.ADJ,
				"N": wordnet.NOUN,
				"V": wordnet.VERB,
				"R": wordnet.ADV}

	return tag_dict.get(tag, wordnet.NOUN) # return simplified POS (defaults to NOUN)


def to_sentence(arr):
	'''Converts numpy array into a string'''
	for i in range(arr.size):
		arr[i] = ' '.join(str(word) for word in arr[i])


def view_intents():
	'''Quality of Life Function that returns intents.xmls as a dictionary'''
	# Load Data from intents.xlsx
	wb = pyxl.load_workbook('intents.xlsx')
	sheet = wb.active

	info = {}
	
	# Iterate Col by Col
	for col in sheet.iter_cols(min_row=1, max_col=sheet.max_column, max_row=sheet.max_row, values_only=True):
		info.update({col[0]:[a for a in col[1:] if a]})

	return info


def train_svm(data, labels):
	'''Trains the SVM with the given dataset and labels.'''
	
	pass




def main():
	pdb.set_trace()
	preprocess()



if __name__ == '__main__':
	main()











