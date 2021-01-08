from flask import Flask
from flask_graphql import GraphQLView

from fx_converter.database import db
from fx_converter.models import Rate
from fx_converter.schema import schema


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


@app.route('/test')
def test():
    print(Rate.query.all())
    return 'lol'


if __name__ == "__main__":
    app.run()
