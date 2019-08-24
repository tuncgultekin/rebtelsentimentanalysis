import requests
import pickle
from bs4 import BeautifulSoup

page_num = 1
comments = []

while (True):

    print("Page {} is being fetched...".format(page_num))
    # Fetch comment data
    url = "https://www.trustpilot.com/review/www.rebtel.com?page=" + str(page_num)
    response = requests.get(url)

    # Trustpilot returns Http 301 when the requested page number is invalid
    if (len(response.history)>0) and (response.history[-1].status_code==301):
        break    

    # Parse comment 'div's
    html_parser = BeautifulSoup(response.text, "html.parser")
    review_card_list = html_parser.findAll("div", {"class": "review-card"})

    for review_card in review_card_list:
        score = int(review_card.find("div", {"class":"star-rating star-rating--medium"}).find("img").attrs["alt"][0])
        title = review_card.find("h2", {"class":"review-content__title"}).find("a").contents[0]
        title = title.replace("\n"," ").replace("\t"," ").replace("\r"," ").strip()

        body = review_card.find("p", {"class":"review-content__text"}).contents[0]
        body = body.replace("\n"," ").replace("\t"," ").replace("\r"," ").strip()

        comments.append([title, body, score])

    print("Page {} was fetched.".format(page_num))
    page_num = page_num + 1

with open("rebtel_comments.pickle", "wb") as output_file:
    pickle.dump(comments, output_file)

print("{} comment collected.".format(len(comments)))
print("Dataset creation completed.")