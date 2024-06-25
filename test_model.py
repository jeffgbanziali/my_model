import os
import requests
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Charger le modèle sauvegardé avec compile=False
model = tf.keras.models.load_model('image_classifier_model.keras', compile=False)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# Extraire les sous-catégories automatiquement
def extract_categories(dataset_path):
    categories = []
    for main_category in os.listdir(dataset_path):
        main_category_path = os.path.join(dataset_path, main_category)
        if os.path.isdir(main_category_path):
            for sub_category in os.listdir(main_category_path):
                sub_category_path = os.path.join(main_category_path, sub_category)
                if os.path.isdir(sub_category_path):
                    categories.append(f"{main_category}/{sub_category}")
    return categories


dataset_path = 'dataset'
categories = extract_categories(dataset_path)


# Fonction pour prédire une image donnée
def predict_image(img):
    img = img.resize((224, 224)).convert('RGB')
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    print("Predictions:", predictions)  # Voir les prédictions brutes
    predicted_class = np.argmax(predictions[0])
    confidence = np.max(predictions[0])

    print("Predicted class index:", predicted_class)  # Voir l'index de la classe prédite
    print("Confidence:", confidence)  # Voir la confiance associée à la prédiction

    result_text = f"Predicted class: {categories[predicted_class]}, Confidence: {confidence:.2f}"
    result_label.config(text=result_text)

    img_display = ImageTk.PhotoImage(img)
    panel.configure(image=img_display)
    panel.image = img_display


# Charger une image depuis un fichier
def load_image_from_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        predict_image(img)


# Charger une image depuis une URL
def load_image_from_url():
    url = url_entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        predict_image(img)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load image from URL: {e}")


# Configurer l'interface utilisateur
root = tk.Tk()
root.title("Image Classifier")

# Personnaliser la fenêtre principale
root.geometry("800x700")
root.configure(bg="#e0f7fa")

# Ajouter une étiquette pour le titre
title_label = tk.Label(root, text="Image Classifier", font=("Helvetica", 24, "bold"), bg="#e0f7fa", fg="#00796b")
title_label.pack(pady=20)

# Cadre pour les boutons et les résultats
frame = tk.Frame(root, bg="#e0f7fa")
frame.pack(pady=20)

# Bouton pour charger l'image depuis un fichier
btn_file = tk.Button(frame, text="Select Image from File", command=load_image_from_file, font=("Helvetica", 14),
                     bg="#00796b", fg="white", padx=20, pady=10, bd=0, highlightthickness=0)
btn_file.pack(side=tk.LEFT, padx=20)

# Étiquette pour afficher le résultat
result_label = tk.Label(frame, text="", font=("Helvetica", 16, "italic"), bg="#e0f7fa", fg="#00796b")
result_label.pack(side=tk.LEFT, padx=20)

# Champ d'entrée pour l'URL de l'image
url_frame = tk.Frame(root, bg="#e0f7fa")
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="Enter Image URL:", font=("Helvetica", 14), bg="#e0f7fa", fg="#00796b")
url_label.pack(side=tk.LEFT, padx=5)

url_entry = tk.Entry(url_frame, font=("Helvetica", 14), width=50)
url_entry.pack(side=tk.LEFT, padx=5)

# Bouton pour charger l'image depuis un URL
btn_url = tk.Button(url_frame, text="Load Image from URL", command=load_image_from_url, font=("Helvetica", 14),
                    bg="#00796b", fg="white", padx=20, pady=10, bd=0, highlightthickness=0)
btn_url.pack(side=tk.LEFT, padx=20)

# Panel pour afficher l'image sélectionnée
panel_frame = tk.Frame(root, bg="#e0f7fa", bd=2, relief="sunken")
panel_frame.pack(pady=20)
panel = tk.Label(panel_frame, bg="#e0f7fa")
panel.pack()

# Lancer l'interface
root.mainloop()
