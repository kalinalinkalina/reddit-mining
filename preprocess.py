import os
import re
import string
from nltk.corpus import stopwords
import json
import enchant
import nltk

# Specify which fields to delete
rsFieldsToDelete = ['author_flair_css_class', 'author_flair_text', 'author_h', 'brand_safe', 'can_guild', 'created_date', 'created_utc', 'distinguished', 'domain', 'edited', 'hide_score', 'id_h', 'is_video', 'link_flair_css_class', 'media_embed', 'media', 'name_h', 'num_comments', 'over_18', 'url_h' 'post_hint', 'preview', 'quarantine', 'retrieved_on_date', 'retrieved_on', 'saved', 'secure_media_embed', 'secure_media', 'spoiler', 'subreddit_id', 'thumbnail' ]
rsExtensionFieldsToDelete = ['socialsim_search_source', 'created_dow', 'created_hod', 'permalink_h']
# Fields not deleted: extension.sentiment_polarity, extension.sentiment_subjectivity, extension.socialsim_keywords, extension.socialsim_domain, gilded, is_self, locked, num_comments, score, selftext_m, stickied, subreddit, title_m

# Data paths and names and stuff
topics = ['Crypto', 'CVE', 'Cyber']
inPath  = '/home/kalina/Desktop/CS412/raw/' + topics[2] + '/'
outPath = '/home/kalina/Desktop/CS412/clean/' + topics[2] + '/'

# This needs to be run on all data files. Here is one.
fileName = 'Tng_an_RS_CVE_LINK_sent.json'

# Text that we want to get rid of during pre-processing
unwantedText = ['[deleted]', '[removed]', 'url', 'edit', '\n', '\r']
stopWords = list(stopwords.words('english'))

# Set dictionaries to English
dictionary = enchant.Dict("en_US")
#stemmer = SnowballStemmer("english")
lemmatizer = nltk.wordnet.WordNetLemmatizer()

def removeUrlFromString(s):
	s = re.sub(r'http\S+', ' ', s)
	s = re.sub(r'www.\S+', ' ', s)
	return s

def isAlpha(s):
	return re.search('[a-zA-Z]', s)

def processWordByWord(s):
	# This does processing word by word
	words = s.split()
	englishText = ""
	for word in words:
		
		# Make sure the word is lowercase and stripped of extra spaces
		word = word.lower()
		word = word.strip()

		# Make sure the word is alphabatic (we don't care about numbers, or emojis, etc )
		if word and isAlpha(word):

			# Remove punctuation
			word = re.sub(r'[^\w\s]','',word)

			# Make sure the word is not a stopword:
			if word not in stopWords:

				# Make sure the word is English
				#isEnglish = dictionary.check(word)
				if True: #isEnglish:

					# Lemmatize the word
					lemmatizedWord = lemmatizer.lemmatize(word)
					englishText += lemmatizedWord + " "
	return englishText

def removeUnwantedText(text, unwantedWords):
    for word in unwantedWords:
        text = text.replace(word, ' ')
    return text

# Get NLTK default stopwords, and add custom Reddit-related stopwords
stopwords = nltk.corpus.stopwords.words('english')
newStopWords = stopwords.extend(['deleted', 'removed', 'edit', 'url'])

# Go through the input json file line-by-line
with open(outPath + fileName, 'w') as outFile:
	with open(inPath + fileName, 'r') as inFile:
		for line in inFile:

			# Read one json line
			element = json.loads(line.strip())

			# Delete the keys that we are not interested in
			for key in rsFieldsToDelete:
				if key in element:
					del element[key]
			if element['extension']: # We are interested in some but not all of the 'extension' keys 
				for key in rsExtensionFieldsToDelete:
					if key in element['extension']:
						del element['extension'][key]
			
			# Remove things like '\n' and '[deleted]' from selftext and titles
			selftext = removeUnwantedText(element['selftext_m'], unwantedText)
			title = removeUnwantedText(element['title_m'], unwantedText)

			# Remove URLs from selftext and titles
			selftext = removeUrlFromString(selftext)
			title = removeUrlFromString(title)

			# Remove foreign language, stopwords, and lemmatize
			selftext = processWordByWord(selftext)
			title = processWordByWord(title)

			# Replace the original data with the cleaned text
			element['selftext_m'] = selftext.strip()
			element['title_m'] = title.strip()

			# If text and title are not completely empty after the pre-processing
			if element['selftext_m'] and element['title_m']:

				# Write the new line to the output file
				outFile.write(json.dumps(element) + '\n')
