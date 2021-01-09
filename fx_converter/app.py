from flask import Flask
from flask_graphql import GraphQLView

from fx_converter.database import db
from fx_converter.schema import schema
from fx_converter.service import basic_db_data


def init_db(app: Flask):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config.from_object("fx_converter.config")
    app.secret_key = app.config["SECRET_KEY"]
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql", schema=schema, graphiql=True,
            context={"db_session": None},
        ),
    )
    app.url_map.strict_slashes = False

    init_db(app)

    return app


app = create_app()


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()


@app.route('/test')
def test():
    basic_db_data()
    return 'lol'


if __name__ == "__main__":
    app.run()
