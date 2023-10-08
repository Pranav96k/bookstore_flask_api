# from pymongo import MongoClient
# from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from bson import ObjectId


app = Flask(__name__)

CORS(app)

# MongoDB connection
# Replace with your MongoDB connection string
client = MongoClient('mongodb://localhost:27017')
db = client['bookstore']  # Use your database name
collection = db['books']  # Use your collection name


@app.route('/users')
def index():
    # Retrieve data from MongoDB
    books = list(collection.find())
    # Ensure that the data structure matches the keys used in React
    formatted_books = [
        {
            '_id': str(book['_id']),  # Convert ObjectId to string if needed
            'coverImage': book['CoverImage'],
            'title': book['Title'],
            'author': book['Author'],
            # Add other necessary keys here
        }
        for book in books
    ]
    return jsonify(formatted_books)  # Return data as JSON


@app.route('/books')
def search_books():
    # Get the search query from the URL parameter 'q'
    search_query = request.args.get('q', '')
    books = list(collection.find())

    # Filter books based on the search query
    filtered_books = [
        {
            '_id': str(book['_id']),
            'coverImage': book['CoverImage'],
            'title': book['Title'],
            'author': book['Author'],
            'genre': book['Genre'],
            'publicationdate': book['PublicationDate'],
            'price': book['Price']
            # Add other necessary keys here
        }
        for book in books
        if search_query.lower() in book['Title'].lower() or search_query.lower() in book['Author'].lower()
    ]

    return jsonify(filtered_books)


@app.route('/books/<string:bookId>', methods=['GET'])
def get_book_details(bookId):
    objectId = ObjectId(bookId)
    print(f"Received bookId: {objectId}")
    book = collection.find_one({'_id': objectId})
    print(f"abc book: {book}")
    if book is None:
        # Handle the case where the book is not found
        print("Book not found in the database")
        return jsonify({'error': 'Book not found'}), 404

    # Construct a response with the book details
    response_data = {
        'title': book['Title'],
        'author': book['Author'],
        'genre': book['Genre'],
        # Add other book details here
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)


# app = Flask(__name__)

# client = MongoClient('mongodb://localhost:27017')

# db = client['bookstore']  # DB name


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/users', methods=['POST', 'GET'])
# def data():
#     # if request.method == 'POST':
#     #     body = request.json
#     #     firstname = body['firstname']
#     #     lastname = body['lastname']
#     #     emailID = body['emailID']

#     #     db['users'].insert_one({
#     #         "firstname": firstname,
#     #         "lastname": lastname,
#     #         "emailID": emailID
#     #     })

#     #     return jsonify({
#     #         'status': 'Data is posted to MongoDB',
#     #         'firstname': firstname,
#     #         'lastname': lastname,
#     #         'emailID': emailID
#     #     })

#     if request.method == 'GET':
#         allData = db['users'].find
#         dataJson = []
#         for data in allData:
#             id = data['_id']
#             Tital = data['Tital']
#             Author = data['Author']
#             Genere = data['Genere']
#             dataDict = {
#                 'id': str(id),
#                 'Tital': Tital,
#                 'Author': Author,
#                 'Genere': Genere,
#             }
#             dataJson.append(dataDict)
#         print(dataJson)
#         return jsonify(dataJson)


# if __name__ == '__main__':
#     app.debug = True
#     app.run()
