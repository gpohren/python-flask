import click
import json
import pandas as pd
from ..extensions.database import mongo
from flask import Blueprint, cli

productCommands = Blueprint('product', __name__)

@productCommands.cli.command("import")
@click.argument("csvfile")
def import_csv(csvfile):
    collection = mongo.db.produtos
    data = pd.read_csv(csvfile)
    jsondata = json.loads(data.to_json(orient='records'))
    collection.insert_many(jsondata)
    return collection.count