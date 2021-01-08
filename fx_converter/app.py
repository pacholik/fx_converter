from flask import Flask
from flask_graphql import GraphQLView

from fx_converter.schema import schema


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

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
