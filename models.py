from mongoengine import Document, StringField, IntField, BinaryField, ListField
from views import app
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
db = PyMongo(app)


def get_albums():
    column_names = [
        ['id', 'id'],            
        ['year', 'Год выхода'],
        ['title', 'Название'],
        ['artists', 'Исполнители'],
        ['tracks', 'Треки']
    ]
    columns = ['id', 'Название', 'Год выхода', 'Исполнители', 'Треки']
    documents = db.db.albums.find()
    data = []
    for document in documents:
        row = {}
        for column_name in column_names:
            if column_name[0] in ['artists', 'tracks']:
                row[column_name[1]] = document.get(column_name[0])
            elif column_name[0] == '_id':
                row[column_name[1]] = str(document.get(column_name[0]))
            else:
                row[column_name[1]] = document.get(column_name[0])
        data.append(row)
    return data, columns

def get_receptes():
    column_names = [
        ['id', 'id'],            
        ['title', 'Название'],
        ['cuisine', 'Кухня'],
        ['ingredients', 'Ингредиенты'],
        ['instructions', 'Рецепт']
    ]
    columns = ['id', 'Название', 'Кухня', 'Ингредиенты', 'Рецепт']
    documents = db.db.recipes.find()
    data = []
    for document in documents:
        row = {}
        for column_name in column_names:
            if column_name[0] in ['artists', 'tracks']:
                row[column_name[1]] = document.get(column_name[0])
            elif column_name[0] == '_id':
                row[column_name[1]] = str(document.get(column_name[0]))
            else:
                row[column_name[1]] = document.get(column_name[0])
        data.append(row)
    return data, columns

def edit_data(table, data):
    if table == 'Альбомы':
        data[3] = data[3].split('\n')
        data[4] = data[4].split('\n')
        while " " in data[3]:
            data[3].remove(" ")
        while " " in data[4]:
            data[4].remove(" ")
        db.db.albums.update_one({"id": int(data[0])}, {"$set": {
            "title": data[1],
            "year": data[2],
            "artists": data[3],
            "tracks": data[4]
        }})
    elif table == 'Рецепты':
        data[3] = data[3].split('\n')
        while " " in data[3]:
            data[3].remove(" ")
        db.db.recipes.update_one({"id": int(data[0])}, {"$set": {
        'title': data[1],
        'cuisine': data[2],
        'ingredients': data[3],
        'instructions': data[4]
        }})
        

def create_newRow(table, data):
    if table == 'Альбомы':
        try:
            ID = db.db.albums.find().sort("id", -1).limit(1)[0]["id"] + 1
        except:
            ID = 0
        data[3] = data[3].split('\n')
        data[4] = data[4].split('\n')
        while " " in data[3]:
            data[3].remove(" ")
        while " " in data[4]:
            data[4].remove(" ")
        db.db.albums.insert_one({
            "id": ID,
            "title": data[1],
            "year": data[2],
            "artists": data[3],
            "tracks": data[4]
        })
    elif table == 'Рецепты':
        try:
            ID = db.db.recipes.find().sort("id", -1).limit(1)[0]["id"] + 1
        except:
            ID = 0
        data[3] = data[3].split('\n')
        while " " in data[3]:
            data[3].remove(" ")
        db.db.recipes.insert_one({
            "id": ID,
            'title': data[1],
            'cuisine': data[2],
            'ingredients': data[3],
            'instructions': data[4]
        })

def delete_data(table, delID):
    if table == 'Альбомы':
        db.db.albums.delete_one({"id": int(delID)})
    if table == 'Рецепты':
        db.db.recipes.delete_one({"id": int(delID)})