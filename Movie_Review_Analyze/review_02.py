# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import urllib
import pandas as pd

class Review :
    def __init__(self, comment, date, star, good, bad) :
        self.comment = comment
        self.date = date
        self.star = star
        self.good = good
        self.bad = bad

    def show(self) :
        print("내용 : " + self.comment +
              "\n날짜 : " + self.date +
              "\n별점 : " + self.star +
              "\n좋아요 : " + self.good +
              "\n싫어요 : " + self.bad )

def crawl(url) :
    soup = BeautifulSoup(urllib.request.urlopen(url), "html.parser")
    review_list = []
    title = soup.find('h3', class_='h_movie').find('a').text
    div = soup.find('div', class_="score_result")
    data_list = div.select("ul > li")

    for review in data_list :
        star = review.find("div", class_="star_score").text.strip()
        reply = review.find("div", class_= "score_reple")
        comment = reply.find("p").text.strip()
        date = reply.select("dt > em")[1].text.strip()
        button = review.find("div", class_="btn_area")
        sympathy = button.select("strong")
        good = sympathy[0].text
        bad = sympathy[1].text
        review_list.append(Review(comment, date, star, good, bad))

    return title, review_list

def get_summary(review_list) :
        title_list = []
        star_list = []
        good_list = []
        bad_list = []
        comment_list = []

        for review in review_list :
            title_list.append(str(title))
            star_list.append(int(review.star))
            good_list.append(int(review.good))
            bad_list.append(int(review.star))
            comment_list.append(str(review.comment))

        star_series = pd.Series(star_list)
        good_series = pd.Series(good_list)
        bad_series = pd.Series(bad_list)
        comment_series = pd.Series(comment_list)
        title_series = pd.Series(title_list)

        summary = pd.DataFrame({
            'title' : title_series,
            'Star' : star_series,
            'Good' : good_series,
            'Bad': bad_series,
            'Score': good_series / (good_series + bad_series),
            'Comment' : comment_series
        })
        return summary


movie_code =[189069, 182234, 188909, 178351, 185917]
review_lists= []

for i in movie_code:
    title, list_list = crawl("https://movie.naver.com/movie/bi/mi/basic.nhn?code=" +str(i))
    summary = get_summary(list_list)
    print("[%s]" %(title))
    print(summary)

    summary.to_csv("review.csv", mode='a')



