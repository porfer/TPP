
from flask_restful import Api
from App.apis.CinemasApi import CinemasResource
from App.apis.CityApi import CityResource
from App.apis.IconApi import IconResource
from App.apis.LoginApi import Login
from App.apis.MoviesApi import MoviesResource
from App.apis.MoviesTestApi import MoviesTestResource
from App.apis.PasswordAPi import PasswordChange
from App.apis.RegisterApi import RegisterResouce
from App.apis.UserActiveApi import UserActive




api = Api()

def init_api(app):
    api.init_app(app)


api.add_resource(CityResource, '/api/v1/city/', endpoint='city')
api.add_resource(RegisterResouce, '/api/v1/register/', endpoint='register')
api.add_resource(UserActive, '/api/v1/useractive/', endpoint='useractive')
api.add_resource(Login, '/api/v1/login/', endpoint='login')
api.add_resource(PasswordChange, '/api/v1/passwdchange/', endpoint='passwdchange')
api.add_resource(MoviesTestResource, '/api/v1/moviestest/', endpoint='moviestest')
api.add_resource(MoviesResource, '/api/v1/movies/', endpoint='movies')
api.add_resource(CinemasResource, '/api/v1/cinemas/', endpoint='cinemas')
api.add_resource(IconResource, '/api/v1/icon/', endpoint='icon')