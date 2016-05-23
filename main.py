import serial
import sqlite3

if __name__ == "__main__":
    # Database name
    connection = "data.db"

    try:
        # Initialise the connection of data.db
        conn = sqlite3.connect(connection)

        port = "COM6"
        baudrate = 9600

        try:
            # On ouvre la connexion série
            ser = serial.Serial(port, baudrate=baudrate, timeout=1)

            # On boucle indéfiniment sur la lecture du port série
            while True:
                line = ser.readline()  # On lit une ligne entière (retourne un tableau d'octets)
                line = line.decode("utf-8")  # On la convertit en chaîne de caractère
                line = line.strip()  # Supprime le retour à la ligne à la fin

                # Si la ligne est vide, c'est que le correspondant n'a rien envoyé à la fin du timeout
                if len(line) <= 0:
                    continue  # On retourne au début

                # Si la ligne commence par un dièse, c'est que c'est un commentaire
                if line[0] == "#":
                    print("Commentaire : {}".format(line[1:]))  # on se contente de l'afficher
                # Sinon, c'est une carte
                else:
                    if len(line) == 8:
                        # print("Carte détéctée : {}".format(line))

                        # Initialize the request object
                        cursor = conn.cursor()

                        # Check if the db is empty
                        if cursor.execute("""
                                        SELECT * FROM data
                                  """).rowcount is not None:
                            # Select and print requested data

                            result = cursor.execute("""
                                  SELECT detail FROM data WHERE nuID = ?
                            """, [line]).fetchone()[0]

                            print("Carte détectée : " + result)

                            ser.write(str.encode(result))
                    else:
                        print("Avertissement : L'identifiant de la carte est incorrect ({})".format(line))
            ser.close()
        except serial.SerialException as ex:
            print("Erreur : {}".format(ex))
        except KeyboardInterrupt:
            # Si on fait Ctrl+C, pour quitter
            ser.close()
    # Error related to the database
    except sqlite3.Error as e:
        print("An error occurred:", e)
    finally:
        # Closure of the connexion
        conn.close()
