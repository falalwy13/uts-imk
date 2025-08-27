import streamlit as st
import pandas as pd
from database import buat_tabel, simpan_data, ambil_semua_data
import json

buat_tabel()

try:
    data_pertanyaan = pd.read_csv("pertanyaan_16pf_lengkap.csv")
    if 'faktor' not in data_pertanyaan.columns or 'arah_skor' not in data_pertanyaan.columns:
        st.error("File 'pertanyaan_16pf_lengkap.csv' harus memiliki kolom 'faktor' dan 'arah_skor' untuk skoring dan uraian. Mohon periksa dan perbarui file Anda.")
        st.stop()
except FileNotFoundError:
    st.error("File 'pertanyaan_16pf_lengkap.csv' tidak ditemukan. Pastikan file berada di direktori yang sama dengan 'app.py'.")
    st.stop()
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca CSV: {e}")
    st.stop()

opsi_jawaban = ['a. Ya', 'b. Kadang-kadang', 'c. Tidak']

deskripsi_faktor = {
    'A': {
        'low': "A- : Pribadi yang menyendiri, kaku, kritis, dingin.",
        'high': "A+ : Pribadi yang ramah, hangat, mudah bergaul, perhatian."
    },
    'B': {
        'low': "B- : Kurang cerdas, berpikir konkrit, belajar lambat.",
        'high': "B+ : Cerdas, berpikir abstrak, cepat belajar."
    },
    'C': {
        'low': "C- : Cenderung emosional, mudah terganggu, kurang matang.",
        'high': "C+ : Stabil secara emosi, tenang, matang, realistis."
    },
    'E': {
        'low': "E- : Patuh, rendah hati, akomodatif, mudah dikendalikan.",
        'high': "E+ : Dominan, asertif, keras kepala, kompetitif."
    },
    'F': {
        'low': "F- : Serius, pendiam, berhati-hati, pesimis.",
        'high': "F+ : Gembira, antusias, spontan, ceria."
    },
    'G': {
        'low': "G- : Tidak patuh aturan, suka berubah, oportunistik.",
        'high': "G+ : Penuh kesadaran aturan, teliti, bertanggung jawab."
    },
    'H': {
        'low': "H- : Pemalu, hati-hati, mudah terancam, sensitif.",
        'high': "H+ : Berani secara sosial, suka bertualang, tebal muka."
    },
    'I': {
        'low': "I- : Keras, realistik, mandiri, kurang peka.",
        'high': "I+ : Sensitif, artistik, imajinatif, lembut hati."
    },
    'L': {
        'low': "L- : Percaya, mudah menerima, tidak curiga.",
        'high': "L+ : Curiga, skeptis, sulit mempercayai orang lain."
    },
    'M': {
        'low': "M- : Praktis, berorientasi realitas, konvensional.",
        'high': "M+ : Imajinatif, abstrak, berorientasi ide, kurang praktis."
    },
    'N': {
        'low': "N- : Terus terang, polos, apa adanya.",
        'high': "N+ : Cerdik, taktis, hati-hati, pandai menahan diri."
    },
    'O': {
        'low': "O- : Percaya diri, puas diri, tenang.",
        'high': "O+ : Cemas, khawatir, mudah menyalahkan diri sendiri."
    },
    'Q1': {
        'low': "Q1- : Konservatif, tradisional, menerima yang sudah ada.",
        'high': "Q1+ : Eksperimental, liberal, terbuka terhadap perubahan."
    },
    'Q2': {
        'low': "Q2- : Bergantung pada kelompok, mengikuti, suka berkelompok.",
        'high': "Q2+ : Mandiri, mandiri, tidak suka bergantung."
    },
    'Q3': {
        'low': "Q3- : Tidak disiplin, ceroboh, konflik internal.",
        'high': "Q3+ : Terkendali, disiplin, perfeksionis, teliti."
    },
    'Q4': {
        'low': "Q4- : Tenang, santai, sabar, tidak frustasi.",
        'high': "Q4+ : Tegang, gelisah, frustasi, tidak sabar."
    }
}

st.title("Tes Kepribadian 16 PF (Skoring & Kesimpulan Sederhana)")
st.warning("PERHATIAN: Skoring dan uraian ini **BUKAN** skoring resmi atau valid secara psikologis untuk tes 16 PF. Ini hanyalah demonstrasi fungsionalitas teknis dan interpretasi berdasarkan asumsi yang sangat disederhanakan.")

