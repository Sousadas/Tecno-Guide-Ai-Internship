# Day 12 Notes — NLP Basics

Date: 2026-05-29

## Objectives
- Understand core NLP text-processing steps
- Tokenize text and build a spam classifier
- Compare Bag-of-Words vs TF-IDF vectorization
- Evaluate model performance with metrics

## Key Concepts

### Text Preprocessing
- **Lowercasing** – normalises case so "Win" and "win" are treated the same.
- **Punctuation removal** – strips noise characters (`!`, `$`, etc.).
- **Stop-word filtering** – removes common words ("the", "is", "a") that add little signal.

### Vectorization (turning text → numbers)
| Method | How it works | Pros | Cons |
|--------|-------------|------|------|
| **CountVectorizer** (Bag of Words) | Counts how often each word appears | Simple, fast | Treats every word equally |
| **TfidfVectorizer** (TF-IDF) | Weights words by importance (frequent in doc but rare across docs) | Better at surfacing important words | Slightly more complex |

### Classification – MultinomialNB (Naïve Bayes)
- Works well with word-count / frequency features
- Assumes features are independent (the "naïve" part)
- Very fast to train and surprisingly effective for text

### Evaluation Metrics
- **Accuracy** – % of correct predictions
- **Precision** – of items predicted as spam, how many actually are?
- **Recall** – of all actual spam, how many did we catch?
- **F1-score** – harmonic mean of precision & recall
- **Confusion Matrix** – grid showing true vs predicted labels

## What I Learned
- Preprocessing steps (lowercase, punctuation removal, stopwords) are crucial for NLP
- CountVectorizer creates a sparse matrix of word counts
- TF-IDF often outperforms raw counts by down-weighting common words
- `train_test_split` with `stratify` ensures balanced class distribution
- `predict_proba` gives confidence scores alongside predictions

## Next Steps
- Try a larger real-world dataset (e.g., SMS Spam Collection from UCI)
- Experiment with n-grams (`ngram_range=(1,2)`) to capture word pairs
- Try other classifiers (SVM, Logistic Regression)
- Add more preprocessing (stemming / lemmatization with NLTK)
