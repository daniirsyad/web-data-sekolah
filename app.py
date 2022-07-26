import hashlib
import json
from unittest import result
from importlib_metadata import method_cache
from playhouse.shortcuts import model_to_dict
import peewee
from flask import Flask, flash, jsonify, render_template, request, request_started, url_for, redirect, session
from jinja2 import Template

from api import *
import models

# Function


def getNilai(nis):
    dataNilai = models.Nilai.select().where(
        models.Nilai.nis == nis).order_by(models.Nilai.semester.asc())
    return dataNilai


def setListSemester(nis):
    fnis = nis
    dataList = models.Nilai.select(
        models.Nilai.semester).where(models.Nilai.nis == fnis).order_by(models.Nilai.semester.asc())
    # Total Semester
    dataSemester = ["1", "2", "3", "4", "5",
                    "6", "7", "8", "9", "10", "11", "12"]
    for x in dataList:
        if x.semester in dataSemester:
            dataSemester.remove(x.semester)
    print(dataSemester)
    return dataSemester


# End Function
app = Flask(__name__)
app.secret_key = 'thisismyscretkey123333'
app.jinja_env.globals.update(
    getKabupaten=getKabupaten, getKecamatan=getKecamatan, getDesa=getDesa, getNilai=getNilai, setListSemester=setListSemester)

icon = "/static/images/icon.png"


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
def home():
    if 'username' in session:
        data = models.Siswa.select()
        data_desc_gender = models.desc_gender.select()
        data_api_provinsi = getProvinsi()
        data_desc_agama = models.desc_religion.select()
        return render_template("index.html", icon=icon, title='Dashboard Manager', data=data, data_jeniskelamin=data_desc_gender, data_agama=data_desc_agama, data_provinsi=data_api_provinsi)

    return redirect(url_for("login"))

# Route untuk Login, Logout, dan SignUp


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        fusername = session['username']
        return redirect(url_for('home'))
    if request.method == "POST":
        fusername = request.form.get("username")
        fpassword = request.form.get("password")
        hashed_password = hashlib.sha256(fpassword.encode()).hexdigest()

        try:
            models.User.get(models.User.username == fusername,
                            models.User.password == hashed_password)
        except peewee.DoesNotExist:
            flash("Username/Password salah!", "failed")
            return redirect(url_for("login"))
        session['username'] = fusername
        return redirect(url_for('home'))
    return render_template("login.html", icon=icon)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('home'))

    if request.method == "POST":
        femail = request.form.get("email")
        fusername = request.form.get("username")
        fpassword = request.form.get("password")
        hashed_password = hashlib.sha256(fpassword.encode()).hexdigest()

        try:
            models.User.get(models.User.username == fusername)
        except peewee.DoesNotExist:
            models.User.create(
                email=femail, username=fusername, password=hashed_password)
            flash("Berhasil membuat akun!", "success")
            return redirect(url_for("login"))
        flash("Username sudah digunakan!", "failed")
        return redirect(url_for("signup"))

    return render_template("signup.html", icon=icon)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# End


@app.route("/addsiswa", methods=["POST"])
def addsiswa():
    if 'username' in session:
        fusername = session["username"]
        fnama = request.form.get("nama")
        ftempatlahir = request.form.get("tempatlahir")
        ftanggallahir = request.form.get("tanggallahir")
        fjeniskelamin = request.form.get("jeniskelamin")
        fagama = request.form.get("agama")
        fnamaayah = request.form.get("namaayah")
        fnamaibu = request.form.get("namaibu")
        fnamawali = request.form.get("namawali")
        fkontakwali = request.form.get("kontakwali")
        fjalan = request.form.get("jalan")
        fprovinsi = request.form.get("provinsi")
        fkota = request.form.get("kota")
        fkecamatan = request.form.get("kecamatan")
        fdesa = request.form.get("desa")
        frt = request.form.get("rt")
        frw = request.form.get("rw")
        fkodepos = request.form.get("kodepos")

        models.Siswa.create(nama=fnama, tempatlahir=ftempatlahir,
                            tanggallahir=ftanggallahir, jeniskelamin=fjeniskelamin, agama=fagama, namaayah=fnamaayah, namaibu=fnamaibu,
                            namawali=fnamawali, kontakwali=fkontakwali, jalan=fjalan, provinsi=fprovinsi, kota=fkota, kecamatan=fkecamatan,
                            desa=fdesa, rt=frt, rw=frw, kodepos=fkodepos)
        flash("Berhasil menambahkan data!", "success")
        return redirect(url_for("home"))
    flash("Silahkan Login kembali!", "failed")
    return redirect(url_for("login"))


