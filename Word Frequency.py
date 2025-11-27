# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import nltk

# Download the stopwords resource if not already present
nltk.download('stopwords')

# Request the HTML file
url = "https://s3.amazonaws.com/assets.datacamp.com/production/project_147/datasets/2701-h.htm"
r = requests.get(url)  # <-- use variable r

# Set the correct text encoding of the HTML page
r.encoding = 'utf-8'

# Extract HTML
html = r.text

# Parse HTML and extract text
html_soup = BeautifulSoup(html, 'html.parser')
moby_text = html_soup.get_text()

# Tokenize text keeping only alphanumeric words
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(moby_text)

# Convert all tokens to lowercase
words = [token.lower() for token in tokens]

# Remove stopwords for words_no_stop
stop_words = nltk.corpus.stopwords.words('english')
words_no_stop = [word for word in words if word not in stop_words]

# Count word frequencies
count = Counter(words_no_stop)
top_ten = count.most_common(10)

# Print the 10 most common words
print(top_ten)
