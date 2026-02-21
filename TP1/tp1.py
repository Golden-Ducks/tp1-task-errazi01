import re
import nltk
import spacy

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

print("\n1. text cleaning")
text = "Hello!! This is a TEST text... with $pecial ch@racters & numbers 123."

# Lowercase
text_clean = text.lower()
print("Lowercase:", text_clean)

# Remove everything except letters, numbers, and whitespace
text_clean = re.sub(r'[^\w\s]', '', text_clean)
print("Cleaned:", text_clean)

# Regex examples
print("\n1.2.Regex Example")
test = "Hi there!\nhow are you?"

print("Whitespace chars found:", re.findall(r'\s', test))
print("Non-whitespace chars found:", re.findall(r'\S', test))


print("\n2. Tokenization")
sentence = "I like python!"

# Simple split
tokens = sentence.split()
print("Simple split:", tokens)

# Using NLTK
from nltk.tokenize import word_tokenize
tokens_nltk = word_tokenize(sentence)
print("NLTK tokens:", tokens_nltk)

# Using spaCy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Say something !")
tokens_spacy = [token.text for token in doc]
print("spaCy tokens:", tokens_spacy)

print("\n3. Stopword Removal")

from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

text = "This is a sample sentence, showing off the stop words filtration."
tokens = word_tokenize(text)

# Keep only words that are NOT stopwords
filtered = [word for word in tokens if word.lower() not in stop_words]
print("Original:", tokens)
print("After stopword removal:", filtered)