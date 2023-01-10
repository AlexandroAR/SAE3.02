import tkinter as tk
from tkinter import filedialog, Checkbutton
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Créer la fenêtre principale
window = tk.Tk()
window.title("Détermination du type d’AP Wifi, par zone")

# Ajouter un bouton pour importer le premier fichier
def import_first_file():
  file_path = filedialog.askopenfilename()
  # Vous pouvez faire quelque chose avec le fichier ici
  print(f"Premier fichier importé: {file_path}")
  first_file_button.config(bg="green")

first_file_button = tk.Button(window, text="Importer coordonnées AP", command=import_first_file)
first_file_button.pack(padx=20, pady=20)

# Ajouter un bouton pour importer le second fichier
def import_second_file():
  file_path = filedialog.askopenfilename()
  # Vous pouvez faire quelque chose avec le fichier ici
  print(f"Deuxième fichier importé: {file_path}")
  second_file_button.config(bg="green")

second_file_button = tk.Button(window, text="Importer AP Controller", command=import_second_file)
second_file_button.pack(padx=20, pady=20)


# Ajouter une case à cocher et une étiquette
tableau_distance_var = tk.BooleanVar()
tableau_distance_checkbox = Checkbutton(window, text="Tableau distance", variable=tableau_distance_var)
tableau_distance_checkbox.pack(padx=20, pady=20)

graphique_var = tk.BooleanVar()
graphique_checkbox = Checkbutton(window, text="Graphique", variable=graphique_var)
graphique_checkbox.pack(padx=20, pady=20)

# Ajouter une étiquette pour afficher l'image
image_label = tk.Label(window)
image_label.pack(side="right", fill="both", expand=True)

# Définir la fonction show_plot et la variable globale plot_button
def show_plot():
  # Créer et afficher un graphique Matplotlib
  plt.plot([1, 2, 3, 4])
  plt.ylabel('quelques nombres')
  plt.show()

plot_button = None

def start():
  # Vous pouvez faire quelque chose avec les fichiers importés et les états de la case à cocher ici
  global plot_button
  tableau_distance = tableau_distance_var.get()
  graphique = graphique_var.get()
  print(f"Tableau distance: {tableau_distance}")
  print(f"Graphique: {graphique}")

  # Charger et afficher l'image
  image = Image.open("image.png")
  image = ImageTk.PhotoImage(image)
  image_label.config(image=image)
  image_label.image = image

  # Ouvrir et afficher l'image "Tableau distance" si la case à cocher est cochée
  if tableau_distance:
    image = Image.open("tableau_distance.png")
    image.show()

  # Ouvrir et afficher l'image "Graphique" si la case à cocher est cochée
  if graphique:
    image = Image.open("graphique.png")
    image.show()

  # Supprimer le bouton plot_button s'il existe
  if plot_button is not None:
    plot_button.pack_forget()

  # Créer un nouveau bouton plot_button et l'afficher
  plot_button = tk.Button(window, text="Show Plot", command=show_plot)
  plot_button.pack(padx=20, pady=20)

# Ajouter un bouton pour démarrer le processus
start_button = tk.Button(window, text="Start", command=start)
start_button.pack(padx=20, pady=20)


# Ajouter un bouton pour générer un résultat aléatoire
def random_generation():
  # Vous pouvez faire quelque chose avec les fichiers importés et les états de la case à cocher ici

  global plot_button
  tableau_distance = tableau_distance_var.get()
  graphique = graphique_var.get()
  print(f"Tableau distance: {tableau_distance}")
  print(f"Graphique: {graphique}")

  # Charger et afficher l'image
  image = Image.open("image.png")
  image = ImageTk.PhotoImage(image)
  image_label.config(image = image)
  image_label.image = image

  # Ouvrez et affichez l'image "Tableau distance" si la case est cochée.
  if tableau_distance:
    image = Image.open("tableau_distance.png")
    image.show()

  # Ouvrez et affichez l'image "graphique" si la case est cochée.
  if graphique:
    image = Image.open("graphique.png")
    image.show()

# Remove the plot_button if it exists
  if plot_button is not None:
    plot_button.pack_forget()

  # Supprimez le bouton plot_button s'il existe
  plot_button = tk.Button(window, text="Show Plot", command=show_plot)
  plot_button.pack(padx=20, pady=20)

random_generation_button = tk.Button(window, text="Random Generation", command=random_generation)
random_generation_button.pack(padx=20, pady=20)

# Créez l'étiquette du pied de page
footer_label = tk.Label(window, text="Nicolas Egloff, Alexandro Amarayo, RT2A 2022/2023")

# L'afficher en bas de la fenêtre
footer_label.pack(side="bottom")

# Exécuter la boucle d'événement de Tkinter
window.mainloop()
