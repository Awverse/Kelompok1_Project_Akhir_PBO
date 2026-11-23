class Pengguna:
    def __init__(self, id_pengguna, nama):
        if id_pengguna.strip() == "" or nama.strip() == "":
            raise ValueError("ID pengguna dan nama wajib diisi.")
        self.__id_pengguna = id_pengguna.strip().upper()
        self.__nama = nama.strip()

    @property
    def id_pengguna(self):
        return self.__id_pengguna

    @property
    def nama(self):
        return self.__nama

    def info_pengguna(self):
        return f"{self.id_pengguna} | {self.nama}"


class Anggota(Pengguna):
    def __init__(self, id_pengguna, nama, unit_organisasi):
        super().__init__(id_pengguna, nama)
        self.__unit_organisasi = unit_organisasi.strip()

    @property
    def unit_organisasi(self):
        return self.__unit_organisasi

    def info_pengguna(self):
        return f"{super().info_pengguna()} | Anggota | Unit: {self.unit_organisasi}"


class Admin(Pengguna):
    def __init__(self, id_pengguna, nama, jabatan):
        super().__init__(id_pengguna, nama)
        self.__jabatan = jabatan.strip()

    @property
    def jabatan(self):
        return self.__jabatan

    def info_pengguna(self):
        return f"{super().info_pengguna()} | Admin | Jabatan: {self.jabatan}"
