import re
import math
import numpy as np
from sklearn.datasets import fetch_20newsgroups


# Load Data

corpus = fetch_20newsgroups(
    subset='train',
    remove=('headers', 'footers', 'quotes')
).data[:3000]


# Step 1 — Preprocessing

def preprocess(text):
    # keep only lowercase letters and spaces
    text = re.sub(r'[^a-z\s]', '', text.lower())
    return text.split()


# Step 2 — Build Vocabulary

def build_vocab(docs):
    tokens = set()
    for doc in docs:
        tokens.update(preprocess(doc))
    return sorted(tokens)


# Step 3 — Document Frequency

def compute_df(docs, vocab):
    df = dict.fromkeys(vocab, 0)
    for doc in docs:
        unique_tokens = set(preprocess(doc))
        for token in unique_tokens:
            if token in df:
                df[token] += 1
    return df


# Step 4 — IDF with Smoothing

def compute_idf(df, N):
    # smoothed IDF: log((N+1)/(df+1)) + 1
    # avoids division by zero and prevents log(1)=0 for words in all docs
    return {word: math.log((N + 1) / (count + 1)) + 1 for word, count in df.items()}


# Step 5 — TF Vector

def compute_tf(doc, vocab):
    tokens = preprocess(doc)
    if not tokens:
        return [0.0] * len(vocab)
    total = len(tokens)
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return [freq.get(word, 0) / total for word in vocab]


# Step 6 — TF-IDF Matrix

def build_tfidf(docs):
    vocab = build_vocab(docs)
    df   = compute_df(docs, vocab)
    idf  = compute_idf(df, len(docs))

    matrix = []
    for doc in docs:
        tf  = compute_tf(doc, vocab)
        vec = [tf_val * idf[word] for tf_val, word in zip(tf, vocab)]
        matrix.append(vec)

    return matrix, vocab


# Step 7 — Cosine Similarity

def cosine_sim(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return np.dot(a, b) / denom


# Step 8 — Search Engine

def search(query, docs, top_k=5):
    matrix, vocab = build_tfidf(docs)

    # build query vector (raw TF, then normalize)
    q_tokens = preprocess(query)
    q_vec = np.array([q_tokens.count(w) for w in vocab], dtype=float)
    total = q_vec.sum()
    if total > 0:
        q_vec /= total

    scores = [(cosine_sim(q_vec, matrix[i]), i) for i in range(len(docs))]
    scores.sort(reverse=True)
    return scores[:top_k]


# Test

query = "machine learning neural network"
results = search(query, corpus)

print(f"Top {len(results)} results for: \"{query}\"\n")
for score, idx in results:
    print(f"Score: {score:.4f}")
    print(corpus[idx][:200])
    print("-" * 60)