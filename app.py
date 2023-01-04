import tkinter as tk
from tkinter import filedialog, Checkbutton
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Create the main window
window = tk.Tk()
window.title("Détermination du type d’AP Wifi, par zone")

# Add a button to import the first file
def import_first_file():
  file_path = filedialog.askopenfilename()
  # You can do something with the file here
  print(f"First file imported: {file_path}")
  first_file_button.config(bg="green")

first_file_button = tk.Button(window, text="Importer coordonnées AP", command=import_first_file)
first_file_button.pack(padx=20, pady=20)

# Add a button to import the second file
def import_second_file():
  file_path = filedialog.askopenfilename()
  # You can do something with the file here
  print(f"Second file imported: {file_path}")
  second_file_button.config(bg="green")

second_file_button = tk.Button(window, text="Importer AP Controller", command=import_second_file)
second_file_button.pack(padx=20, pady=20)


# Add a checkbox and label
tableau_distance_var = tk.BooleanVar()
tableau_distance_checkbox = Checkbutton(window, text="Tableau distance", variable=tableau_distance_var)
tableau_distance_checkbox.pack(padx=20, pady=20)

graphique_var = tk.BooleanVar()
graphique_checkbox = Checkbutton(window, text="Graphique", variable=graphique_var)
graphique_checkbox.pack(padx=20, pady=20)

# Add a label to display the image
image_label = tk.Label(window)
image_label.pack(side="right", fill="both", expand=True)

# Add a button to start the process

def start():
  # You can do something with the imported files and checkbox states here
  tableau_distance = tableau_distance_var.get()
  graphique = graphique_var.get()
  print(f"Tableau distance: {tableau_distance}")
  print(f"Graphique: {graphique}")

  # Load and display the image
  image = Image.open("image.png")
  image = ImageTk.PhotoImage(image)
  image_label.config(image=image)
  image_label.image = image

  # Open and display the "Tableau distance" image if the checkbox is checked
  if tableau_distance:
    image = Image.open("tableau_distance.png")
    image.show()

  # Open and display the "Graphique" image if the checkbox is checked
  if graphique:
    image = Image.open("graphique.png")
    image.show()

  # Add a button to open a Matplotlib plot
  def show_plot():
    # Create and display a Matplotlib plot
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()

  plot_button = tk.Button(window, text="Show Plot", command=show_plot)
  plot_button.pack(padx=20, pady=20)


start_button = tk.Button(window, text="Start", command=start)
start_button.pack(padx=20, pady=20)

# Create the footer label
footer_label = tk.Label(window, text="Nicolas Egloff, Alexandro Amarayo, RT2A 2022/2023")

# Pack the footer label at the bottom of the window
footer_label.pack(side="bottom")


# Run the Tkinter event loop
window.mainloop()