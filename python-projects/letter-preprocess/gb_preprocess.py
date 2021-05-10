from bs4 import BeautifulSoup
import sys

class GBPreprocessor:

    def __init__(self, text):
        self.text = text

    def extract_gb(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        body = soup.body

        temp = body.find_all("dl", {"class": "qnaLists"})
        if len(temp) != 0:
            qnaLists = temp[0]
        else:
            return None, None

        good_ans_list = qnaLists.find_all("b", {"class": "good"})
        bad_ans_list = qnaLists.find_all("b", {"class": "bad"})

        good = []
        for ans in good_ans_list:
            try:
                for span in ans.find_all("span"):
                    span.decompose()
            except:
                pass

            try:
                for br in ans.find_all("br"):
                    br.decompose()
            except:
                pass

            good.append({"target": 1,
                         "content": ans.text})

        bad = []
        for ans in bad_ans_list:
            try:
                for span in ans.find_all("span"):
                    span.decompose()
            except:
                pass

            try:
                for br in ans.find_all("br"):
                    br.decompose()
            except:
                pass

            bad.append({"target": 0,
                        "content": ans.text})

        return good, bad


if __name__ == '__main__':
    file = open("../collector/test/jk-2021-4-30-15-34-6673.txt", 'rt')

    gbp = GBPreprocessor(file)
    good, bad = gbp.extract_gb()

    print(good)
    print(bad)