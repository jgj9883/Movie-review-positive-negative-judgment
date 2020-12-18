from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import numpy


data = []
f = open('p_sample.txt', "r")
while True:
    line = f.readline()
    if not line:
        break
    data.append(line)
f.close()

okt = Okt()
p_set = set()

for i in data:
    y = okt.pos(i, stem=True)
    for j in y:
        if j[1] == 'Noun' or j[1] == 'Verb' or j[1] == 'Adjective':
            p_set.add(j[0])

f = open("p_set.txt", 'w')
for i in p_set:
    f.write(i + ' ')
f.close()

x = list(p_set)

data = []
f = open('n_sample.txt', "r")
while True:
    line = f.readline()
    if not line:
        break
    data.append(line)
f.close()

n_set = set()

for i in data:
    y = okt.pos(i, stem=True)
    for j in y:
        if j[1] == 'Noun' or j[1] == 'Verb' or j[1] == 'Adjective':
            n_set.add(j[0])

f = open("n_set.txt", 'w')
for i in n_set:
    f.write(i + ' ')
f.close()

y = list(n_set)

# tfidf_vectorizer_p = TfidfVectorizer()
# tfidf_vectorizer_p.fit(p_set)
# print(tfidf_vectorizer_p.vocabulary_)
# print(tfidf_vectorizer_p.transform(p_set))
#
#
# tfidf_vectorizer_n = TfidfVectorizer()
# tfidf_vectorizer_n.fit(n_set)
# print(tfidf_vectorizer_n.vocabulary_)
# print(tfidf_vectorizer_n.transform(n_set))

train_x, test_x = train_test_split(x, test_size=0.2, random_state=0)

tfv_p = TfidfVectorizer()
tfv_p.fit(train_x)
tfv_train_x = tfv_p.transform(train_x)
#print(tfv_train_x)

clf = LogisticRegression(random_state=0)
params = {'C' : [1,3,5,7,9]}
grid_cv = GridSearchCV(clf, param_grid=params, cv=4, scoring='accuracy',verbose=1)
grid_cv.fit(tfv_train_x)



