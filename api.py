import requests

token = '9c448d0480bee8e02b635fbbb0e9992acc73e66e17d536983279ec241db48c94'


def getProvinsi():
    api_url = 'https://api.binderbyte.com/wilayah/provinsi?api_key=' + token

    result = requests.get(api_url)

    if result.status_code == requests.codes.ok:
        data = result.json()

        hasil = data["value"]

        return hasil


def getKabupaten(id_prov, id):
    api_url = 'https://api.binderbyte.com/wilayah/kabupaten?api_key=' + \
        token + '&id_provinsi=' + id_prov

    result = requests.get(api_url)

    if result.status_code == requests.codes.ok:
        data = result.json()
        hasil = data["value"]
        for i in hasil:
            if i["id"] == id:
                return i["name"]


def getKecamatan(id_kab, id):
    api_url = 'https://api.binderbyte.com/wilayah/kecamatan?api_key=' + \
        token + '&id_kabupaten=' + id_kab

    result = requests.get(api_url)

    if result.status_code == requests.codes.ok:
        data = result.json()
        hasil = data["value"]
        for i in hasil:
            if i["id"] == id:
                return i["name"]


def getDesa(id_kec, id):
    api_url = 'https://api.binderbyte.com/wilayah/kelurahan?api_key=' + \
        token + '&id_kecamatan=' + id_kec

    result = requests.get(api_url)

    if result.status_code == requests.codes.ok:
        data = result.json()
        hasil = data["value"]
        for i in hasil:
            if i["id"] == id:
                return i["name"]
