import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Hannanum
from konlpy.tag import Twitter

hannanum = Hannanum()
df = pd.read_csv("review.csv")

score = df['Star']
text = df['Comment']

han = hannanum.morphs(text)

train_x, test_x, train_y, test_y = train_test_split(text, score, test_size= 0.2, random_state=0)
# print(len(train_x), len(train_y))
# print(len(test_x), len(test_y))
tfv = TfidfVectorizer(tokenizer = Twitter(), ngram_range=(1,2), min_df=3, max_df =0.9) #min_df는 최소 3개이상만 수행 max_df는 너무 자주 나오는 단어는 필요 없음
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)
print(tfv_train_x)