@app.route("/getsiswa/<nis>", methods=["GET"])
def getsiswa(nis):
    if 'username' in session:
        get_data = models.Siswa.get(models.Siswa.nis == nis)
        value = model_to_dict(get_data)

        return {'value': value}
    return redirect(url_for("login"))


@app.route("/updatesiswa/<nis>", methods=["POST"])
def updatesiswa(nis):
    if 'username' in session:
        fnis = nis
        fnama = request.form.get("nama")
        ftempatlahir = request.form.get("tempatlahir")
        ftanggallahir = request.form.get("tanggallahir")
        fjeniskelamin = request.form.get("jeniskelamin")
        fagama = request.form.get("agama")
        fnamaayah = request.form.get("namaayah")
        fnamaibu = request.form.get("namaibu")
        fnamawali = request.form.get("namawali")
        fkontakwali = request.form.get("kontakwali")
        fjalan = request.form.get("jalan")
        fprovinsi = request.form.get("provinsi")
        fkota = request.form.get("kota")
        fkecamatan = request.form.get("kecamatan")
        fdesa = request.form.get("desa")
        frt = request.form.get("rt")
        frw = request.form.get("rw")
        fkodepos = request.form.get("kodepos")
        feditalamat = request.form.get("editalamat")

        if feditalamat:
            models.Siswa.update(nama=fnama, tempatlahir=ftempatlahir,
                                tanggallahir=ftanggallahir, jeniskelamin=fjeniskelamin, agama=fagama, namaayah=fnamaayah, namaibu=fnamaibu,
                                namawali=fnamawali, kontakwali=fkontakwali, jalan=fjalan, provinsi=fprovinsi, kota=fkota, kecamatan=fkecamatan,
                                desa=fdesa, rt=frt, rw=frw, kodepos=fkodepos).where(models.Siswa.nis == fnis).execute()
            flash("Berhasil mengupdate data!", "success")
            return redirect(url_for("home"))
        else:
            models.Siswa.update(nama=fnama, tempatlahir=ftempatlahir,
                                tanggallahir=ftanggallahir, jeniskelamin=fjeniskelamin, agama=fagama, namaayah=fnamaayah, namaibu=fnamaibu,
                                namawali=fnamawali, kontakwali=fkontakwali).where(models.Siswa.nis == fnis).execute()
            flash('Berhasil mengupdate data!', "success")
            return redirect(url_for("home"))
    flash("Silahkan Login terlebih dahulu!", "failed")
    return redirect(url_for("login"))


@app.route("/deletesiswa/<nis>", methods=["GET", "POST"])
def deletesiswa(nis):
    if 'username' in session:
        models.Siswa.delete().where(models.Siswa.nis == nis).execute()
        flash("Berhasil menghapus data!", "success")
        return redirect(url_for("home"))
    return redirect(url_for("login"))


# Halaman Rapor Nilai Siswa
@app.route("/raporsiswa", methods=["POST", "GET"])
def raporsiswa():
    if 'username' in session:
        data = models.Siswa.select()
        return render_template("rapor.html", icon=icon, title="Rapor Siswa", data=data)
    return redirect(url_for("login"))


