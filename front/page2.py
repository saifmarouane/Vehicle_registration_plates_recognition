import csv
import io
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2  # Assurez-vous d'avoir OpenCV installé pour obtenir la durée de la vidéo

#import detect from cars
import sys
import os
# Déclaration globale pour processing_text
processing_text = None
# Ajouter le dossier parent au chemin de recherche
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# Importer la fonction detect depuis cars.py
from addmissingdata import addmissingdata
from cars import detect

# Déclaration des variables globales pour les labels
video_name_label = None
video_duration_label = None
def creer_interface2(root):
    global video_name_label, video_duration_label  # Déclaration des variables globales ici
    
    # Supprimer les anciens widgets de la première page
    for widget in root.winfo_children():
        widget.destroy()

    # Barre de navigation
    navbar = tk.Frame(root, bg="#808080", padx=10, pady=5)  # Changer la couleur de fond en gris
    navbar.pack(fill='x')

    # Label aligné à gauche
    title_label_nav = tk.Label(navbar, text="Application de Reconnaissance", bg="#808080", fg="white", font=("Helvetica", 12))
    title_label_nav.pack(side='left', padx=10)

    # Cadre pour les boutons
    button_frame = tk.Frame(navbar, bg="#808080")
    button_frame.pack(side='right')

    help_button = tk.Button(button_frame, text="Help", command=show_help, bg="#808080", fg="white", font=("Helvetica", 12), borderwidth=0)
    help_button.pack(side='left', padx=10)
    help_button.bind("<Enter>", lambda e: help_button.config(bg="#6d6d6d"))  # Hover effect
    help_button.bind("<Leave>", lambda e: help_button.config(bg="#808080"))  # Restore original color

    contact_button = tk.Button(button_frame, text="Contact", command=show_contact, bg="#808080", fg="white", font=("Helvetica", 12), borderwidth=0)
    contact_button.pack(side='left', padx=10)
    contact_button.bind("<Enter>", lambda e: contact_button.config(bg="#6d6d6d"))  # Hover effect
    contact_button.bind("<Leave>", lambda e: contact_button.config(bg="#808080"))  # Restore original color

    # Titre de l'interface
    title_label = tk.Label(root, text="Application de Reconnaissance des Plaques", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=20, fill='x')

    # Cadre pour les informations sur la vidéo et les boutons
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(pady=20, padx=20, fill='x')

    # Cadre pour les informations sur la vidéo (tableau)
    info_table_frame = tk.Frame(main_frame)
    info_table_frame.grid(row=0, column=0, padx=10, pady=10)

    # Titre pour les informations
    title_label_info = tk.Label(info_table_frame, text="Informations Vidéo", font=("Helvetica", 10, "bold"), bg="#e3f2fd", fg="#333")
    title_label_info.grid(row=0, column=0, columnspan=2, pady=5)

    # Étiquettes d'information sur la vidéo (tableau avec alternance des couleurs)
    video_name_label = tk.Label(info_table_frame, text="Nom : Aucun", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
    video_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    video_duration_label = tk.Label(info_table_frame, text="Durée : 0 sec", font=("Helvetica", 10), bg="#e3f2fd", fg="#333")
    video_duration_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    # Ligne pour une séparation
    separator_label = tk.Label(info_table_frame, text="", bg="#808080", height=1)
    separator_label.grid(row=3, column=0, columnspan=2, pady=5)

    # Autres informations (ajoutez-en autant que nécessaire)
    # Par exemple : une ligne pour un autre champ
    additional_info_label = tk.Label(info_table_frame, text="Autres Informations", font=("Helvetica", 10), bg="#f0f0f0", fg="#333")
    additional_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

    # Boutons pour charger la vidéo et démarrer la reconnaissance
    load_button = tk.Button(main_frame, text="Charger Vidéo", command=load_video, bg="#4CAF50", fg="white", font=("Helvetica", 12))
    load_button.grid(row=0, column=1, padx=10)

    start_button = tk.Button(main_frame, text="Démarrer la reconnaissance", command=start_recognition, bg="#2196F3", fg="white", font=("Helvetica", 12))
    start_button.grid(row=0, column=2, padx=10)


    # Section pour le traitement de la vidéo (pleine largeur)
    processing_frame = tk.Frame(main_frame, bg="#f0f0f0")  # Cadre de fond clair
    processing_frame.grid(row=1, column=0, padx=10, pady=20, sticky="ew")  # Pleine largeur

    # Titre pour le traitement avec un fond
    title_label_processing = tk.Label(processing_frame, text="Traitement de la Vidéo", font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white")
    title_label_processing.pack(fill='x', pady=5)  # Remplir en largeur
    global processing_text  # Déclarer processing_text comme global

    # Zone de texte pour afficher le processus de traitement
    processing_text = tk.Text(processing_frame, height=5, width=50, font=("Helvetica", 10), bg="white", fg="#333", wrap=tk.WORD)
    processing_text.pack(padx=10, pady=5)

    # Exemple de texte à afficher (peut être remplacé par du texte dynamique)
    processing_text.insert(tk.END, "Le traitement de la vidéo a commencé...\n")


import ast







def display_results(results):
    print("fefbezkbfk",results)

    # Logique pour afficher les résultats dans l'interface
    # Par exemple, vous pouvez afficher les résultats dans une zone de texte ou un label
    processing_text.delete(1.0, tk.END)  # Effacer le texte précédent
    for frame_nmr, cars in results.items():
        processing_text.insert(tk.END, f"Frame {frame_nmr}:\n")
        for car_id, info in cars.items():
            license_text = info['license_plate']['text']
            processing_text.insert(tk.END, f" - Car ID: {car_id}, License: {license_text}\n")

def show_help():
    messagebox.showinfo("Help", "Ceci est l'aide de l'application.")

def show_contact():
    messagebox.showinfo("Contact", "Contactez-nous à : contact@example.com")

def load_video():
    global video_name_label, video_duration_label
    
    video_path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4;*.avi;*.mov")])
    if video_path:
        # Mise à jour du label avec le nom de la vidéo
        video_name = os.path.basename(video_path)
        video_name_label.config(text=f"Nom : {video_name}")

        # Calcul de la durée de la vidéo
        duration = get_video_duration(video_path)
        video_duration_label.config(text=f"Durée : {duration} sec")

        # Ouvrir la vidéo avec cv2.VideoCapture
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            messagebox.showerror("Erreur", "Impossible d'ouvrir la vidéo.")
            return

        try:
            results = detect(cap)  # Récupérer les résultats de la détection
            display_results(results)  # Afficher les résultats dans l'interface
            messagebox.showinfo(results)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la détection : {e}")
        finally:
            # Libérer les ressources
            cap.release()

def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps if fps > 0 else 0
    cap.release()
    return round(duration, 2)



def start_recognition():
    # Ajoutez ici la logique pour la reconnaissance des plaques
    resultaddmissingdata=addmissingdata()
    messagebox.showinfo("Information", "Processus de reconnaissance démarré!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reconnaissance des Plaques d'Immatriculation")
    root.geometry("800x600")
    root.config(bg="#f0f0f0")  # Couleur de fond de la fenêtre principale

    # Appel à la fonction pour créer l'interface
    creer_interface2(root)

    root.mainloop()
