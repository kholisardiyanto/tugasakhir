import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify

# 1. Hubungin Flask ke Firebase
# (Pastikan nama file json lu bener dan ada di folder yang sama)
cred = credentials.Certificate("kunci-firebase.json")

# Ganti link URL ini sama link database Firebase lu (ada di tab Realtime Database)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tugasakhir-6969-default-rtdb.asia-southeast1.firebasedatabase.app/' 
})

# 2. Bikin Mesin Flask
app = Flask(__name__)

# 3. Bikin Pintu Masuk Data (Endpoint)
@app.route('/api/data', methods=['GET'])
def terima_data():
    try:
        # Nangkep paket dari ESP32
        status_motor = request.args.get('status', 'AMAN')
        latitude = request.args.get('lat', 0.0)
        longitude = request.args.get('lng', 0.0)

        # Rapihin datanya
        data_baru = {
            "status": status_motor,
            "lat": float(latitude),
            "lng": float(longitude),
        }

        # Masukin ke Gudang Firebase (di folder /motor_utama)
        ref = db.reference('motor_utama')
        ref.set(data_baru)

        return jsonify({"pesan": "Data berhasil masuk gudang Firebase!", "data": data_baru}), 200

    except Exception as e:
        return jsonify({"pesan": "Waduh error Bar", "error": str(e)}), 500

# 4. Jalanin Mesin di Laptop (Buat Testing Local)
if __name__ == '__main__':
    app.run(debug=True, port=5000)