import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import nltk
import time
from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import TextBlob
import re

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Load input file
df = pd.read_excel("Input.xlsx")

# Create folder for extracted articles
if not os.path.exists("Extracted_Articles"):
    os.makedirs("Extracted_Articles")

# Load positive and negative words
positive_words = set(open("MasterDictionary/positive-words.txt", "r", encoding="utf-8").read().split())
negative_words = set(open("MasterDictionary/negative-words.txt", "r", encoding="utf-8").read().split())


def extract_text(url, url_id, max_retries=3):
    """Extracts text from a given URL and saves it in a text file."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.find("title").text.strip() if soup.find("title") else "No Title"
            paragraphs = soup.find_all("p")
            content = "\n".join([p.text.strip() for p in paragraphs])

            if not content.strip():
                raise ValueError("No valid content found on the page.")

            with open(f"Extracted_Articles/{url_id}.txt", "w", encoding="utf-8") as file:
                file.write(title + "\n\n" + content)

            return content
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            time.sleep(2)

    print(f"Skipping {url} after {max_retries} failed attempts.")
    return None


def count_syllables(word):
    return len(re.findall(r'[aeiouy]+', word.lower()))


def count_complex_words(words):
    return sum(1 for word in words if count_syllables(word) > 2)


def analyze_text(text):
    """Performs text analysis and computes required variables."""
    if not text:
        return None

    words = word_tokenize(text.lower())
    sentences = sent_tokenize(text)

    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = TextBlob(text).sentiment.polarity
    subjectivity_score = TextBlob(text).sentiment.subjectivity
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    complex_word_count = count_complex_words(words)
    percentage_complex_words = (complex_word_count / len(words)) * 100 if words else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
    word_count = len(words)
    syllable_per_word = sum(count_syllables(word) for word in words) / word_count if word_count else 0
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in words) / word_count if word_count else 0

    return {
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
        "COMPLEX WORD COUNT": complex_word_count,
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllable_per_word,
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": avg_word_length
    }


results = []
for _, row in df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]

    print(f"Processing: {url}")
    text = extract_text(url, url_id)

    analysis = analyze_text(text)
    if analysis:
        results.append({"URL_ID": url_id, **analysis})

output_df = pd.DataFrame(results)
output_df.to_excel("Final_Output.xlsx", index=False)

print("Processing completed. Output saved to Final_Output.xlsx")
