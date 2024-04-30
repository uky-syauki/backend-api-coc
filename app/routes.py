from flask import request, jsonify

from app.models import Pendaftar
from app import app, db


@app.route("/api/add", methods=["POST","GET"])
def add():
    try:
        data = request.json
        if len(data['nama']) < 2:
            print(f"Data nama {data['nama']} < 2")
            return jsonify({"message":"nama"})
        if len(data['email']) < 2 or "@" not in data['email']:
            print(f"Data email {data['email']} < 2")
            return jsonify({"message":"email"})
        if len(data['telepon']) < 2:
            print(f"Data telepon {data['telepon']} < 2")
            return jsonify({"message":"telepon"})
        if len(data['asalSekolah']) < 2:
            print(f"Data asalSekolah {data['asalSekolah']} < 2")
            return jsonify({"message":"asalSekolah"})
        
        orangDaftar = Pendaftar(nama_lengkap=data['nama'], email=data['email'], no_telp=data['telepon'], asal=data['asalSekolah'])
        db.session.add(orangDaftar)
        db.session.commit()
        print(data)
        return jsonify({"message":"success","nama":orangDaftar.nama_lengkap})
    except:
        db.session.rollback()
        return jsonify({"message":"error"})
        

@app.route("/api/<pendaftar>", methods=["GET","POST"])
def orang(pendaftar):
    data = Pendaftar.query.filter_by(nama_lengkap=pendaftar).first()
    print(bool(data))
    if data:
        newData = {
            "nama_lengkap":data.nama_lengkap,
            "email":data.email,
            "telepon":data.no_telp,
            "asal_sekolah":data.asal,
            "status":"Berhasil Mendaftar"
        }
        return jsonify(newData)
    else:
        newData = {
            "nama_lengkap":pendaftar,
            "email":"Tidak ada",
            "telepon":"Tidak ada",
            "asal_sekolah":"Tidak ada",
            "status":"Tidak Terdaftar"
        }
        return jsonify(newData)


@app.route("/api/get/<nama>/<kunci>", methods=["GET","POST"])
def ambil(nama, kunci):
    if nama == "coc02" and kunci == "coconut@013":
        data = Pendaftar.query.all()
        newData = {}
        for isi in data:
            newData[str(isi.id)] = {}
            newData[str(isi.id)]['nama_lengkap'] = isi.nama_lengkap
            newData[str(isi.id)]['email'] = isi.email
            newData[str(isi.id)]['telepon'] = isi.no_telp
            newData[str(isi.id)]['asal'] = isi.asal
        return jsonify({"message":"success","data":newData})
    return jsonify({"message":"Tidak memiliki akses!"})
