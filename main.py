import serial
import sqlite3
from threading import Thread
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="Tentative de connexion au lecteur...", justify=tk.LEFT)
        self.label.pack()

        self.map_image = tk.PhotoImage(file="plan_exia.png")
        self.canvas = tk.Canvas(self, width=476, height=540)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)
        self.canvas.pack()

        self._stop = False
        self._thread = Thread(target=self.listen_serial)
        self._thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self._stop = True
        tk.Tk.destroy(self)

    def listen_serial(self):
        # Database name
        connection = "data.db"

        try:
            # Initialise the connection of data.db
            conn = sqlite3.connect(connection)

            port = "COM3"
            baudrate = 9600

            try:
                # On ouvre la connexion série
                ser = serial.Serial(port, baudrate=baudrate, timeout=1)

                # On boucle indéfiniment sur la lecture du port série
                while not self._stop:
                    line = ser.readline()  # On lit une ligne entière (retourne un tableau d'octets)
                    line = line.decode("utf-8")  # On la convertit en chaîne de caractère
                    line = line.strip()  # Supprime le retour à la ligne à la fin

                    # Si la ligne est vide, c'est que le correspondant n'a rien envoyé à la fin du timeout
                    if len(line) <= 0:
                        continue  # On retourne au début

                    # Si la ligne commence par un dièse, c'est que c'est un commentaire
                    if line[0] == "#":
                        print("Commentaire : {}".format(line[1:].strip()))  # on se contente de l'afficher
                        self.label["text"] = "{}".format(line[1:].strip())
                    # Sinon, c'est une carte
                    else:
                        if len(line) == 8:
                            cursor = conn.cursor()
                            result = cursor.execute("SELECT room_name, x, y FROM Tags WHERE nuid = ?;", [line]).fetchone()

                            if result:
                                room_name = result[0]
                                posx = result[1]
                                posy = result[2]
                                filename = tk.PhotoImage(file="map_marker.gif")
                                image = self.canvas.create_image(posx, posy, anchor=tk.S, image=filename)
                                self.label["text"] = "Marqueur détecté ({}) : {}".format(line, room_name)
                                print("Marqueur détectée ({}) : {}".format(line, room_name))
                                ser.write(str.encode(room_name))
                            else:
                                self.label["text"] = "Marqueur détectée ({}) : Ce marqueur n'est pas enregistré dans la base.".format(line)
                                print("Marqueur détectée ({}) : Ce marqueur n'est pas enregistré dans la base.".format(line))
                                ser.write(b"<Not in db>")
                        else:
                            print("Avertissement : L'identifiant de du marqueur est incorrect ({})".format(line))
                ser.close()
            except serial.SerialException as ex:
                self.label["text"] = "Erreur (serial) : {}".format(ex)
                print("Erreur (serial) : {}".format(ex))
        # Error related to the database
        except sqlite3.Error as ex:
            self.label["text"] = "Erreur (sqlite) : {}".format(ex)
            print("Erreur (sqlite) : {}".format(ex))
        finally:
            # Closure of the connexion
            conn.close()


if __name__ == "__main__":
    App().mainloop()
