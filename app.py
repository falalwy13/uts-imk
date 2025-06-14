import streamlit as st
import pandas as pd
from database import buat_tabel, simpan_data, ambil_semua_data

buat_tabel()

data_pertanyaan = pd.read_csv("pertanyaan_16pf_lengkap.csv")
opsi_jawaban = ['a. Ya', 'b. Kadang-kadang', 'c. Tidak']

st.title("Tes Kepribadian 16 PF")

st.subheader("Silakan Isi Identitas Anda")
nama_pengguna = st.text_input("Nama Lengkap")
usia_pengguna = st.number_input("Usia", min_value=10, max_value=100, step=1)

if nama_pengguna and usia_pengguna:
    st.subheader("Jawab Semua Pertanyaan:")
    daftar_jawaban = []
    for _, baris in data_pertanyaan.iterrows():
        pilihan = st.radio(baris['pertanyaan'], opsi_jawaban, key=str(baris['id']))
        daftar_jawaban.append(pilihan)

    if st.button("Kirim Jawaban"):
        jawaban_bersih = [jwb.split('.')[0] for jwb in daftar_jawaban]
        simpan_data(nama_pengguna, usia_pengguna, str(jawaban_bersih))
        st.success("Jawaban berhasil disimpan!")

st.subheader("📊 Data Hasil Tes")
if st.checkbox("Tampilkan Semua Hasil"):
    semua_data = ambil_semua_data()
    data_tabel = pd.DataFrame(semua_data, columns=["ID", "Nama", "Usia", "Jawaban"])
    st.dataframe(data_tabel)
