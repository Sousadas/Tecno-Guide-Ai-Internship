from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

texts = ['Win money now', 'Hello friend', 'Limited offer', 'Meeting today']
labels = [1,0,1,0]
cv = CountVectorizer()
X = cv.fit_transform(texts)
clf = MultinomialNB()
clf.fit(X, labels)
print('Trained tiny spam detector')
