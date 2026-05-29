import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ---------------------------------------------------------------------------
# 1. DATASET
# ---------------------------------------------------------------------------
# A small but realistic labelled dataset.
# label: 1 = spam, 0 = ham (not spam)

messages = [
    # --- SPAM examples ---
    ("Win a FREE iPhone now! Click here immediately!", 1),
    ("Congratulations! You have been selected for a $1000 gift card", 1),
    ("URGENT: Your account will be suspended. Verify now!", 1),
    ("Limited time offer! Buy one get one free!!!", 1),
    ("You won $5000! Claim your prize today", 1),
    ("Free entry to win a brand new car! Text WIN to 12345", 1),
    ("Act now! Special discount just for you, 90% off!", 1),
    ("Make money fast! Work from home and earn $$$", 1),
    ("Click here for exclusive deal! Don't miss out!", 1),
    ("You have won a lottery! Send your details to claim", 1),
    ("Get rich quick! Invest now for guaranteed returns!", 1),
    ("FREE FREE FREE! Call now to claim your reward", 1),
    ("Hot stock tip! Double your money in 24 hours!", 1),
    ("Cheap meds online! No prescription needed!", 1),
    ("Congratulations winner! Reply with your bank details", 1),
    # --- HAM examples ---
    ("Hey, are we still meeting for lunch today?", 0),
    ("Can you send me the project report by Friday?", 0),
    ("Happy birthday! Hope you have a wonderful day", 0),
    ("Meeting rescheduled to 3 PM tomorrow", 0),
    ("Thanks for helping me with the assignment", 0),
    ("Don't forget to pick up groceries on your way home", 0),
    ("I'll be late to the office today, stuck in traffic", 0),
    ("Let's catch up over coffee this weekend", 0),
    ("Please review the attached document and share feedback", 0),
    ("The team dinner is at 7 PM on Saturday", 0),
    ("Can you help me debug this code? I'm stuck", 0),
    ("Great presentation today! Well done", 0),
    ("Reminder: dentist appointment at 10 AM", 0),
    ("I just finished reading that book you recommended", 0),
    ("See you at the gym tomorrow morning", 0),
]

texts  = [msg for msg, _ in messages]
labels = [lbl for _, lbl in messages]

print(f"Dataset size : {len(texts)} messages")
print(f"  Spam : {labels.count(1)}")
print(f"  Ham  : {labels.count(0)}")
print()

# ---------------------------------------------------------------------------
# 2. TEXT PREPROCESSING
# ---------------------------------------------------------------------------

def preprocess(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


print("--- Preprocessing examples ---")
for sample in texts[:3]:
    print(f"  Original : {sample}")
    print(f"  Cleaned  : {preprocess(sample)}")
    print()

# Apply preprocessing to entire dataset
texts_clean = [preprocess(t) for t in texts]

# ---------------------------------------------------------------------------
# 3. TRAIN / TEST SPLIT
# ---------------------------------------------------------------------------
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    texts_clean, labels, test_size=0.3, random_state=42, stratify=labels
)

print(f"Training set : {len(X_train_raw)} messages")
print(f"Test set     : {len(X_test_raw)} messages")
print()

# ---------------------------------------------------------------------------
# 4. VECTORIZATION — Bag of Words (CountVectorizer)
# ---------------------------------------------------------------------------
print("=" * 55)
print("MODEL 1 — CountVectorizer + MultinomialNB")
print("=" * 55)

count_vec = CountVectorizer(stop_words="english")
X_train_bow = count_vec.fit_transform(X_train_raw)
X_test_bow  = count_vec.transform(X_test_raw)

print(f"Vocabulary size : {len(count_vec.vocabulary_)} words")
print(f"Feature matrix  : {X_train_bow.shape}")
print()

# Train
clf_bow = MultinomialNB()
clf_bow.fit(X_train_bow, y_train)

# Evaluate
y_pred_bow = clf_bow.predict(X_test_bow)
print(f"Accuracy: {accuracy_score(y_test, y_pred_bow):.2%}")
print()
print("Classification Report:")
print(classification_report(y_test, y_pred_bow, target_names=["Ham", "Spam"]))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_bow))
print()

# ---------------------------------------------------------------------------
# 5. VECTORIZATION — TF-IDF
# ---------------------------------------------------------------------------
print("=" * 55)
print("MODEL 2 — TfidfVectorizer + MultinomialNB")
print("=" * 55)

tfidf_vec = TfidfVectorizer(stop_words="english")
X_train_tfidf = tfidf_vec.fit_transform(X_train_raw)
X_test_tfidf  = tfidf_vec.transform(X_test_raw)

print(f"Vocabulary size : {len(tfidf_vec.vocabulary_)} words")
print(f"Feature matrix  : {X_train_tfidf.shape}")
print()

# Train
clf_tfidf = MultinomialNB()
clf_tfidf.fit(X_train_tfidf, y_train)

# Evaluate
y_pred_tfidf = clf_tfidf.predict(X_test_tfidf)
print(f"Accuracy: {accuracy_score(y_test, y_pred_tfidf):.2%}")
print()
print("Classification Report:")
print(classification_report(y_test, y_pred_tfidf, target_names=["Ham", "Spam"]))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_tfidf))
print()

# ---------------------------------------------------------------------------
# 6. CLASSIFY NEW / UNSEEN TEXT
# ---------------------------------------------------------------------------
print("=" * 55)
print("CLASSIFYING NEW MESSAGES (using TF-IDF model)")
print("=" * 55)

new_messages = [
    "You have won a free vacation! Call now!",
    "Hey, can we reschedule our meeting to next week?",
    "URGENT! Verify your account or it will be deleted!",
    "Thanks for the birthday wishes, really appreciate it",
    "Get 50% cashback! Limited period offer!!!",
    "Let's discuss the project timeline tomorrow",
]

new_clean  = [preprocess(m) for m in new_messages]
new_vectors = tfidf_vec.transform(new_clean)
predictions = clf_tfidf.predict(new_vectors)
probabilities = clf_tfidf.predict_proba(new_vectors)

for msg, pred, proba in zip(new_messages, predictions, probabilities):
    label = "🚫 SPAM" if pred == 1 else "✅ HAM"
    confidence = max(proba) * 100
    print(f"  {label} ({confidence:.1f}% confident) → \"{msg}\"")

print()
print("Done! Spam detector training and evaluation complete.")
