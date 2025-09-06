import re, math, random, io, csv
from collections import Counter

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been before 
being below between both but by can could did do does doing down during each few for 
from further had has have having he her here hers herself him himself his how i if in 
into is it its itself just me more most my myself no nor not of off on once only or 
other our ours ourselves out over own same shall she should so some such than that 
the their theirs them themselves then there these they this those through to too under 
until up very was we were what when where which while who whom why with would you your 
yours yourself yourselves
""".split())

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def split_sentences(text):
    text = clean_text(text)
    return re.split(r"(?<=[.!?])\s+", text)

def tokenize(text):
    return re.findall(r"[A-Za-z]+", text.lower())

def word_freq(tokens):
    return Counter([t for t in tokens if t not in STOPWORDS])

def summarize_text(text, max_sentences=5):
    sents = split_sentences(text)
    tokens = tokenize(text)
    freqs = word_freq(tokens)
    scores = []
    for s in sents:
        stoks = tokenize(s)
        if not stoks: continue
        score = sum(freqs.get(t, 0) for t in stoks) / math.sqrt(len(stoks))
        scores.append((score, s))
    top = sorted(scores, key=lambda x: x[0], reverse=True)[:max_sentences]
    selected = [s for _, s in sorted(top, key=lambda x: sents.index(x[1]))]
    return " ".join(selected)

def generate_mcqs(text, n=5):
    sents = split_sentences(text)
    tokens = tokenize(text)
    freqs = word_freq(tokens)
    keywords = [w for w, _ in freqs.most_common(30)]
    mcqs = []
    for w in keywords:
        for s in sents:
            if w in s.lower():
                q = s.replace(w, "_____")
                options = [w] + random.sample([t for t in keywords if t != w], min(3, len(keywords)-1))
                random.shuffle(options)
                mcqs.append({"question": q, "answer": w, "options": options})
                break
        if len(mcqs) >= n:
            break
    return mcqs

def generate_flashcards(text, n=10):
    tokens = tokenize(text)
    freqs = word_freq(tokens)
    top = [w for w, _ in freqs.most_common(n)]
    cards = []
    for t in top:
        cards.append({"front": t.capitalize(), "back": f"Meaning or context for {t}"})
    return cards

def export_flashcards_csv(cards):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Front", "Back"])
    for c in cards:
        writer.writerow([c["front"], c["back"]])
    return output.getvalue().encode("utf-8")
