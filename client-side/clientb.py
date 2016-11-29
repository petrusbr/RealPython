import requests

r = requests.get("http://news.ycombinator.com")

with open("hackernews.html", "wb") as code:
    code.write(r.content)