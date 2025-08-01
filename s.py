from pymongo import MongoClient
import gridfs

client=MongoClient("mongodb://localhost:27017/")
db=client["hotel_booking"]
fs=gridfs.GridFS(db)
hotel_data=[
    {"name":"taj hotel","location":"mumbai","price":10000,"image":"img1.jpg"},    
    {"name":"taj deccan","location":"hyderabad","price":20000,"image":"img2.jpg"}, 
    {"name":"spicy hotel","location":"chennai","price":30000,"image":"img3.avif"} 
]
for hotel in hotel_data:
    with open(f"static/images/{hotel['image']}","rb") as img_file:
        i=fs.put(img_file,filename=hotel["image"])
        db.hotels.insert_one({
            "name":hotel["name"],
            "location":hotel["location"],
            "price":hotel["price"],
            "i":i
        }) 
print("added succesfully")