st.subheader("Silakan Isi Identitas Anda")
nama_pengguna = st.text_input("Nama Lengkap", key="nama_input")
usia_pengguna = st.number_input("Usia", min_value=10, max_value=100, step=1, key="usia_input")

def hitung_skor_16pf(daftar_jawaban_bersih, data_pertanyaan_df):
    skor_faktor = {
        'A': 0, 'B': 0, 'C': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0,
        'L': 0, 'M': 0, 'N': 0, 'O': 0, 'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0
    }
    
    jumlah_pertanyaan_per_faktor = data_pertanyaan_df['faktor'].value_counts().to_dict()

    nilai_jawaban = {'a': 2, 'b': 1, 'c': 0}

    if len(daftar_jawaban_bersih) != len(data_pertanyaan_df):
        st.error(f"Kesalahan skoring: Jumlah jawaban ({len(daftar_jawaban_bersih)}) tidak sesuai dengan jumlah pertanyaan ({len(data_pertanyaan_df)}).")
        return None, None 

    for idx, jawaban_user in enumerate(daftar_jawaban_bersih):
        pertanyaan_info = data_pertanyaan_df.iloc[idx]
        faktor = pertanyaan_info.get('faktor')
        arah_skor = pertanyaan_info.get('arah_skor')

        if faktor not in skor_faktor or arah_skor not in ['positif', 'negatif']:
            continue 

        skor_item = nilai_jawaban.get(jawaban_user)
        if skor_item is None:
            continue

        if arah_skor == 'negatif':
            skor_item = 2 - skor_item
        
        skor_faktor[faktor] += skor_item

    ambang_batas_per_faktor = {}
    for faktor, jumlah_q in jumlah_pertanyaan_per_faktor.items():
        if faktor in skor_faktor:
            max_skor_faktor = jumlah_q * 2 
            ambang_batas_per_faktor[faktor] = {
                'low_max': int(max_skor_faktor / 3),
                'high_min': int(max_skor_faktor * 2 / 3) + 1 
            }
            if ambang_batas_per_faktor[faktor]['low_max'] >= ambang_batas_per_faktor[faktor]['high_min']:
                ambang_batas_per_faktor[faktor]['high_min'] = ambang_batas_per_faktor[faktor]['low_max'] + 1

    return skor_faktor, ambang_batas_per_faktor

PERTANYAAN_PER_HALAMAN = 10 
total_pertanyaan = len(data_pertanyaan)
total_halaman = (total_pertanyaan + PERTANYAAN_PER_HALAMAN - 1) // PERTANYAAN_PER_HALAMAN

if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = [''] * total_pertanyaan 

def go_to_page(page_num):
    st.session_state.current_page = page_num

