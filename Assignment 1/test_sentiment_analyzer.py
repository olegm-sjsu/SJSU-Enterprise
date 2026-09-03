"""Tests for sentiment_analyzer.py, including a full-dataset accuracy check."""

import csv
from collections import Counter

import pytest

from sentiment_analyzer import analyze_sentiment, clean_text

CSV_PATH = "test.csv"

# Measured accuracy on the full dataset is ~0.675 (VADER + independently
# tuned positive/negative thresholds); keep a margin below that so this is a
# meaningful regression guard rather than a coin flip.
MIN_ACCURACY = 0.63


def load_rows():
    with open(CSV_PATH, encoding="latin-1") as f:
        reader = csv.DictReader(f)
        return [
            row for row in reader
            if row.get("text") and row.get("text").strip()
        ]


# --- clean_text ---

def test_clean_text_removes_url():
    assert "http" not in clean_text("check this out http://example.com/page")


def test_clean_text_removes_www_url():
    assert "www" not in clean_text("visit www.example.com now")


def test_clean_text_removes_email():
    cleaned = clean_text("contact me at a@b.com please")
    assert "a@b.com" not in cleaned


def test_clean_text_removes_stopwords_case_insensitively():
    cleaned = clean_text("I really LOVE this, check http://x.co or me@x.com")
    tokens = cleaned.lower().split()
    assert "i" not in tokens
    assert "http://x.co" not in cleaned
    assert "me@x.com" not in cleaned


def test_clean_text_preserves_case_and_punctuation_of_kept_words():
    cleaned = clean_text("I really LOVE this movie, check http://x.co or me@x.com")
    assert "LOVE" in cleaned
    assert "movie," in cleaned


def test_clean_text_keeps_negation_words():
    cleaned = clean_text("this is not good")
    tokens = cleaned.lower().split()
    assert "not" in tokens


# --- analyze_sentiment ---

def test_analyze_sentiment_positive():
    assert analyze_sentiment("I absolutely love this, it's wonderful and amazing!") == "Positive"


def test_analyze_sentiment_negative():
    assert analyze_sentiment("This is terrible, I hate it, worst experience ever.") == "Negative"


def test_analyze_sentiment_neutral_empty():
    assert analyze_sentiment("") == "Neutral"


def test_analyze_sentiment_neutral_only_stopwords():
    assert analyze_sentiment("I am the of and") == "Neutral"


def test_analyze_sentiment_negation_flips_polarity():
    assert analyze_sentiment("this movie is not good at all") == "Negative"


# --- accuracy over the full dataset ---

def test_accuracy_over_full_dataset():
    rows = load_rows()
    assert len(rows) > 0

    correct = 0
    per_class_correct = Counter()
    per_class_total = Counter()

    for row in rows:
        actual = row["sentiment"].strip().lower()
        predicted = analyze_sentiment(row["text"]).lower()
        per_class_total[actual] += 1
        if predicted == actual:
            correct += 1
            per_class_correct[actual] += 1

    accuracy = correct / len(rows)

    print(f"\nTotal rows evaluated: {len(rows)}")
    print(f"Overall accuracy: {accuracy:.4f}")
    for cls in sorted(per_class_total):
        total = per_class_total[cls]
        right = per_class_correct[cls]
        print(f"  {cls}: {right}/{total} = {right / total:.4f}")

    assert accuracy >= MIN_ACCURACY
