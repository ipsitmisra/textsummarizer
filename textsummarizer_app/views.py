from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from spacy.lang.en import English
import numpy as np
from bs4 import BeautifulSoup
import requests
import time


import warnings
warnings.filterwarnings('ignore')

nlp=spacy.load("en_core_web_sm")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

# Create your views here.


def index(request):
    return render(request, 'index.html')


def analyze(request):
    start=time.time()
    if request.method=='POST':
        rawtext=request.POST['rawtext']
        final_reading_time=readingTime(rawtext)
        final_summary=summarizer(rawtext,tokenizer=nlp,max_sent_in_summary=5)
        summary_reading_time=readingTime(final_summary)
        end=time.time()
        final_time=end-start
    output={'ctext':rawtext,
    'final_summary':final_summary,
    'final_time':final_time,
    'final_reading_time':final_reading_time,
    'summary_reading_time':summary_reading_time}
    return render(request,'index.html',output)

def analyze_url(request):
    start=time.time()
    if request.method=='POST':
        raw_url=request.POST['raw_url']
        rawtext=get_text(raw_url)
        final_reading_time=readingTime(rawtext)
        final_summary=summarizer(rawtext,tokenizer=nlp,max_sent_in_summary=5)
        summary_reading_time=readingTime(final_summary)
        end=time.time()
        final_time=end-start

    return render(request,'index.html',{'ctext':rawtext,'final_summary':final_summary,'final_time':final_time,'final_reading_time':final_reading_time,'summary_reading_time':summary_reading_time})

def about(request):
    return render(request,'about.html')

def get_text(link):
    response = requests.get(link,  headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    soup.title
    for title in soup.find_all('title'):
        print(title.get_text())
    t = []
    for txt in soup.find_all('p'):
        #print(txt.get_text())
        t.append(txt.get_text())
    raw_txt = ' '.join([a for a in t]) 
    return raw_txt

#Summarizer function
def summarizer(text, tokenizer, max_sent_in_summary):
    doc = nlp(text.replace("\n", ""))
    sentences = [sent.text.strip() for sent in doc.sents]

    sentence_organizer = {k:v for v,k in enumerate(sentences)}

    tf_idf_vectorizer = TfidfVectorizer(min_df=2,  max_features=None, 
                                        strip_accents='unicode', 
                                        analyzer='word',
                                        token_pattern=r'\w{1,}',
                                        ngram_range=(1, 3), 
                                        use_idf=1,smooth_idf=1,
                                        sublinear_tf=1,
                                        stop_words = 'english')

    tf_idf_vectorizer.fit(sentences)

    sentence_vectors = tf_idf_vectorizer.transform(sentences)

    sentence_scores = np.array(sentence_vectors.sum(axis=1)).ravel()

    N = max_sent_in_summary
    top_n_sentences = [sentences[ind] for ind in np.argsort(sentence_scores, axis=0)[::-1][:N]]

    mapped_top_n_sentences = [(sentence,sentence_organizer[sentence]) for sentence in top_n_sentences]

    mapped_top_n_sentences = sorted(mapped_top_n_sentences, key = lambda x: x[1])
    ordered_scored_sentences = [element[0] for element in mapped_top_n_sentences]

    summary = " ".join(ordered_scored_sentences)
    return summary

# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime