class SequenceParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_fasta(self):
        """Membaca file FASTA menggunakan List dan Dictionary standar"""
        sequences = []  # List untuk menampung seluruh data sekuens
        current_header = ""
        current_seq = ""

        with open(self.filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith(">"):
                    # Jika sebelum baris ini sudah ada sekuens yang terbaca, simpan dulu
                    if current_header != "":
                        data = {"header": current_header, "sequence": current_seq}
                        sequences.append(data)
                    
                    # Ambil header baru (hilangkan tanda '>')
                    current_header = line[1:]
                    current_seq = ""
                else:
                    # Gabungkan baris sekuens dan pastikan huruf kapital
                    current_seq = current_seq + line.upper()
            
            # Jangan lupa simpan sekuens yang paling terakhir setelah loop selesai
            if current_header != "":
                data = {"header": current_header, "sequence": current_seq}
                sequences.append(data)
                
        return sequences

    def parse_fastq(self):
        """Membaca file FASTQ berdasarkan pola kelipatan 4 baris"""
        sequences = []
        with open(self.filepath, 'r') as file:
            lines = file.readlines()
            
        # File FASTQ memiliki 4 baris per satu record data
        for i in range(0, len(lines), 4):
            header = lines[i].strip()[1:] # Ambil header tanpa tanda '@'
            sequence = lines[i+1].strip().upper() # Baris ke-2 adalah sekuens nukleotida
            
            data = {"header": header, "sequence": sequence}
            sequences.append(data)
            
        return sequences


class SequenceAnalyzer:
    def count_nucleotides(self, sequence):
        """Menghitung frekuensi nukleotida menggunakan Dictionary dasar"""
        counts = {"A": 0, "T": 0, "G": 0, "C": 0}
        
        for base in sequence:
            if base in counts:
                counts[base] = counts[base] + 1
        return counts

    def calculate_gc_content(self, sequence):
        """Menghitung persentase nilai GC Content"""
        if len(sequence) == 0:
            return 0.0
            
        counts = self.count_nucleotides(sequence)
        gc_total = counts["G"] + counts["C"]
        percentage = (gc_total / len(sequence)) * 100
        return percentage