if nama_pengguna and usia_pengguna:
    st.subheader("Jawab Semua Pertanyaan:")

    start_idx = st.session_state.current_page * PERTANYAAN_PER_HALAMAN
    end_idx = min(start_idx + PERTANYAAN_PER_HALAMAN, total_pertanyaan)
    
    pertanyaan_di_halaman_ini = data_pertanyaan.iloc[start_idx:end_idx]

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_page > 0:
            st.button("Halaman Sebelumnya", on_click=go_to_page, args=(st.session_state.current_page - 1,), key="prev_page_top")
    with col2:
        st.markdown(f"<h5 style='text-align: center;'>Halaman {st.session_state.current_page + 1} dari {total_halaman}</h5>", unsafe_allow_html=True)
    with col3:
        if st.session_state.current_page < total_halaman - 1:
            st.button("Halaman Selanjutnya", on_click=go_to_page, args=(st.session_state.current_page + 1,), key="next_page_top")

    st.markdown("---")

    for i, baris in pertanyaan_di_halaman_ini.iterrows():
        nomor_soal = i + 1
        current_answer = st.session_state.answers[i] if st.session_state.answers[i] else '' 

        st.markdown(f"**{nomor_soal}.** {baris['pertanyaan']}")
        
        default_index = opsi_jawaban.index(current_answer) if current_answer in opsi_jawaban else 0 
        
        selected_option = st.radio(
            "", 
            opsi_jawaban,
            index=default_index,
            key=f"q_{baris['id']}_{st.session_state.current_page}" 
        )
        st.session_state.answers[i] = selected_option 

    st.markdown("---")
    
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b1:
        if st.session_state.current_page > 0:
            st.button("Halaman Sebelumnya", on_click=go_to_page, args=(st.session_state.current_page - 1,), key="prev_page_bottom")
    with col_b2:
        st.markdown(f"<h5 style='text-align: center;'>Halaman {st.session_state.current_page + 1} dari {total_halaman}</h5>", unsafe_allow_html=True)
    with col_b3:
        if st.session_state.current_page < total_halaman - 1:
            st.button("Halaman Selanjutnya", on_click=go_to_page, args=(st.session_state.current_page + 1,), key="next_page_bottom")

    if st.session_state.current_page == total_halaman - 1:
        if st.button("Kirim Jawaban dan Lihat Hasil"):
            jawaban_bersih = [jwb.split('.')[0] for jwb in st.session_state.answers if jwb] 

            if len(jawaban_bersih) != total_pertanyaan:
                st.error(f"Harap lengkapi semua {total_pertanyaan} pertanyaan sebelum mengirim. Anda baru menjawab {len(jawaban_bersih)}.")
            else:
                simpan_data(nama_pengguna, usia_pengguna, json.dumps(jawaban_bersih))
                st.success("Jawaban berhasil disimpan!")

                st.subheader("Tabel Skor (Sederhana) Kepribadian 16 PF Anda:")
                skor_akhir, ambang_batas = hitung_skor_16pf(jawaban_bersih, data_pertanyaan)
                
                if skor_akhir and ambang_batas:
                    df_skor = pd.DataFrame(list(skor_akhir.items()), columns=['Faktor', 'Skor'])
                    st.dataframe(df_skor.set_index('Faktor'))
                    
                    st.markdown("---") 
                    st.subheader("Kesimpulan Uraian Hasil:")
                    
                    faktor_tinggi = []
                    faktor_rendah = []

                    for faktor, skor in skor_akhir.items():
                        if faktor in deskripsi_faktor and faktor in ambang_batas:
                            low_max = ambang_batas[faktor]['low_max']
                            high_min = ambang_batas[faktor]['high_min']
                            
                            if skor <= low_max:
                                faktor_rendah.append(faktor)
                            elif skor >= high_min:
                                faktor_tinggi.append(faktor)
                    
                    kesimpulan_str = f"Berdasarkan jawaban Anda, berikut adalah gambaran singkat profil kepribadian **{nama_pengguna}** (Usia: {usia_pengguna} tahun):\n\n"
                    
                    if faktor_tinggi:
                        kesimpulan_str += "**Kecenderungan Menonjol (Skor Tinggi):**\n"
                        for f in faktor_tinggi:
                            kesimpulan_str += f"- Pada faktor **{f}**, Anda cenderung bersifat {deskripsi_faktor[f]['high'].split(':')[1].strip()}.\n"
                    else:
                        kesimpulan_str += "- Tidak ada kecenderungan yang secara signifikan 'tinggi' pada faktor-faktor utama yang diukur.\n"

                    if faktor_rendah:
                        kesimpulan_str += "\n**Kecenderungan yang Mungkin Perlu Perhatian (Skor Rendah):**\n"
                        for f in faktor_rendah:
                            kesimpulan_str += f"- Pada faktor **{f}**, Anda cenderung bersifat {deskripsi_faktor[f]['low'].split(':')[1].strip()}.\n"
                    else:
                        kesimpulan_str += "- Tidak ada kecenderungan yang secara signifikan 'rendah' pada faktor-faktor utama yang diukur.\n"
                    
                    if not faktor_tinggi and not faktor_rendah:
                        kesimpulan_str += "Secara keseluruhan, Anda menunjukkan kecenderungan sedang pada sebagian besar faktor yang diukur, yang menunjukkan profil kepribadian yang seimbang dan adaptif.\n"

                    kesimpulan_str += "\n*Penting diingat bahwa kesimpulan ini bersifat umum dan didasarkan pada asumsi sederhana. Untuk analisis yang mendalam dan akurat, diperlukan interpretasi oleh psikolog profesional.*"
                    
                    st.markdown(kesimpulan_str)
                    
                    st.info("Catatan Penting: Interpretasi skor ini membutuhkan standar normatif dan keahlian psikologi. Skor ini hanyalah total poin berdasarkan asumsi sederhana.")
                else:
                    st.error("Gagal menghitung skor atau ambang batas. Mohon periksa konsistensi data.")


