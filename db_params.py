import sqlite3

connection = "data.db"

try:
    conn = sqlite3.connect(connection)

    cursor = conn.cursor()

    # create table
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS Tags(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    nuid VARCHAR(8) UNIQUE,
                    room_name VARCHAR(255),
                    x REAL,
                    y REAL
                );
            """)

    # insert data
    cursor.execute("""
                INSERT INTO Tags(nuid, room_name, x, y)
                VALUES ("4408FC93", "Salle C26", 282, 282),
                       ("A6D2EF13", "Local du BDE", 608, 453),
                       ("4A5A2AE2", "Salle C28", 241, 754);
            """)

    conn.commit()
except sqlite3.Error as ex:
    print("Erreur : {}".format(ex))
finally:
    conn.close()
