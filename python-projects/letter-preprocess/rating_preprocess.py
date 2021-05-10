from bs4 import BeautifulSoup
import sys

class RatingPreprocessor:

    def __init__(self, text):
        self.text = text

    def extract_rating(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        body = soup.body

        temp = body.find_all("div", {"class": "adviceTotal"})
        if len(temp) != 0:
            advice = temp[0]
        else:
            return None

        grade = advice.find_all("span", {"class": "grade"})  # 자소서 평점
        if len(grade) == 0:
            return None

        temp = body.find_all("dl", {"class": "qnaLists"})
        if len(temp) != 0:
            qnaList = temp[0]
        else:
            return None

        ddList = qnaList.find_all("dd")
        answer = ""
        for dd in ddList:
            ans = dd.find_all("div", {"class": "tx"})[0]
            for span in ans.find_all("span"):
                span.decompose()
            answer += ans.text

        ret = {"rating": float(grade[0].text.strip()),
               "content": answer}

        return ret

if __name__ == '__main__':
    file = open("../collector/test/jk-2021-4-30-15-34-6673.txt", 'rt')

    rp = RatingPreprocessor(file)
    result = rp.extract_rating()

    print(result)
    print(result['rating'])