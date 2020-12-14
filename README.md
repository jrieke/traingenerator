<h1 align="center">
    traingenerator
</h1>

<p align="center">
    <strong>🧙&nbsp; A web app to generate template code for machine learning</strong>
</p>

<p align="center">
    <a href="https://www.buymeacoffee.com/jrieke"><img src="https://img.shields.io/badge/Buy%20me%20a-coffee-orange.svg?logo=buy-me-a-coffee&logoColor=orange"></a>
    <a href=""><img src="https://img.shields.io/github/license/jrieke/traingenerator.svg"></a>
</p>

<br>

<p align="center">
    <img src="docs/assets/demo.gif" width=600>
</p>

<br>

<h3 align="center">
    🎉 traingenerator is now live! 🎉
    <br><br>
    Try it out: <br>
    >>> <a href="https://traingenerator.jrieke.com">https://traingenerator.jrieke.com</a> <<<
</h3>

<!--
<p align="center"><strong>
    Try it out: <br>
    >>> <a href="https://traingenerator.jrieke.com">https://traingenerator.jrieke.com</a> <<<</strong>
</p>
-->

<br>

Generate custom template code for PyTorch & sklearn, using a simple web UI built with [streamlit](https://www.streamlit.io/). traingenerator offers multiple options for preprocessing, model setup, training, and visualization (using Tensorboard or comet.ml). It exports to .py, Jupyter Notebook, or  [Google Colab](https://colab.research.google.com/). The perfect tool to jumpstart your next machine learning project! ✨

<br>

---

<br>

**Note: The steps below are only required for developers who want to run/deploy traingenerator locally.**

## Installation

```bash
git clone https://github.com/jrieke/traingenerator.git
cd traingenerator
pip install -r requirements.txt
```

*Optional: For the "Open in Colab" button to work you need to set up a Github repo 
where the notebook files can be stored (Colab can only open public files if 
they are on Github). After setting up the repo, create a file `.env` with content:*

```bash
GITHUB_TOKEN=<your-github-access-token>
REPO_NAME=<user/notebooks-repo>
```

*If you don't set this up, the app will still work but the "Open in Colab" button 
will only show an error message.*


## Running locally

```bash
streamlit run app/main.py
```

Make sure to run always from the `traingenerator` dir (not from the `app` dir), 
otherwise the app will not be able to find the templates.

## Deploying to Heroku

First, [install heroku and login](https://devcenter.heroku.com/articles/getting-started-with-python#set-up). 
To create a new deployment, run inside `traingenerator`:

```
heroku create
git push heroku main
heroku open
```

To update the deployed app, commit your changes and run:

```
git push heroku main
```

*Optional: If you set up a Github repo to enable the "Open in Colab" button (see above),
you also need to run:*

```
heroku config:set GITHUB_TOKEN=<your-github-access-token>
heroku config:set REPO_NAME=<user/notebooks-repo>
```

## Testing

```bash
pytest ./tests
```

This generates Python codes with different configurations (just like the app would do) 
and checks that they run. The streamlit app itself is not tested at the moment.
