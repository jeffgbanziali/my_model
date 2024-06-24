import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import ssl

# Créer un contexte SSL qui n'exige pas de vérification du certificat
ssl._create_default_https_context = ssl._create_unverified_context


def download_images(query, num_images, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    search_url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    count = 0
    for img_tag in img_tags:
        if count >= num_images:
            break
        try:
            img_url = img_tag['src']
            if not img_url.startswith('http'):
                img_url = 'https:' + img_url
            save_path = os.path.join(save_folder, f"{query}_{count}.jpg")
            urllib.request.urlretrieve(img_url, save_path)
            print(f"Downloaded {img_url} to {save_path}")
            count += 1
        except Exception as e:
            print(f"Error downloading image {count}: {e}")


# Catégories et nombre d'images à télécharger pour chaque catégorie
categories = ["éducatif", "divertissement", "inspirant", "lifestyle", "commercial", "événements", "communautaire",
              "informatif", "créatif", "culinaire", "technologique", "santé", "familial", "animaux",
              "écologie", "mode de vie durable", "caritatif", "spirituel", "carrière", "finances",
              "gaming", "programmation", "automobiles", "culture", "photographie"]
num_images_per_category = 50

# Télécharger les images pour chaque catégorie
for category in categories:
    download_images(category, num_images_per_category, f"dataset/{category}")
