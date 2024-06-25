import os
import requests
from PIL import Image
from io import BytesIO
import time
from random import randint

# Remplacez 'YOUR_PEXELS_API_KEY_HERE' par votre clé d'API Pexels
PEXELS_API_KEY = 'k84hdLYdZdQ8J0ztfa61znROwqkgrdxCcZbyQKQlCKCxVWjrSehTZmqQ'


def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.save(save_path)
        print(f"Downloaded {url} to {save_path}")
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")


def search_and_download_images_pexels(query, num_images, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    headers = {
        'Authorization': PEXELS_API_KEY
    }
    search_url = f"https://api.pexels.com/v1/search?query={query}&per_page={num_images}"

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for idx, photo in enumerate(data['photos']):
            img_url = photo['src']['original']
            save_path = os.path.join(save_folder, f"{query.replace(' ', '_')}_pexels_{idx}.jpg")
            download_image(img_url, save_path)
            time.sleep(randint(1, 3))  # Attendre entre 1 et 3 secondes entre les téléchargements
    except Exception as e:
        print(f"Error fetching images from Pexels: {e}")


def search_and_download_images(query, num_images, save_folder):
    search_and_download_images_pexels(query, num_images, save_folder)


# Catégories principales et leurs sous-catégories
categories = {
    "éducatif": ["école", "université", "formation en ligne", "tutorat", "cours"],
    "divertissement": ["cinéma", "musique", "jeux", "sports", "parcs"],
    "inspirant": ["citations", "histoires de succès", "motivation", "leadership", "développement personnel"],
    "lifestyle": ["voyages", "mode", "fitness", "bien-être", "gastronomie"],
    "commercial": ["publicité", "marketing", "entreprise", "commerce électronique", "vente"],
    "événements": ["mariages", "concerts", "conférences", "festivals", "foires"],
    "communautaire": ["associations", "bénévolat", "entraide", "projets locaux", "initiatives sociales"],
    "informatif": ["actualités", "documentaires", "reportages", "articles", "blogs"],
    "créatif": ["art", "design", "photographie", "sculpture", "peinture"],
    "culinaire": ["recettes", "plats", "chefs", "restaurants", "cuisine du monde"],
    "technologique": ["gadgets", "logiciels", "applications", "innovations", "IA"],
    "santé": ["médecine", "exercices", "nutrition", "maladies", "thérapies"],
    "familial": ["famille", "enfants", "parentalité", "activités familiales", "maison"],
    "animaux": ["chiens", "chats", "oiseaux", "animaux sauvages", "animaux de ferme"],
    "écologie": ["environnement", "nature", "recyclage", "énergies renouvelables", "faune"],
    "mode de vie durable": ["zéro déchet", "éco-responsable", "permaculture", "produits bio", "éco-tourisme"],
    "caritatif": ["ONG", "aide humanitaire", "collectes de fonds", "solidarité", "actions sociales"],
    "spirituel": ["méditation", "yoga", "religion", "philosophie", "pratiques spirituelles"],
    "carrière": ["emploi", "entrepreneuriat", "réseautage", "compétences professionnelles", "formation continue"],
    "finances": ["investissement", "épargne", "banque", "budget", "cryptomonnaie"],
    "gaming": ["jeux vidéo", "esport", "jeux de société", "jouets", "jeux de rôle"],
    "programmation": ["code", "développement web", "applications mobiles", "data science", "cybersécurité"],
    "automobiles": ["voitures", "motos", "courses automobiles", "équipements", "entretien"],
    "culture": ["histoire", "traditions", "arts", "littérature", "langues"],
    "photographie": ["paysages", "portraits", "photographie de rue", "photos de voyage", "photographie animalière"]
}

num_images_per_category = 10

# Télécharger les images pour chaque catégorie et sous-catégorie
for main_category, sub_categories in categories.items():
    for sub_category in sub_categories:
        query = f"{main_category} {sub_category}"
        print(f"Downloading images for category: {query}")
        search_and_download_images(query, num_images_per_category, f"dataset/{main_category}/{sub_category}")
