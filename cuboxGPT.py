import typer
from chatFromDB import queryFromPersistantDB
import db
import webParser

app = typer.Typer()


@app.command()
def init_database():
    # Code to initialize the database
    typer.echo("Initializing the database...")
    db.initDatabase()


@app.command()
def search(query: str):
    # Code to query the database
    queryFromPersistantDB(query)


@app.command()
def import_data(filepath: str = 'cubox_export.html'):
    typer.echo("Importing data into the database...")
    webParser.loadWebContentFromCuboxExport(filepath)


if __name__ == "__main__":
    app()
