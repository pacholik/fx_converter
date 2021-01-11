#!/bin/sh

export DEBUG=1
export SQLALCHEMY_DATABASE_URI='sqlite:///fx.db'
python3 -m fx_converter.app
