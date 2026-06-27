# 🧬 Platform Analisis Komparatif Sekuens Genomik Berbasis Web Flask 🧪

Proyek ini dibuat secara mandiri untuk memenuhi tugas mini project mata kuliah **Struktur Data**. Aplikasi ini dirancang sebagai *pipeline* analisis komputasi sekuens makromolekul (DNA/RNA) mentah berbasis web lokal (*local-hosting*) menggunakan framework **Flask** dengan sentuhan estetika visual bertema **Pewarnaan Gram (Crystal Violet & Safranin)** yang interaktif.

## 📝 Deskripsi Proyek & Konsep Pipeline
Aplikasi ini mengotomatisasi proses pengolahan data mentah genomik hingga menjadi informasi biologis yang siap diinterpretasikan untuk kebutuhan genomik komparatif. Alur kerja (*data flow*) yang diterapkan mengikuti prinsip dasar pipa data (*pipeline*) bioinformatika:

1. **Input Data (Parser):** Membaca file mentah berformat **FASTA** atau **FASTQ** (seperti data yang diperoleh dari NCBI) menggunakan pendekatan pemrograman berbasis objek (OOP) lewat kelas `SequenceParser`.
2. **Struktur Data List:** Menyimpan koleksi objek sekuens yang berhasil diekstrak ke dalam bentuk *List* dinamis untuk memproses banyak file/sekuens sekaligus secara simultan.
3. **Struktur Data Dictionary:** Melakukan iterasi untuk menghitung distribusi frekuensi kumulatif dari masing-masing basa nukleotida (Adenin [A], Timin [T], Guanin [G], Sitosin [C]) secara efisien menggunakan *Dictionary* melalui kelas `SequenceAnalyzer`.
4. **Kalkulasi & Sorting:** Menghitung persentase kandungan *GC-Content* per sekuens, lalu melakukan pengurutan data secara menurun (*descending*) berdasarkan nilai GC tersebut untuk menentukan peringkat *Top 3 Juara GC-Content*.
5. **Dashboard Output:** Menyajikan visualisasi grafik batang horizontal hasil generate otomatis dari komponen server, menampilkan tabel ringkasan hasil kalkulasi, serta menyediakan fitur unduh laporan dalam format **CSV**.

## 🧫 Studi Kasus Analisis: Komparasi 5 Strain *Escherichia coli*
Platform ini telah diuji untuk melakukan analisis komparatif terhadap cetak biru genetika dari 5 strain bakteri *Escherichia coli* dengan karakteristik fenotipe dan patogenisitas yang bertolak belakang:
* **E. coli K-12 MG1655 & BL21(DE3):** Strain laboratorium komensal dan ekspresi protein yang aman.
* **E. coli IAI39:** Strain komensal alami dari usus manusia sehat.
* **E. coli CFT073:** Strain patogen penyebab Infeksi Saluran Kemih (UPEC).
* **E. coli O157:H7 EDL933:** Strain patogen berbahaya pemicu diare berdarah dan sindrom uremik hemolitik (EHEC).

Melalui *pipeline* ini, pengguna dapat langsung memetakan variasi panjang basa nukleotida serta fluktuasi nilai *GC-content* yang menjadi penanda evolusioner penting (seperti hasil transfer gen horizontal atau *xenogeneic silencing*) pada masing-masing strain tersebut.

## ✨ Fitur Utama
* **Antarmuka Bertema Pewarnaan Gram:** Desain UI mewah menggunakan Bootstrap 5 dengan skema warna ungu gelap (*Crystal Violet*) dan aksen merah muda/oranye (*Safranin*) khas laboratorium mikrobiologi.
* **Dukungan Multi-format & Multi-upload:** Mampu memproses beberapa file sekuens sekaligus berformat `.fasta`, `.fa`, `.fastq`, maupun `.fq`.
* **Automated Backend Visualization:** Visualisasi distribusi nilai GC-Content berbentuk *horizontal bar chart* yang diproduksi langsung di background server menggunakan **Matplotlib** (`Agg` backend mode).
* **Manual CSV Exporter:** Konversi data hasil pemrosesan secara *on-the-fly* ke dalam file tabel `.csv` tanpa ketergantungan pada library eksternal yang berat.

## 🛠️ Struktur Direktori Proyek
```text
📦 platform-analisis-genomik
├── 📄 app.py               # Controller utama server Flask, penanganan upload, & routing
├── 📄 bioinformatics.py    # Core Logic OOP (Kelas SequenceParser & SequenceAnalyzer)
├── 📂 templates
│   └── 📄 index.html       # View: Antarmuka Dashboard utama (Landing & Result Page)
└── 📂 static
    ├── 📄 gc_chart.png     # Grafik visualisasi Matplotlib hasil generate otomatis
    └── 📄 hasil_analisis.csv # File CSV hasil ekspor data sekuens terurut
