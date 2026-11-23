class Barang:
    def __init__(self, kode_barang, nama, kategori, jumlah_total):
        if kode_barang.strip() == "" or nama.strip() == "" or kategori.strip() == "":
            raise ValueError("Kode, nama, dan kategori barang wajib diisi.")
        if type(jumlah_total) != int or jumlah_total < 0:
            raise ValueError("Jumlah awal harus bilangan bulat nol atau lebih.")

        self.__kode_barang = kode_barang.strip().upper()
        self.__nama = nama.strip()
        self.__kategori = kategori.strip()
        self.__jumlah_total = jumlah_total
        self.__jumlah_tersedia = jumlah_total
        self.__jumlah_rusak = 0

    @property
    def kode_barang(self):
        return self.__kode_barang

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai_baru):
        if nilai_baru.strip() == "":
            raise ValueError("Nama barang wajib diisi.")
        self.__nama = nilai_baru.strip()

    @property
    def kategori(self):
        return self.__kategori

    @kategori.setter
    def kategori(self, nilai_baru):
        if nilai_baru.strip() == "":
            raise ValueError("Kategori barang wajib diisi.")
        self.__kategori = nilai_baru.strip()

    @property
    def jumlah_total(self):
        return self.__jumlah_total

    @property
    def jumlah_tersedia(self):
        return self.__jumlah_tersedia

    @property
    def jumlah_rusak(self):
        return self.__jumlah_rusak

    def cek_ketersediaan(self, jumlah):
        return type(jumlah) == int and jumlah > 0 and jumlah <= self.__jumlah_tersedia

    def kurangi_stok(self, jumlah):
        if not self.cek_ketersediaan(jumlah):
            return False, "Jumlah peminjaman tidak valid atau stok tidak cukup."
        self.__jumlah_tersedia -= jumlah
        return True, "Stok tersedia berhasil dikurangi."

    def catat_pengembalian(self, jumlah, kondisi):
        if type(jumlah) != int or jumlah <= 0:
            return False, "Jumlah pengembalian harus bilangan bulat positif."
        if kondisi != "baik" and kondisi != "rusak":
            return False, "Kondisi hanya boleh baik atau rusak."

        # Bagian dari jumlah total yang belum tersedia atau tercatat rusak.
        belum_kembali = self.__jumlah_total - self.__jumlah_tersedia - self.__jumlah_rusak
        if jumlah > belum_kembali:
            return False, "Jumlah pengembalian melebihi barang yang dipinjam."

        if kondisi == "baik":
            self.__jumlah_tersedia += jumlah
        else:
            self.__jumlah_rusak += jumlah
        return True, "Jumlah barang berhasil diperbarui."
