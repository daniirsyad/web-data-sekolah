import hashlib
import json
from unittest import result
from importlib_metadata import method_cache
from playhouse.shortcuts import model_to_dict
import peewee
from flask import Flask, flash, jsonify, render_template, request, url_for, redirect, session
from jinja2 import Template

from api import *
import models

# Function


def getNilai(nis):
    dataNilai = models.Nilai.select().where(
        models.Nilai.nis == nis).order_by(models.Nilai.semester.asc())
    return dataNilai


# End Function
app = Flask(__name__)
app.secret_key = 'thisismyscretkey123333'
app.jinja_env.globals.update(
    getKabupaten=getKabupaten, getKecamatan=getKecamatan, getDesa=getDesa, getNilai=getNilai)

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


@app.route("/raporsiswa", methods=["POST", "GET"])
def raporsiswa():
    if 'username' in session:
        data = models.Siswa.select()
        return render_template("rapor.html", icon=icon, title="Rapor Siswa", data=data)
    else:
        return redirect(url_for("login"))


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