@app.route("/raporsiswa/update/<nis>", methods=["GET", "POST"])
def updateRaporSiswa(nis):
    if 'username' in session:
        fnis = nis
        fsemester = request.form.get("semester")
        fmtk = request.form.get("mtk") or '0'
        fipa = request.form.get("ipa") or '0'
        fips = request.form.get("ips") or '0'
        fbindo = request.form.get("bindo") or '0'
        fbingg = request.form.get("bingg") or '0'
        ffisika = request.form.get("fisika") or '0'
        fkimia = request.form.get("kimia") or '0'
        fsejarah = request.form.get("sejarah") or '0'

        models.Nilai.update(mtk=fmtk, ipa=fipa, ips=fips, bindo=fbindo, bingg=fbingg, fisika=ffisika,
                            kimia=fkimia, sejarah=fsejarah).where(models.Nilai.nis == fnis, models.Nilai.semester == fsemester).execute()
        flash("Berhasil Merubah Data", "success")
        return redirect(url_for("raporsiswa"))


@app.route("/raporsiswa/add/<nis>", methods=["POST"])
def addRaporSiswa(nis):
    if 'username' in session:
        fnis = nis
        fsemester = request.form.get("semester")
        fmtk = request.form.get("mtk") or '0'
        fipa = request.form.get("ipa") or '0'
        fips = request.form.get("ips") or '0'
        fbindo = request.form.get("bindo") or '0'
        fbingg = request.form.get("bingg") or '0'
        ffisika = request.form.get("fisika") or '0'
        fkimia = request.form.get("kimia") or '0'
        fsejarah = request.form.get("sejarah") or '0'

        models.Nilai.create(nis=fnis, semester=fsemester, mtk=fmtk, ipa=fipa, ips=fips, bindo=fbindo, bingg=fbingg, fisika=ffisika,
                            kimia=fkimia, sejarah=fsejarah)
        flash("Berhasil menambahkan Nilai pada nis "+fnis, "success")
        return redirect(url_for("raporsiswa"))
    return redirect(url_for("login"))
# End Halaman Rapor Nilai Siswa

# Halaman Rapor Sikap Siswa


@app.route("/raporsikapsiswa", methods=["GET"])
def raporSikapSiswa():
    if 'username' in session:
        dataSiswa = models.Siswa.select(models.Siswa.nis, models.Siswa.nama)
        return render_template("raporSikapSiswa.html", icon=icon, title="Rapor Sikap Siswa", dataSiswa=dataSiswa)
    return redirect(url_for("login"))
# End Halaman Rapor Sikap Siswa

# Halaman User Manager


@app.route("/usermanager", methods=["GET"])
def userManager():
    if 'username' in session:
        dataUser = models.User.select()
        return render_template("accountManager.html", icon=icon, title="User Manager", data=dataUser)
    return redirect(url_for("login"))


@app.route("/usermanager/add", methods=["POST"])
def addUser():
    if 'username' in session:
        frole = request.form.get("role")
        fnama = request.form.get("nama")
        femail = request.form.get("email")
        fusername = request.form.get("username")
        fpassword = request.form.get("password")
        hashedPassword = hashlib.sha256(fpassword.encode()).hexdigest()

        try:
            models.User.get(models.User.username == fusername)
        except peewee.DoesNotExist:
            models.User.create(role=frole, nama=fnama, email=femail,
                               username=fusername, password=hashedPassword)
            flash("Berhasil Membuat Akun", "success")
            return redirect(url_for("userManager"))
        flash("Gagal Membuat Akun, Username sudah digunakan", "failed")
        return redirect(url_for("userManager"))
    flash("Silahkan Login terlebih dahulu", "failed")
    return redirect(url_for("login"))


@app.route("/usermanager/edit/<username>", methods=["POST"])
def editUser(username):
    if 'username' in session:
        fusername = request.form.get("username")
        frole = request.form.get("role")
        fnama = request.form.get("nama")
        femail = request.form.get("email")
        fpassword = hashlib.sha256(
            request.form.get("password").encode()).hexdigest()
        frepassword = hashlib.sha256(request.form.get(
            "retypepassword").encode()).hexdigest()

        if fpassword or frepassword:
            models.User.update(username=fusername, role=frole, nama=fnama, email=femail, password=fpassword).where(
                models.User.username == username).execute()
            flash("Berhasil Update Data User", "success")
            return redirect(url_for("userManager"))

        models.User.update(username=fusername, role=frole, nama=fnama, email=femail).where(
            models.User.username == username).execute()
        return redirect(url_for("userManager"))

    flash("Silahkan Login Terlebih Dahulu", "failed")
    return redirect(url_for("login"))


