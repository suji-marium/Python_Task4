from routes.api import create_routes
from pymongo import MongoClient

#Database connection
client = MongoClient('mongodb://localhost:27017/')
db = client['users'] #Database name
app = create_routes(db)


if __name__ == '__main__':
    from wsgiref import simple_server

    with simple_server.make_server('127.0.0.1', 8000, app) as httpd:
        print("Serving on http://127.0.0.1:8000")
        httpd.serve_forever()
