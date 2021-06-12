from bs4 import BeautifulSoup, element
from soupsieve.css_types import Selector
import requests
import json
#=============================================================================
def extract_element(dom_tree, selector, attribute = None):
    try:
        if isinstance(attribute, str):
            return dom_tree.select_one(selector)[attribute].strip()
        if isinstance(attribute, list):
            return [e.text.strip() for e in dom_tree.select(selector)]
        return dom_tree.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None
#=============================================================================

features = {
            "review_id" : ["data-entry-id"],
            "author" : ["span.user-post__author-name"],
            "recommendation" : ["span.user-post__author-recomendation"],
            "stars" : ["span.user-post__score-count"],
            "content" : ["div.user-post__text"],
            "pros" :["div.review-feature__title--positives ~ div.review-feature__item", []],
            "cons" : ["div.review-feature__title--negatives ~ div.review-feature__item", []],
            "useful" : ["button.vote-yes"],
            "useless" : ["button.vote-no"],
            "purchased" : ["div.review-pz"],
            "review_date" : ["span.user-post__published > time:nth-child(1)", "datetime"],
            "purchase_date" : ["span.user-post__published > time:nth-child(2)", "datetime"]
        }

all_reviews = []
serivce_url = "https://www.ceneo.pl"
product_id = input("Podaj numer produktu: ")
next_page = f"/{product_id}#tab=reviews"

while next_page:
    response = requests.get(serivce_url + next_page)
    page_dom = BeautifulSoup(response.text, 'html.parser')
    reviews = page_dom.select("div.js_product-review")
    for review in reviews:
        single_review = {key:extract_element(review, *value) for key, value in features.items()}
        single_review["review_id"] = review["data-entry-id"]
        all_reviews.append(single_review)
    next_page = extract_element(page_dom,"a.pagination__next", "href")

with open(f"reviews/{product_id}.json", "w") as jf:
    print(json.dump(all_reviews, jf, ensure_ascii=False, indent=4))
#print(json.dumps(all_reviews, ensure_ascii=False, indent=4))