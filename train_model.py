import os
import ssl
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Ignorer la vérification SSL pour télécharger les poids pré-entraînés
ssl._create_default_https_context = ssl._create_unverified_context

# Définir la forme d'entrée
input_shape = (224, 224, 3)

# Charger le modèle pré-entraîné MobileNetV2 sans les couches de classification supérieures
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)

# Ajouter des couches de classification personnalisées
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)  # Ajout de Dropout pour régularisation
num_classes = 25  # Assurez-vous que ce nombre correspond au nombre de sous-catégories que vous avez
predictions = Dense(num_classes, activation='softmax')(x)

# Créer le modèle complet
model = Model(inputs=base_model.input, outputs=predictions)

# Geler les couches de base du modèle pré-entraîné
for layer in base_model.layers:
    layer.trainable = False

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Préparer les données avec augmentation
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    horizontal_flip=True,
    zoom_range=0.2,
    validation_split=0.2
)

# Générateur de données d'entraînement
train_generator = train_datagen.flow_from_directory(
    'dataset/',  # Assurez-vous que ce chemin est correct
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

# Générateur de données de validation
validation_generator = train_datagen.flow_from_directory(
    'dataset/',  # Assurez-vous que ce chemin est correct
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Définir les callbacks
checkpoint = ModelCheckpoint('best_model.keras', monitor='val_accuracy', save_best_only=True, mode='max')
early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, mode='max')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.00001, mode='min')

# Entraîner le modèle
model.fit(
    train_generator,
    epochs=10,  # Augmentez ce nombre si nécessaire
    validation_data=validation_generator,
    callbacks=[checkpoint, early_stopping, reduce_lr]
)

# Sauvegarder le modèle final en format .keras
model.save('image_classifier_model.keras')
