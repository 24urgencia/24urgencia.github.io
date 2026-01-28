import requests
from bs4 import BeautifulSoup
import os
import yaml
from unidecode import unidecode

BLOG_URL = "https://atlasmicologia.blogspot.com"

def slugify(text):
    text = unidecode(text).lower()
    return "".join(c if c.isalnum() else "-" for c in text).strip("-")

def fetch_posts():
    response = requests.get(BLOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("h3", class_="post-title")
    return posts

def save_post(title, content, folder):
    slug = slugify(title)
    path = f"{folder}/{slug}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"---\ntitle: \"{title}\"\n---\n\n{content}")

def main():
    os.makedirs("_fungos", exist_ok=True)
    os.makedirs("_clinica", exist_ok=True)

    posts = fetch_posts()

    for post in posts:
        title = post.text.strip()
        link = post.find("a")["href"]

        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        content = soup.find("div", class_="post-body").decode_contents()

        if "clínica" in title.lower():
            save_post(title, content, "_clinica")
        else:
            save_post(title, content, "_fungos")

if __name__ == "__main__":
    main()

