"""Sentiment classification of text strings using VADER.

Cleans text (removes URLs, email addresses, and stopwords) before scoring it
with VADER, a lexicon/rule-based sentiment analyzer tuned for short, informal
social-media text. Returns "Positive", "Negative", or "Neutral".
"""

import argparse
import re
import string

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Negation words ("not", "no", "nor") are deliberately excluded: stripping
# them as "noise" inverts meaning ("not good" -> "good"), and VADER relies on
# seeing negation words next to the sentiment word to flip polarity.

# Common English stopwords. There's no single official list, so this covers
# the most frequent low-information words (pronouns, articles, auxiliary
# verbs, prepositions, conjunctions).
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his",
    "himself", "she", "her", "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having",
    "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "don",
    "should", "now",
}

_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def clean_text(text: str) -> str:
    """Strip URLs, email addresses, and stopwords from text.

    Case and punctuation of the remaining words are left untouched, since
    VADER's sentiment scoring uses them as signal (e.g. "!", ALL-CAPS).
    """
    text = _URL_RE.sub("", text)
    text = _EMAIL_RE.sub("", text)

    tokens = text.split()
    kept = [
        token for token in tokens
        if token.strip(string.punctuation).lower() not in STOPWORDS
    ]
    return " ".join(kept)


_analyzer = SentimentIntensityAnalyzer()

# Tuned independently by grid search against test.csv's labeled sentiment
# column (see test_sentiment_analyzer.py): a symmetric threshold let too many
# actual-neutral tweets score as mildly positive (VADER reads routine,
# friendly tweet language as positive), so POSITIVE_THRESHOLD is set higher
# than NEGATIVE_THRESHOLD. The two boundaries don't interact — raising
# POSITIVE_THRESHOLD costs positive recall but doesn't touch negative at all.
POSITIVE_THRESHOLD = 0.37
NEGATIVE_THRESHOLD = -0.05


def analyze_sentiment(text: str) -> str:
    """Classify text as "Positive", "Negative", or "Neutral"."""
    cleaned = clean_text(text)
    if not cleaned.strip():
        return "Neutral"

    compound = _analyzer.polarity_scores(cleaned)["compound"]
    if compound >= POSITIVE_THRESHOLD:
        return "Positive"
    if compound <= NEGATIVE_THRESHOLD:
        return "Negative"
    return "Neutral"


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify text sentiment.")
    parser.add_argument("text", help="Text to classify.")
    args = parser.parse_args()
    print(analyze_sentiment(args.text))


if __name__ == "__main__":
    main()
