import sqlite3

def buat_tabel():
    koneksi = sqlite3.connect('hasil_tes.db')
    cursor = koneksi.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hasil (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            usia INTEGER,
            jawaban TEXT
        )
    ''')
    koneksi.commit()
    koneksi.close()

def simpan_data(nama, usia, jawaban):
    koneksi = sqlite3.connect('hasil_tes.db')
    cursor = koneksi.cursor()
    cursor.execute("INSERT INTO hasil (nama, usia, jawaban) VALUES (?, ?, ?)", (nama, usia, jawaban))
    koneksi.commit()
    koneksi.close()

def ambil_semua_data():
    koneksi = sqlite3.connect('hasil_tes.db')
    cursor = koneksi.cursor()
    cursor.execute("SELECT * FROM hasil")
    data = cursor.fetchall()
    koneksi.close()
    return data
