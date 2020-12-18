
from konlpy.tag import Okt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
# 데이터 가져오기
df = pd.read_csv("review.csv")
star_arr = df['Star'].values
comment_arr = df['Comment'].values
# print("[원본 평점] : ", star_arr)
# print("[원본 내용] : ", comment_arr)
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
okt = Okt()
noun = []
verb = []
adjective = []
sentence =[]
for i in comment_arr:
    x = okt.morphs(i, stem=True)
    #print("[형태소로 분리] : ", x)
    y = okt.pos(i, stem=True)
    for j in y:
        if j[1] == 'Noun':
            noun.append(j[0])
            sentence.append(noun)
        elif j[1] == 'Verb':
            verb.append(j[0])
            sentence.append(verb)
        elif j[1] == 'Adjective':
            adjective.append(j[0])
            sentence.append(adjective)

print("[명사 추출] :", noun)
print("[명사 개수] :", len(noun))

print("[동사 추출] : ",verb)
print("[동사 개수] :", len(verb))

print("[형용사 추출] : ",adjective)
print("[형용사 개수] :", len(adjective))


#tfidfv = TfidfVectorizer().fit(verb)
#print(tfidfv.transform(verb).toarray())
#print(tfidfv.vocabulary_)

#print(vect.transform(x).toarray())
#print(vect)

train_x, test_x, train_y, test_y = train_test_split( comment_arr, star_arr, test_size=0.2, random_state=0)

tfv_p = TfidfVectorizer()
tfv_p.fit(train_x)
tfv_train_x = tfv_p.transform(train_x)
#print(tfv_train_x)

clf = LogisticRegression(random_state=0)
params = {'C' : [1,3,5,7,9]}
grid_cv = GridSearchCV(clf, param_grid=params, cv=4, scoring='accuracy',verbose=1)
grid_cv.fit(tfv_train_x,train_y)
print(grid_cv.best_params_)
print(grid_cv.best_score_)


a = ['아 너무 재미있어요 꼭 보세요',
     '핵 노잼 너무 재미없어 절대 보지마세요',
     '개 노잼중에 노잼',
     '영화 개망 ']
my_review= tfv_p.transform(a)
print(grid_cv.best_estimator_.predict(my_review))
