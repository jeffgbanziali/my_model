import tensorflow as tf

# Charger le modèle sauvegardé avec compile=False
model = tf.keras.models.load_model('image_classifier_model.keras', compile=False)

# Re-compiler le modèle
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Redéfinir explicitement l'entrée du modèle
input_shape = (224, 224, 3)
inputs = tf.keras.Input(shape=input_shape)
outputs = model(inputs)

# Créer un nouveau modèle avec l'entrée définie
new_model = tf.keras.Model(inputs=inputs, outputs=outputs)

# Re-sauvegarder le modèle au format HDF5
new_model.save('image_model.h5')
