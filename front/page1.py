import tkinter as tk
from tkinter import ttk
import page2  # Importer la deuxième page

def creer_interface1(root):
    root.title("Application d'Intelligence Artificielle")
        # Dimensions de la fenêtre
    window_width = 900
    window_height = 600
    
    # Obtenir les dimensions de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculer la position x, y pour centrer la fenêtre
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Définir la taille et la position de la fenêtre
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Cadre principal
    cadre_principal = tk.Frame(root, bg="#333333")  # Fond gris foncé
    cadre_principal.pack(expand=True, fill='both')

    # Titre de l'application
    titre = tk.Label(cadre_principal, text="Bienvenue dans notre Application d'IA", font=("Helvetica", 24, "bold"), bg="#333333", fg="white")
    titre.pack(pady=20)

    # Image au-dessus du bouton Start
    logo_image = tk.PhotoImage(file="front\\assets\\vector2.png")  # Remplacez "logo.png" par le nom de votre image
    logo_label = tk.Label(cadre_principal, image=logo_image, bg="#333333")
    logo_label.pack(pady=10)

    # Description
    description = tk.Label(cadre_principal, text="Cliquez sur 'Start' .", font=("Helvetica", 16), bg="#333333", fg="white")
    description.pack(pady=10)

    # Barre de progression (initialement cachée)
    progress_bar = ttk.Progressbar(cadre_principal, orient="horizontal", length=500, mode="determinate")
    
    # Fonction pour démarrer la progression
    def demarrer_progression():
        bouton_start.config(state='disabled')  # Désactiver le bouton "Start" après clic
        progress_bar.pack(pady=20)  # Afficher la barre de progression
        progress_value = 0
        max_value = 100
        step = 5  # Vitesse de progression

        # Fonction interne pour mettre à jour la progression
        def mise_a_jour():
            nonlocal progress_value
            if progress_value < max_value:
                progress_value += step
                progress_bar['value'] = progress_value
                root.after(200, mise_a_jour)  # Appel récursif après 200 ms
            else:
                # Une fois la progression terminée, passer à la page 2
                page2.creer_interface2(root)

        mise_a_jour()

    # Bouton Start pour démarrer la progression
    bouton_start = tk.Button(cadre_principal, text="Start", command=demarrer_progression, font=("Helvetica", 16), bg="#4CAF50", fg="white", relief=tk.RAISED)
    bouton_start.pack(pady=20)

    # Centrer tous les éléments dans le cadre
    for widget in cadre_principal.winfo_children():
        widget.pack(pady=10, padx=20)  # Espace autour des widgets

    # Boucle principale
    root.mainloop()
