import sqlite3

connection = "data.db"

try:
    conn = sqlite3.connect(connection)

    cursor = conn.cursor()

    # create table
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS data(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    nuID VARCHAR(8),
                    detail VARCHAR(255)
                )
            """)

    # insert data
    cursor.execute("""
                INSERT INTO data(nuID, detail) VALUES ("4408FC93", "C25"),
                                                ("A6D2EF13", "C23"),
                                                ("4A5A2AE2", "C20")
            """)

    conn.commit()
except sqlite3.Error as e:
    print
    "An error occurred:", e.args[0]
finally:
    conn.close()