import json
from datetime import datetime
from db.models import Author, Quote
import db.connect
import logging


logger = logging.getLogger("json2mongo")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

with open("authors.json", "r", encoding="utf-8") as authors_file:
    a_data = json.load(authors_file)

    for author in a_data:
        auth_i = Author()
        auth_i.fullname = author["fullname"]
        auth_i.born_date = datetime.strptime(author["born_date"], "%B %d, %Y")
        auth_i.born_location = author["born_location"]
        auth_i.description = author["description"]
        auth_i.save()
        logger.info(f"author {author['fullname']} saved")

with open("quotes.json", "r", encoding="utf-8") as quotes_file:
    q_data = json.load(quotes_file)

    for quote in q_data:
        quo_i = Quote()
        quo_i.author = Author.objects.get(fullname=quote["author"])
        quo_i.quote = quote["quote"]
        quo_i.tags = quote["tags"]
        quo_i.save()
        logger.info(f"quote: {quote['quote']} saved")
