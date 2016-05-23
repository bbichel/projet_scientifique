import sqlite3

connection = "data.db"

try:
    conn = sqlite3.connect(connection)

    cursor = conn.cursor()

    # create table
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS data(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    NUID VARCHAR(8) UNIQUE,
                    detail VARCHAR(255)
                );
            """)

    # insert data
    cursor.execute("""
                INSERT INTO data(nuID, detail) VALUES ("4408FC93", "Production"),
                                                ("A6D2EF13", "Bureau CS32"),
                                                ("4A5A2AE2", "Assemblage");
            """)

    conn.commit()
except sqlite3.Error as ex:
    print("Erreur : {}".format(ex))
finally:
    conn.close()