@app.route("/usermanager/delete/<username>", methods=["GET", "POST"])
def deleteUser(username):
    if 'username' in session:
        fusername = username
        models.User.delete().where(models.User.username == fusername).execute()
        flash("Berhasil menghapus User dengan Username "+fusername, "success")
        return redirect(url_for("userManager"))
    flash("Silahkan Login Terlebih Dahulu", "failed")
    return redirect(url_for("login"))


@app.route("/usermanager/getuser/<username>", methods=["GET"])
def getUser(username):
    if 'username' in session:
        fusername = username
        dataUser = models.User.get(models.User.username == fusername)
        value = model_to_dict(dataUser)
        return {"value": value}
    return redirect(url_for("login"))

# End Halaman User Manager

# Halaman Role Manager


@app.route("/rolemanager", methods=["GET"])
def roleManager():
    if 'username' in session:
        return render_template("roleManager.html", icon=icon, title="Role Manager")
    return redirect(url_for("login"))
# End Halaman Role Manager


# Halaman Akun


@app.route("/account", methods=["GET", "POST"])
def account():
    if 'username' in session:
        fusername = session['username']
        if request.method == "POST":
            fnama = request.form.get("nama")
            femail = request.form.get("email")
            fpassword = request.form.get("password")
            fnpassword = request.form.get("npassword")
            hashed_password = hashlib.sha256(fpassword.encode()).hexdigest()
            hashed_npassword = hashlib.sha256(fnpassword.encode()).hexdigest()

            if fpassword or fnpassword:
                try:
                    models.User.get(
                        models.User.username == fusername, models.User.password == hashed_password)
                except peewee.DoesNotExist:
                    flash("Password awal salah!", "failed")
                    return redirect(url_for("account"))
                models.User.update(
                    nama=fnama, email=femail, password=hashed_npassword).where(models.User.username == fusername).execute()
                flash("Berhasil merubah data!", "success")
                return redirect(url_for("account"))
            models.User.update(nama=fnama, email=femail).where(
                models.User.username == fusername).execute()
            flash("Berhasil merubah data!", "success")
            return redirect(url_for("account"))

        data = models.User.get(models.User.username == fusername)
        return render_template("account.html", icon=icon, title="Akun saya", data=data)
    return redirect(url_for("login"))
# End Halaman Akun

# PENCARIAN


@app.route("/cari/", methods=["GET", "POST"])
def pencarian():
    if 'username' in session:
        fkey = request.form.get("key")
        if not fkey:
            return redirect(url_for("home"))
        data = models.Siswa.select().where(
            (models.Siswa.nis.contains(fkey)) | (models.Siswa.nama.contains(fkey)))
        data_desc_gender = models.desc_gender.select()
        data_desc_religion = models.desc_religion.select()
        return render_template("index.html", icon=icon, title='Pencarian dari kata kunci "' + fkey + '"', data=data, data_jeniskelamin=data_desc_gender, data_agama=data_desc_religion)
    flash("Silahkan login terlebih dahulu!", "failed")
    return redirect(url_for("login"))


@app.route("/raporsiswa/cari/", methods=["GET", "POST"])
def pencarian_raport():
    if 'username' in session:
        fkey = request.form.get("key")
        if not fkey:
            return redirect(url_for("raporsiswa"))

        data = models.Siswa.select().where((models.Siswa.nis.contains(fkey))
                                           | (models.Siswa.nama.contains(fkey)))
        return render_template("rapor.html", icon=icon, title="Pencarian dari kata kunci " + fkey, data=data)
    else:
        return redirect(url_for("login"))
# END OF PENCARIAN


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
