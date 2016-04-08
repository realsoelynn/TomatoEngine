from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from nltk.tokenize import word_tokenize
import json

with open('data/tomato_db.json') as data_file:
	data = json.load(data_file);    
	reviews = data["reviews"];
	new_reviews = [];
	count = 0;

	for review in reviews:
		no_of_words = len(word_tokenize(review["review"]))

		try:
			if review["lang"] == 'en' and 80 <= no_of_words <= 170:
				new_reviews.append(review);
				
				count += no_of_words
		except KeyError:
			continue;

	data["reviews"] = new_reviews;

	f = open('data/tomato_db_filtered.json', 'w', encoding='UTF-8');
	f.write(json.dumps(data, indent = 4));
	f.close();

	print(len(new_reviews));
	print(count);
