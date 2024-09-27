import falcon

from resources.UserResource import UserGetResource,UserPostResource

def create_routes(db):
    app=falcon.App()

    app.add_route('/user-post',UserPostResource(db))
    app.add_route('/user-get/{email}',UserGetResource(db))
    return app
