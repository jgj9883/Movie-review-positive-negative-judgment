from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import pandas as pd

df = pd.read_csv("test.csv")
score = df['score'].values.astype('U')
text = df['text'].values.astype('U')
okt = Okt()

train_x, test_x, train_y, test_y = train_test_split(text, score, test_size=0.2, random_state=0)

# print(len(train_x))
# print(len(train_y))
# print(len(test_x))
# print(len(test_y))
tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1, 2), min_df=3,
                      max_df=0.9)  # min_df, max_df 너무 적거나 많은 빈도수를 가진 단어는 중요하지 않거나 특징이 안되어 제외하는것이 좋음
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)

clf = LogisticRegression(random_state=0)
params = {'C': [1, 3, 5, 7, 9]}
grid_cv = GridSearchCV(clf, param_grid=params, cv=4, scoring='accuracy', verbose=1)
grid_cv.fit(tfv_train_x, train_y)
print(grid_cv.best_params_)
print(grid_cv.best_score_)


my_review = tfv.transform(test_x)
review = grid_cv.best_estimator_.predict(my_review)
print(review)
for i in range(len(test_x)):
    if test_x[i] == 'nan' :
        print('')
    else :
         if review[i] == '1':
            print(test_x[i] + ">>>>>>>>>>>>>>>>>>> 이 리뷰는 긍정입니다.")
            print("--------------------------")
         elif review[i] == '0':
            print(test_x[i] + ">>>>>>>>>>>>>>>>>>>: 이 리뷰는 부정입니다.")
            print("--------------------------")


