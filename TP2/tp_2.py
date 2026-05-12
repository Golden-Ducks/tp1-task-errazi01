import numpy as np
import string
import contractions
from num2words import num2words
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score
import spacy

nlp = spacy.load("en_core_web_sm")

# Dataset

# Sports docs
d1 = "The gold medal price is high effort"
d2 = "Winning a gold medal needs a high jump"
d3 = "Market for a gold medal is a trade of sweat"
d4 = "The athlete will trade all for a gold medal"

# Finance docs
d5 = "The gold bars price is high today"
d6 = "Investing in gold bars needs a high rate"
d7 = "Market for gold bars is a trade of money"
d8 = "The bank will trade all for gold bars"

dataset = [d1, d2, d3, d4, d5, d6, d7, d8]
ground_truth = np.array([0, 0, 0, 0, 1, 1, 1, 1])


# Preprocessing

def expand_contractions(text):
    return contractions.fix(text)

def normalize_numbers(text):
    words = text.split()
    result = []
    for w in words:
        digits = ''.join(c for c in w if c.isdigit())
        if digits:
            w = w.replace(digits, num2words(int(digits)))
        result.append(w)
    return ' '.join(result)

def remove_punctuation(text):
    table = str.maketrans({p: ' ' for p in string.punctuation})
    return text.translate(table)

def clean(text):
    text = text.lower()
    text = expand_contractions(text)
    text = normalize_numbers(text)
    text = remove_punctuation(text)
    doc = nlp(text)
    tokens = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]
    return ' '.join(tokens)


# Vectorization

def build_vectors(docs, n=1):
    cleaned_docs = [clean(doc) for doc in docs]
    cv = CountVectorizer(ngram_range=(1, n))
    X = cv.fit_transform(cleaned_docs).toarray()
    return X, cv


# Clustering + Evaluation

def fix_label_alignment(predicted, true):
    # KMeans cluster IDs are arbitrary — flip if needed
    flipped = 1 - predicted
    if accuracy_score(true, flipped) > accuracy_score(true, predicted):
        return flipped
    return predicted

def run_experiment(docs, y_true, n_gram, label):
    X, _ = build_vectors(docs, n=n_gram)
    km = KMeans(n_clusters=2, random_state=0).fit(X)
    pred = fix_label_alignment(km.labels_, y_true)

    acc  = accuracy_score(y_true, pred)
    prec = precision_score(y_true, pred, average='macro', zero_division=0)

    print(f"\n── {label} ──")
    print(f"Predicted :    {pred.tolist()}")
    print(f"Ground truth : {y_true.tolist()}")
    print(f"Accuracy   : {acc:.2f}")
    print(f"Precision  : {prec:.2f}")


run_experiment(dataset, ground_truth, n_gram=1, label="1-gram BOW + KMeans")
run_experiment(dataset, ground_truth, n_gram=2, label="2-gram BOW + KMeans")

# With 1-gram both classes share words like "gold", "trade", "high" : poor separation
# With 2-gram "gold medal" vs "gold bars" becomes a distinct feature : perfect separation


# Context Window Vectorization

D1 = "I love cats"
D2 = "Cats are chill"
D3 = "I am late"


def tokenize(text):
    return text.lower().split()

def pad(tokens):
    return ['<s>'] + tokens + ['</s>']

def get_windows(tokens, size=1):
    padded = pad(tokens)
    w = 2 * size + 1
    return [' '.join(padded[i:i+w]) for i in range(len(padded) - w + 1)]

def make_vocab(windows_per_doc):
    all_wins = [w for wins in windows_per_doc for w in wins]
    unique = sorted(set(all_wins))
    return {win: i for i, win in enumerate(unique)}

def doc_to_vector(windows, vocab):
    vec = [0] * len(vocab)
    for w in windows:
        if w in vocab:
            vec[vocab[w]] = 1
    return vec


sentences = [D1, D2, D3]
all_windows = [get_windows(tokenize(s)) for s in sentences]
vocab = make_vocab(all_windows)
vectors = [doc_to_vector(wins, vocab) for wins in all_windows]

print("\n\n── Context Window Vocab ──")
for win, idx in vocab.items():
    print(f"  {idx}: \"{win}\"")

print("\n── Document Vectors ──")
for i, vec in enumerate(vectors):
    print(f"  D{i+1}: {vec}")