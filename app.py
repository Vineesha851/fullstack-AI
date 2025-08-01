from flask import Flask, render_template, request, redirect, url_for, Response
from pymongo import MongoClient
import gridfs
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['hotel_booking']
fs = gridfs.GridFS(db)
hotels = db['hotels']
bookings = db['bookings']

@app.route('/')
def home():
    # Show only hotels with images
    all_hotels = list(hotels.find({"image_id": {"$exists": True}}))
    return render_template('index.html', hotels=all_hotels)

@app.route('/image/<image_id>')
def get_image(image_id):
    image = fs.get(ObjectId(image_id))
    return Response(image.read(), mimetype='image/jpeg')
    

@app.route('/book/<hotel_id>', methods=['GET', 'POST'])
def book(hotel_id):
    hotel = hotels.find_one({"_id": ObjectId(hotel_id)})
    if request.method == 'POST':
        bookings.insert_one({
            "hotel_id": hotel_id,
            "name": request.form['name'],
            "checkin": request.form['checkin'],
            "checkout": request.form['checkout']
        })
        return redirect(url_for('home'))
    return render_template('booking.html', hotel=hotel)

@app.route('/add-hotel', methods=['GET', 'POST'])
def add_hotel():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            image_id = fs.put(image, filename=image.filename)
            hotels.insert_one({
                "name": request.form['name'],
                "location": request.form['location'],
                "price": request.form['price'],
                "image_id": image_id
            })
        return redirect(url_for('home'))
    return render_template('add_hotel.html')

if __name__ == '__main__':
    app.run(debug=True)


