from konlpy.tag import Hannanum

sentance = '전규빈은 소프트웨어학과 학생이다.'

hannanum = Hannanum()

x = hannanum.morphs(sentance)
print(x)

x = hannanum.nouns(sentance)
print(x)

x = hannanum.pos(sentance)
print(x)

x = hannanum.tagset
print(x)