# cuboxGPT

Use GPT to help users quickly search/chat with your large cubox dataset.

# Use

Install the package.

```bash
pip install cuboxGPT
```

Export the cubox dataset as html file.
![export](./media/cubox_export.png)

Call the command line tool

```bash
# set openai api key
EXPORT OPENAI_API_KEY=<your openai api key>

# import all cubox bookmarks and downald all web contents.
# Note that the cli will output links that are failed to download and links that have not enough contents.
cuboxgpt  import-data <cubox_export.html file location>

# Init the vector database. Put all downloaded web contents to the vector database and generate embeddings. Save the database in db/ folder.
cuboxgpt init-database

# chat/seach with the dataset
cuboxgpt search <query>
```

# Development

```bash
venv ./venv
source ./venv/bin/activate
pip install --editable .
```

`cuboxGPT.py` has all comand line tools implementation.

`chatFromDB.py` reads from the database and implement the query function.

`webPraser.py` takes responsibility to parse the html file and download the web contents.

`db.py` generate embeddings and save web contents to the database.

`pyproject.toml` contains ruff lint configuration.

# Roadmap

Goal: Enhance the search experience and easily keep datasets up to date.

- [ ] Better CRUD on database. Users can update/delete single ducoments in the database.
- [ ] Seach document with custom filter on metadata.
- [ ] Better parsing rule for certain websites like Twitter, Youtube with Chinese characters, Weixin
- [ ] Better updating experience if user input a new cubox export file.
- [ ] Pagination for search results.
- [ ] Analyze user's query to better hit keywords.
- [ ] For links failed to download, retry with Seleum
- [ ] Support multi-threading for downloading web contents.
- [ ] Better title by supporting open graph meta tags
