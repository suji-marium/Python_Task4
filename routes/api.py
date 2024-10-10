import falcon

from rest.user_controller import UserGet,UserPost

def create_routes(db):
    app=falcon.App()

    app.add_route('/user-post',UserPost(db))
    app.add_route('/user-get/{email}',UserGet(db))
    app.add_route('/user-get', UserGet(db))
    return app
