import re
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, precision_score
# Class 1: 
doc1 = "The gold medal price is high effort"
doc2 = "Winning a gold medal needs a high jump"
doc3 = "Market for a gold medal is a trade of sweat"
doc4 = "The athlete will trade all for a gold medal"
# Class 2: 
doc5 = "The gold bars price is high today"
doc6 = "Investing in gold bars needs a high rate"
doc7 = "Market for gold bars is a trade of money"
doc8 = "The bank will trade all for gold bars"

# task1
def preprocess_text(text):
    text = text.lower()
    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # toknization
    tokens = text.split()
    return tokens

def vectorize(docs, n_gram_size=1):
    # Implement n-gram extrction and vectorzation
    docs_list = []
    for doc in docs:
        tokens = preprocess_text(doc)
            #creat n-gram
        ngram=[]
        for i in range(len(tokens) - n_gram_size + 1):
            grm = " ".join(tokens[i:i+n_gram_size])
            ngram.append(grm)
        docs_list.append(ngram)

    vocab = sorted(set(g for doc in docs_list for g in doc))
    index = {word:i for i,word in enumerate(vocab)}
        # Create document to vector
    vectors = []
    for doc in docs_list:
        v= [0]*len(vocab)

        for word in doc:
            v[index[word]] += 1
        vectors.append(v)
    return np.array(vectors)

# Training / Clustering
all_docs = [doc1, doc2, doc3, doc4, doc5, doc6, doc7, doc8]

# 1-gram Experiment
X1 = vectorize(all_docs, n_gram_size=1)
km1 = KMeans(n_clusters=2, random_state=42).fit(X1)

# 2-gram Experiment
X2 = vectorize(all_docs, n_gram_size=2)
km2 = KMeans(n_clusters=2, random_state=42).fit(X2)

print(f"1-gram clusters: {km1.labels_}")
print(f"2-gram clusters: {km2.labels_}")

# compare acuracy + precision
true_label = [0, 0, 0, 0, 1, 1, 1, 1]  
p1 = km1.labels_
p2 = km2.labels_
acc1 = accuracy_score(true_label, p1)
prec1 = precision_score(true_label, p1)
acc2 = accuracy_score(true_label, p2)
prec2 = precision_score(true_label, p2)

print("\n compare accuracy and precision ")
print(f"1-gram = Accuracy: {acc1:.2f}, Precision: {prec1:.2f}")
print(f"2-gram = Accuracy: {acc2:.2f}, Precision: {prec2:.2f}")

if acc2 > acc1:
    print("2-gram is better because it understands phrases ")
elif acc1 > acc2:
    print("1-gram work better.")
else:
    print("Both give similar result.")

#task2 
# Documents
D1 = "I love cats"
D2 = "Cats are chill"
D3 = "I am late"

def add_padding(tokens):
     return ["<s>"] + tokens + ["</s>"]
def extract_windows(tokens, window_size=1):
    windows = []
    for i in range(window_size, len(tokens)-window_size):
        windw = tokens[i-window_size:i+window_size+1]
        windows.append(" ".join(windw))
    return windows

def build_vocab(all_windows):
    vocab = sorted(set(all_windows))
    indexvoc = {w:i for i,w in enumerate(vocab)}
    return vocab, indexvoc

def vectorize_doc(doc_windows, indexvoc):
    vector = [0]*len(indexvoc)
    for w in doc_windows:
        if w in indexvoc:
            vector[indexvoc[w]] = 1
    return vector

# Run
all_docs = [D1, D2, D3]
doc_windows = []
all_windows = []

for doc in all_docs:

    tokens = preprocess_text(doc)
    tokens = add_padding(tokens)
    windows = extract_windows(tokens,1)

    doc_windows.append(windows)
    all_windows.extend(windows)
vocab, vocab_index = build_vocab(all_windows)

print("\nVocabulary:")
print(vocab)
print("\nVectors:")

i=0
while i < len(doc_windows):
    vec = vectorize_doc(doc_windows[i], vocab_index)
    print(f"D{i+1}:", vec) 
    i += 1