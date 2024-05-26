import tkinter as tk
from tkinter import messagebox, ttk
import pygame
import os
import sys
from ttkthemes import ThemedStyle
import requests
import tempfile
import zipfile

# Inicializar Pygame Mixer
pygame.mixer.init()

def play_background_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)

def stop_background_sound():
    pygame.mixer.music.stop()

def play_sound_effect(file_path):
    effect = pygame.mixer.Sound(file_path)
    effect.play()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ManifestCreator:
    def __init__(self, window):
        self.window = window
        self.language = "Español"
        self.languages = {'Español': 'Spanish', 'English': 'English'}
        self.current_theme = "clam"
        self.question_index = 0
        self.questions = {
            "Español": [
                ("Nuevo appid:", "app_id"),
                ("Nuevo nombre:", "name"),
                ("Nuevo buildid:", "build_id")
            ],
            "English": [
                ("New appid:", "app_id"),
                ("New name:", "name"),
                ("New buildid:", "build_id")
            ]
        }
        self.answers = {}
        self.github_link = "https://github.com/aybar1234/App-para-crear-manifiestos-steam.git"

        self.create_content()
        self.create_menu()

    def create_content(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        question_text, question_key = self.questions[self.language][self.question_index]
        tk.Label(self.window, text=question_text).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.entry = ttk.Entry(self.window)
        self.entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        self.entry.focus_set()

        ttk.Button(self.window, text="Siguiente" if self.language == "Español" else "Next", command=self.next_question).place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        update_button = ttk.Button(self.window, text="Buscar actualizaciones", command=self.check_updates)
        update_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def next_question(self):
        answer = self.entry.get()

        question_key = self.questions[self.language][self.question_index][1]
        self.answers[question_key] = answer

        self.question_index += 1

        if self.question_index < len(self.questions[self.language]):
            self.create_content()
        else:
            self.create_manifest()

    def create_manifest(self):
        appid = self.answers.get("app_id", "")
        name = self.answers.get("name", "")
        buildid = self.answers.get("build_id", "")

        try:
            with open(f"appmanifest_{appid}.acf", "w") as f:
                f.write(f'"AppState"\n{{\n')
                f.write(f'    "appid"         "{appid}"\n')
                f.write(f'    "Universe"      "1"\n')
                f.write(f'    "LauncherPath"  "C:\\Program Files (x86)\\Steam\\steam.exe"\n')
                f.write(f'    "name"          "{name}"\n')
                f.write(f'    "StateFlags"    "1026"\n')
                f.write(f'    "installdir"    "{name}"\n')
                f.write(f'    "LastUpdated"   "0"\n')
                f.write(f'    "LastPlayed"    "0"\n')
                f.write(f'    "SizeOnDisk"    "0"\n')
                f.write(f'    "StagingSize"   "37347304023"\n')
                f.write(f'    "buildid"       "{buildid}"\n')
                f.write(f'    "LastOwner"     "76561198196538353"\n')
                f.write(f'    "UpdateResult"  "0"\n')
                f.write(f'    "BytesToDownload"       "30602716768"\n')
                f.write(f'    "BytesDownloaded"       "3006224384"\n')
                f.write(f'    "BytesToStage"  "37351956959"\n')
                f.write(f'    "BytesStaged"   "3913819811"\n')
                f.write(f'    "TargetBuildID" "14470938"\n')
                f.write(f'    "AutoUpdateBehavior"    "0"\n')
                f.write(f'    "AllowOtherDownloadsWhileRunning"       "0"\n')
                f.write(f'    "ScheduledAutoUpdate"   "0"\n')
                f.write(f'    "InstalledDepots"\n    {{\n    }}\n')
                f.write(f'    "SharedDepots"\n    {{\n        "228988"        "228980"\n        "228990"        "228980"\n    }}\n')
                f.write(f'    "StagedDepots"\n    {{\n        "2347770"\n        {{\n            "manifest"          "8655589593738752418"\n            "size"              "35628026451"\n            "dlcappid"          "0"\n        }}\n    }}\n')
                f.write(f'    "UserConfig"\n    {{\n        "language"      "{self.languages[self.language]}"\n    }}\n')
                f.write(f'    "MountedConfig"\n    {{\n    }}\n')
                f.write(f'}}\n')
            play_sound_effect(resource_path('sounds/success.wav'))
            messagebox.showinfo("Success" if self.language == "English" else "Éxito", "Manifest file created successfully." if self.language == "English" else "Archivo de manifiesto creado con éxito.")
            messagebox.showinfo("Gracias" if self.language == "Español" else "Thanks", "¡Gracias por usar mi programa!" if self.language == "Español" else "Thanks for using my program!")
        except Exception as e:
            play_sound_effect(resource_path('sounds/error.wav'))
            messagebox.showerror("Error", f"Error creating manifest file: {e}")

    def create_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language" if self.language == "English" else "Idioma", menu=language_menu)

        for lang in self.languages.keys():
            language_menu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
            
    def change_language(self, lang):
        self.language = lang
        self.create_content()
        
    def check_updates(self):
        github_repo = "https://github.com/aybar1234/App-para-crear-manifiestos-steam/archive/refs/heads/main.zip"
        try:
            response = requests.get(github_repo, stream=True)
            if response.status_code == 200:
                tmp_dir = tempfile.mkdtemp()
                zip_path = os.path.join(tmp_dir, "repo.zip")
                with open(zip_path, "wb") as f:
                    f.write(response.content)

                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(tmp_dir)

                messagebox.showinfo("Actualización exitosa", "El código fuente se ha descargado correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo descargar el código fuente. Código de error: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar el código fuente: {e}")

def start_application():
    window = tk.Tk()
    window.title("Create Manifest")
    window.geometry("600x400")
    window.resizable(False, False)

    play_background_sound(resource_path('sounds/736586__josefpres__piano-loops-156-efect-octave-long-loop-120-bpm.wav'))
    ManifestCreator(window)

    style = ThemedStyle(window)
    style.set_theme("clam")

    window.mainloop()

if __name__ == "__main__":
    start_application()