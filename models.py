from peewee import *
from sqlalchemy import Integer

host = '192.168.2.251'
user = 'dani'
passwd = 'dani123'

db = PostgresqlDatabase('sekolah', user=user, host=host, password=passwd)


class User(Model):
    id = IntegerField()
    username = CharField(primary_key=True)
    password = CharField()
    email = CharField()
    role = CharField()
    nama = CharField()

    class Meta:
        database = db
        db_table = "tbl_user"


class desc_gender(Model):
    id = IntegerField(primary_key=True)
    keterangan = CharField()

    class Meta():
        database = db
        db_table = "tbl_opt_jeniskelamin"


class desc_religion(Model):
    id = IntegerField()
    keterangan = CharField()

    class Meta:
        database = db
        db_table = "tbl_opt_agama"


class Siswa(Model):
    id = IntegerField()
    nis = CharField(primary_key=True)
    nama = CharField()
    jeniskelamin = CharField()
    jalan = CharField()
    provinsi = CharField()
    kota = CharField()
    kecamatan = CharField()
    desa = CharField()
    rt = CharField()
    rw = CharField()
    kodepos = CharField()
    agama = CharField()
    tempatlahir = CharField()
    tanggallahir = CharField()
    namaayah = CharField()
    namaibu = CharField()
    namawali = CharField()
    kontakwali = CharField()

    class Meta:
        database = db
        db_table = "tbl_siswa_profile"


class Nilai(Model):
    id = IntegerField()
    nis = CharField()
    mtk = CharField()
    ipa = CharField()
    ips = CharField()
    bindo = CharField()
    bingg = CharField()
    fisika = CharField()
    kimia = CharField()
    sejarah = CharField()
    semester = CharField()

    class Meta:
        database = db
        db_table = "tbl_siswa_nilai"


class Role(Model):
    id = IntegerField()
    nama = CharField()
    usermanager = CharField()
    rolemanager = CharField()
    profilesiswa = CharField()
    raporsiswa = CharField()
    komentar = TextField()

    class Meta:
        database = db
        db_table = "tbl_role"


def initialize():
    db.connect()
