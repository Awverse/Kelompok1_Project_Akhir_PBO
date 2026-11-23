from barang import Barang
from pengguna import Anggota, Admin
from peminjaman import Peminjaman
from validasi import tanggal_valid


class Inventaris:
    def __init__(self):
        self.__daftar_barang = []
        self.__daftar_pengguna = []
        self.__daftar_transaksi = []

    @property
    def daftar_barang(self):
        return self.__daftar_barang

    @property
    def daftar_pengguna(self):
        return self.__daftar_pengguna

    def cari_barang(self, kode):
        for barang in self.__daftar_barang:
            if barang.kode_barang == kode.strip().upper():
                return barang
        return None

    def cari_pengguna(self, id_pengguna):
        for pengguna in self.__daftar_pengguna:
            if pengguna.id_pengguna == id_pengguna.strip().upper():
                return pengguna
        return None

    def cari_transaksi(self, id_transaksi):
        for transaksi in self.__daftar_transaksi:
            if transaksi.id_transaksi == id_transaksi.strip().upper():
                return transaksi
        return None

    def tambah_barang(self, barang):
        if not isinstance(barang, Barang):
            return False, "Data harus berupa objek Barang."
        if self.cari_barang(barang.kode_barang) is not None:
            return False, "Kode barang sudah digunakan."
        self.__daftar_barang.append(barang)
        return True, "Barang berhasil ditambahkan."

    def tambah_pengguna(self, pengguna):
        if not isinstance(pengguna, (Anggota, Admin)):
            return False, "Pengguna harus berupa Anggota atau Admin."
        if self.cari_pengguna(pengguna.id_pengguna) is not None:
            return False, "ID pengguna sudah digunakan."
        self.__daftar_pengguna.append(pengguna)
        return True, "Pengguna berhasil ditambahkan."

    def perbarui_data_barang(self, kode, nama, kategori):
        barang = self.cari_barang(kode)
        if barang is None:
            return False, "Barang tidak ditemukan."
        if nama.strip() == "" or kategori.strip() == "":
            return False, "Nama dan kategori barang wajib diisi."

        # Yang diubah hanya identitas. Jumlah barang mengikuti transaksi.
        barang.nama = nama
        barang.kategori = kategori
        return True, "Identitas barang berhasil diperbarui."

    def proses_peminjaman(self, id_transaksi, id_anggota, id_admin,
                          kode_barang, jumlah, tanggal_pinjam, rencana_kembali):
        if id_transaksi.strip() == "":
            return False, "ID transaksi wajib diisi."
        if self.cari_transaksi(id_transaksi) is not None:
            return False, "ID transaksi sudah digunakan."

        anggota = self.cari_pengguna(id_anggota)
        admin = self.cari_pengguna(id_admin)
        barang = self.cari_barang(kode_barang)
        if not isinstance(anggota, Anggota):
            return False, "ID anggota tidak ditemukan atau perannya bukan Anggota."
        if not isinstance(admin, Admin):
            return False, "ID admin tidak ditemukan atau perannya bukan Admin."
        if barang is None:
            return False, "Kode barang tidak ditemukan."

        if not tanggal_valid(tanggal_pinjam) or not tanggal_valid(rencana_kembali):
            return False, "Tanggal harus valid dengan format YYYY-MM-DD."
        # String tanggal dapat dibandingkan karena formatnya sama dan lengkap.
        if rencana_kembali < tanggal_pinjam:
            return False, "Rencana kembali tidak boleh mendahului tanggal pinjam."
        if type(jumlah) != int or jumlah <= 0:
            return False, "Jumlah harus berupa bilangan bulat positif."
        if not barang.cek_ketersediaan(jumlah):
            return False, "Stok tersedia tidak mencukupi."

        transaksi = Peminjaman(id_transaksi, anggota, admin, barang, jumlah,
                               tanggal_pinjam, rencana_kembali)
        berhasil, pesan = barang.kurangi_stok(jumlah)
        if not berhasil:
            return False, pesan
        self.__daftar_transaksi.append(transaksi)
        return True, "Peminjaman berhasil dicatat."

    def proses_pengembalian(self, id_transaksi, tanggal_kembali, kondisi):
        transaksi = self.cari_transaksi(id_transaksi)
        if transaksi is None:
            return False, "Transaksi tidak ditemukan."
        if transaksi.status != "aktif":
            return False, "Transaksi sudah selesai dan tidak dapat dikembalikan lagi."
        if not tanggal_valid(tanggal_kembali):
            return False, "Tanggal kembali harus valid dengan format YYYY-MM-DD."
        if tanggal_kembali < transaksi.tanggal_pinjam:
            return False, "Tanggal kembali tidak boleh mendahului tanggal pinjam."

        kondisi = kondisi.strip().lower()
        if kondisi != "baik" and kondisi != "rusak":
            return False, "Kondisi hanya boleh baik atau rusak."

        # Jumlah diambil dari transaksi karena pengembaliannya harus penuh.
        berhasil, pesan = transaksi.barang.catat_pengembalian(transaksi.jumlah, kondisi)
        if not berhasil:
            return False, pesan
        transaksi.selesaikan_transaksi(tanggal_kembali, kondisi)
        return True, "Pengembalian berhasil dicatat."

    def daftar_transaksi_aktif(self):
        hasil = []
        for transaksi in self.__daftar_transaksi:
            if transaksi.status == "aktif":
                hasil.append(transaksi)
        return hasil

    def riwayat_peminjaman(self):
        hasil = []
        for transaksi in self.__daftar_transaksi:
            if transaksi.status == "selesai":
                hasil.append(transaksi)
        return hasil

    def jumlah_dipinjam(self, kode_barang):
        jumlah = 0
        for transaksi in self.__daftar_transaksi:
            if transaksi.status == "aktif" and transaksi.barang.kode_barang == kode_barang.strip().upper():
                jumlah += transaksi.jumlah
        return jumlah
