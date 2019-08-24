import numpy as np
import pickle
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.ensemble import RandomForestRegressor
import string
import os
import re
from gensim.models import Word2Vec

class SentimentPredictionModel():

	def __init__(self):
			
		self.w2v_model = Word2Vec.load('models/w2v_model2.bin')  
		
		with open("models/RF_regression_model_tfidf.bin", "rb") as input_file:
			self.rf_model_tfidf = pickle.load(input_file)	
			
		with open("models/RF_regression_model_w2v.bin", "rb") as input_file:
			self.rf_model_w2v = pickle.load(input_file)	
			
		with open("models/tf_idf_vectorizer.bin", "rb") as input_file:
			self.tfidf_vectorizer = pickle.load(input_file)	
				
	def execute(self, data):
		
		signatures1 = self.calculate_sentence_signature(data, self.w2v_model, do_preprocess=True)		
		signatures2 = self.tfidf_vectorizer.transform([" ".join(self.preprocess(data))])	

		# Set result to neutral in case all words of the sentence are unknown for w2v embedding
		if (signatures1 == []):
			prediction1 = 3
		else:
			signatures1 = np.expand_dims(signatures1, axis=0)
			prediction1 =  self.rf_model_w2v.predict(signatures1)	

		prediction2 = self.rf_model_tfidf.predict(signatures2)
		prediction = (prediction1+prediction2)/2
		
		return prediction[0]

	def replace_emoticon(self, word):
	
		#print("-->" + word)
		pos = re.findall(r'(?::\)|:-\)|=\)|:D|:d|<3|\(:|:\'\)|\^\^|;\)|\(-:)', word)
		neg = re.findall(r'(:-\(|:\(|;\(|;-\(|=\(|:/|:\\|-_-|\):|\)-:)', word)
		
		if pos:      
		  word = "good"
		elif neg:      
		  word = "bad"
		return word

	def preprocess(self, dt):

		# replace emoticons
		dt = ' '.join([self.replace_emoticon(w) for w in dt.split(' ')])		
	
	    # tokenize all sentences
		words = word_tokenize(dt.lower())   		

		# clear punctuations
		exclude = set(string.punctuation)
		dt = ''.join(ch for ch in words if ch not in exclude)     

		print(words)
		# remove stopwords
		from nltk.corpus import stopwords
		stop_words = stopwords.words('english')
		words = [word for word in words if word not in stop_words and len(word)>1]   

		return words 

	def calculate_sentence_signature(self, sentence, embedding_model, do_preprocess = False):    
		sentenceWords = word_tokenize(sentence) if (do_preprocess==False) else self.preprocess(sentence)      
		sentence_vectors = []

		for w in sentenceWords:
			try:
				sentence_vectors.append(embedding_model[w])
			except:         
				pass

		if (len(sentence_vectors)==0):
			return []

		sentence_vectors = np.array(sentence_vectors)
		signature = np.mean(sentence_vectors, axis=0)
		return signature