st.subheader("📊 Data Hasil Tes")
if st.checkbox("Tampilkan Semua Hasil yang Tersimpan"):
    semua_data = ambil_semua_data()
    if semua_data:
        df_hasil = pd.DataFrame(semua_data, columns=['ID', 'Nama', 'Usia', 'Jawaban'])
        st.dataframe(df_hasil)

        st.subheader("Hitung Ulang Skor dan Kesimpulan dari Data Tersimpan")
        if not df_hasil.empty:
            selected_id = st.selectbox("Pilih ID Hasil untuk Menghitung Skor Ulang:", df_hasil['ID'].tolist(), key='select_id_recalc')
            
            if st.button("Hitung Skor Ulang dan Kesimpulan dari DB"):
                data_terpilih = df_hasil[df_hasil['ID'] == selected_id].iloc[0]
                
                try:
                    jawaban_dari_db = json.loads(data_terpilih['Jawaban'].replace("'", "\""))
                    
                    st.write(f"Menghitung skor ulang dan kesimpulan untuk {data_terpilih['Nama']} (ID: {data_terpilih['ID']})...")
                    skor_ulang, ambang_batas_ulang = hitung_skor_16pf(jawaban_dari_db, data_pertanyaan)
                    
                    if skor_ulang and ambang_batas_ulang:
                        df_skor_ulang = pd.DataFrame(list(skor_ulang.items()), columns=['Faktor', 'Skor'])
                        st.dataframe(df_skor_ulang.set_index('Faktor'))

                        st.markdown("---")
                        st.subheader("Kesimpulan Uraian Hasil (Dihitung Ulang):")
                        
                        faktor_tinggi_ulang = []
                        faktor_rendah_ulang = []

                        for faktor, skor in skor_ulang.items():
                            if faktor in deskripsi_faktor and faktor in ambang_batas_ulang:
                                low_max = ambang_batas_ulang[faktor]['low_max']
                                high_min = ambang_batas_ulang[faktor]['high_min']
                                
                                if skor <= low_max:
                                    faktor_rendah_ulang.append(faktor)
                                elif skor >= high_min:
                                    faktor_tinggi_ulang.append(faktor)

                        kesimpulan_ulang_str = f"Berdasarkan jawaban Anda, berikut adalah gambaran singkat profil kepribadian **{data_terpilih['Nama']}** (Usia: {data_terpilih['Usia']} tahun):\n\n"
                        
                        if faktor_tinggi_ulang:
                            kesimpulan_ulang_str += "**Kecenderungan Menonjol (Skor Tinggi):**\n"
                            for f in faktor_tinggi_ulang:
                                kesimpulan_ulang_str += f"- Pada faktor **{f}**, Anda cenderung bersifat {deskripsi_faktor[f]['high'].split(':')[1].strip()}.\n"
                        else:
                            kesimpulan_ulang_str += "- Tidak ada kecenderungan yang secara signifikan 'tinggi' pada faktor-faktor utama yang diukur.\n"

                        if faktor_rendah_ulang:
                            kesimpulan_ulang_str += "\n**Kecenderungan yang Mungkin Perlu Perhatian (Skor Rendah):**\n"
                            for f in faktor_rendah_ulang:
                                kesimpulan_ulang_str += f"- Pada faktor **{f}**, Anda cenderung bersifat {deskripsi_faktor[f]['low'].split(':')[1].strip()}.\n"
                        else:
                            kesimpulan_ulang_str += "- Tidak ada kecenderungan yang secara signifikan 'rendah' pada faktor-faktor utama yang diukur.\n"

                        if not faktor_tinggi_ulang and not faktor_rendah_ulang:
                            kesimpulan_ulang_str += "Secara keseluruhan, Anda menunjukkan kecenderungan sedang pada sebagian besar faktor yang diukur, yang menunjukkan profil kepribadian yang seimbang dan adaptif.\n"

                        kesimpulan_ulang_str += "\n*Penting diingat bahwa kesimpulan ini bersifat umum dan didasarkan pada asumsi sederhana. Untuk analisis yang mendalam dan akurat, diperlukan interpretasi oleh psikolog profesional.*"
                        
                        st.markdown(kesimpulan_ulang_str)
                        st.info("Skor dan uraian ini dihitung ulang dari data yang tersimpan.")
                    else:
                        st.error("Gagal menghitung skor ulang atau ambang batas. Periksa log atau format jawaban di DB.")
                except json.JSONDecodeError as e:
                    st.error(f"Gagal mengurai jawaban dari database (ID: {selected_id}): {e}. Pastikan format jawaban benar di database.")
        else:
            st.info("Tidak ada data untuk dihitung ulang skornya.")
    else:
        st.info("Belum ada data hasil tes yang tersimpan.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Dibuat oleh Muhammad Naufal Alwy</p>", unsafe_allow_html=True)
