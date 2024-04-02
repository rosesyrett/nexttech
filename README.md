# NextTech

This repository is designed to house the code that will produce leaderboards (based on categories) of the least used heimdall flags, to help inform Lyst staff on which flags should be cleaned up/deleted.

## Installation

### Prerequisites

#### GitHub Authentication

- [create a GitHub account](https://github.com/signup), // REMOVE THIS and chuck it in the doc because it's a privatae repo, they won't be able to see this README otherwise.
- [create an ssh key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) using `ssh-keygen`, and 
- [connect it to your github account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account#adding-a-new-ssh-key-to-your-account).

#### Python installation

This repository requires python 3.11 or higher. To configure this for your laptop, you can install python 3.11 using [homebrew](https://formulae.brew.sh/formula/python@3.11):

```bash
brew install python@3.11
```

### Installation

```bash
git clone git@github.com:rosesyrett/nexttech.git
cd nexttech
python3 -m venv .venv
source .venv/bin/activate
poetry install
```

## Usage
Before using this application, you will need to supply a username and password to authenticate
with the MongoDB:

```bash
export MONGO_ATLAS_USERNAME=nexttech
export MONGO_ATLAS_PASSWORD=<redacted>
```
Speak to Rose Syrett to get the password.

Open a python REPL (e.g. `ipython`, or you can just use `python`):

```bash
ipython
```

You will also need to export a username and a password,
And now you should be able to access all the documents in the database,

```ipython
from nexttech.db import Mongo

db = Mongo()
all_documents = db.all()

all_documents["web_onetrust_enabled"]
```

This should show something like...
```python
Feature({'name': 'web_onetrust_enabled', 'last_editor': 'sami.el.achi@ly.st', ..., 'variations': [], 'history': []}]})
```