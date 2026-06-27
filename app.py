from flask import Flask, render_template, request, send_file
import os
import matplotlib
matplotlib.use('Agg') # Mengizinkan matplotlib membuat grafik di background server web
import matplotlib.pyplot as plt

# Import class yang sudah kita buat di file bioinformatics.py
from bioinformatics import SequenceParser, SequenceAnalyzer

app = Flask(__name__)

# Fungsi penentu kunci pengurutan (untuk mengurutkan list berdasarkan nilai GC)
def ambil_nilai_gc(item):
    return item["gc_content"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. Menangkap DAFTAR file yang di-upload (menggunakan getlist agar bisa membaca banyak file)
        files_input = request.files.getlist('file_kamu')
        file_type = request.form['file_type']
        
        raw_data = [] # List induk untuk menampung seluruh sekuens dari semua file
        
        for file_input in files_input:
            if file_input.filename != '':
                # Simpan file secara lokal di folder static sementara waktu
                filepath = os.path.join("static", file_input.filename)
                file_input.save(filepath)
                
                # 2. Panggil Parser untuk membaca sekuens dari file tersebut
                parser_obj = SequenceParser(filepath)
                if file_type == "FASTA":
                    file_data = parser_obj.parse_fasta()
                else:
                    file_data = parser_obj.parse_fastq()
                
                # Masukkan hasil parser file ini ke list induk
                raw_data.extend(file_data)
                
                # Hapus file mentah temporary hasil unggahan tadi agar direktori tetap bersih
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
        if len(raw_data) > 0:
            # 3. Analisis Pipeline (Hitung Frekuensi & GC Content)
            analyzer_obj = SequenceAnalyzer()
            hasil_pipeline = []
            
            for item in raw_data:
                seq = item["sequence"]
                gc = analyzer_obj.calculate_gc_content(seq)
                freq = analyzer_obj.count_nucleotides(seq)
                
                # Bungkus hasil ke dalam struktur dictionary baru
                info = {
                    "header": item["header"],
                    "sequence": seq,
                    "gc_content": gc,
                    "counts": freq
                }
                hasil_pipeline.append(info)
            
            # 4. Mengurutkan sekuens berdasarkan GC Content (Descending: Terbesar ke Terkecil)
            hasil_pipeline.sort(key=ambil_nilai_gc, reverse=True)
            
            # 5. Mengambil 3 Sekuens Terbaik (Top 3) menggunakan slicing list [0:3]
            top_3 = hasil_pipeline[0:3]
            
            # 6. Pembuatan Visualisasi Grafik Batang (Matplotlib) dengan warna Gram-Negatif Pink
            list_header = []
            list_gc = []
            for res in hasil_pipeline:
                # Potong nama header agar tidak terlalu panjang menumpuk di grafik
                list_header.append(res["header"][:12] + "...") 
                list_gc.append(res["gc_content"])
                
            plt.figure(figsize=(9, 4.5))
            # Diubah warnanya menjadi pink pastel (#ffb7c5) dan garis tepi merah tua (#6b3b43)
            plt.bar(list_header, list_gc, color='#ffb7c5', edgecolor='#6b3b43', linewidth=1)
            plt.ylabel('GC Content (%)')
            plt.xlabel('ID / Header Sekuens')
            plt.title('Visualisasi Nilai GC Content per Sekuens')
            plt.xticks(rotation=30, ha='right')
            plt.tight_layout()
            
            # Simpan gambar grafik ke folder static
            chart_path = os.path.join("static", "gc_chart.png")
            plt.savefig(chart_path)
            plt.close()
            
            # 7. Menuliskan hasil analisis langsung ke file CSV (Manual tanpa library berat)
            csv_path = os.path.join("static", "hasil_analisis.csv")
            with open(csv_path, "w") as f_csv:
                # Tulis judul kolom di baris pertama
                f_csv.write("Header,Panjang_Basa,GC_Content_Persen,A,T,G,C\n")
                # Tulis isi datanya per baris
                for res in hasil_pipeline:
                    baris_teks = f"{res['header']},{len(res['sequence'])},{res['gc_content']:.2f},{res['counts']['A']},{res['counts']['T']},{res['counts']['G']},{res['counts']['C']}\n"
                    f_csv.write(baris_teks)
                
            # Kirim seluruh data hasil perhitungan ke halaman dashboard web
            return render_template('index.html', hasil=hasil_pipeline, top_3_juara=top_3, ada_data=True)
            
    # Jika web baru dibuka pertama kali (GET), jalankan kondisi kosong ini
    return render_template('index.html', hasil=None, top_3_juara=None, ada_data=False)

@app.route('/unduh-csv')
def unduh_csv():
    """Route khusus untuk memberikan file CSV saat tombol download diklik"""
    return send_file(os.path.join("static", "hasil_analisis.csv"), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)