from flask import Flask, make_response
from flask_cors import CORS
from flask_migrate import Migrate


from .accounts.accounts import accounts
from .accounts.models import User
from .common import db, mail, jwt

app = Flask(__name__)
app.config.from_object('config.Config')
app.debug = app.config.get("DEBUG")

cors = CORS(
    app,
    supports_credentials=True,
    resources={
        r'/': {'origins': ['http://127.0.0.1:8080', 'http://localhost:8080']},
        r'/api/v1/*': {'origins': ['http://127.0.0.1:8080', 'http://localhost:8080']},
    })

app.register_blueprint(accounts)


db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)
jwt.init_app(app)

with app.app_context():
    pass
    # print(db.session.query(User).all())

# @app.before_request
# def before_request():
#
#
# @app.after_request
# def after_request(response):
#     print("after_request() called")
#     # abort(401)
#     return response


@app.route("/", methods=['get'])
def index():
    res = make_response({"Message": "Hello world"}, 200)
    return res


@jwt.user_lookup_loader
def user_loader_callback(jwt_header, jwt_payload):
    """Function for app, to return user object"""

    if jwt_header:
        username = jwt_payload["username"]
        user = User.query.filter_by(username=username).one_or_none()
        return user
    else:
        return None


