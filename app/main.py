"""
Runs the streamlit app. 

Call this file in the terminal (from the `traingenerator` dir) 
via `streamlit run app/main.py`.
"""

import streamlit as st
from jinja2 import Environment, FileSystemLoader
import uuid
from github import Github
from dotenv import load_dotenv
import os
import collections

import utils


MAGE_EMOJI_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/259/mage_1f9d9.png"


# Set page title and favicon.
st.set_page_config(
    page_title="Code Generator for Machine Learning", page_icon=MAGE_EMOJI_URL,
)


# Set up github access for "Open in Colab" button.
# TODO: Maybe refactor this to another file.
load_dotenv()  # load environment variables from .env file
if os.getenv("GITHUB_TOKEN") and os.getenv("REPO_NAME"):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(os.getenv("REPO_NAME"))
    colab_enabled = True

    def add_to_colab(notebook):
        """Adds notebook to Colab by pushing it to Github repo and returning Colab link."""
        notebook_id = str(uuid.uuid4())
        repo.create_file(
            f"notebooks/{notebook_id}/generated-notebook.ipynb",
            f"Added notebook {notebook_id}",
            notebook,
        )
        colab_link = f"http://colab.research.google.com/github/{os.getenv('REPO_NAME')}/blob/main/notebooks/{notebook_id}/generated-notebook.ipynb"
        return colab_link


else:
    colab_enabled = False


# Display header.
st.markdown("<br>", unsafe_allow_html=True)
st.image(MAGE_EMOJI_URL, width=80)

"""
# Code Generator for Machine Learning

[![Star](https://img.shields.io/github/stars/jrieke/traingenerator.svg?logo=github&style=social)](https://gitHub.com/jrieke/traingenerator/stargazers)
&nbsp[![Follow](https://img.shields.io/twitter/follow/jrieke?style=social)](https://www.twitter.com/jrieke)
&nbsp[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/jrieke)
"""
st.markdown("<br>", unsafe_allow_html=True)
"""Jumpstart your machine learning code:

1. Specify model in the sidebar *(click on **>** if closed)*
2. Training code will be generated below
3. Download and do magic! :sparkles:

---
"""

# Compile a dictionary of all templates based on the subdirs in traingenerator/templates
# (excluding the "example" template).
# Format:
# {
#     "task1": "path/to/template",
#     "task2": {
#         "framework1": "path/to/template",
#         "framework2": "path/to/template"
#     },
# }
template_dict = collections.defaultdict(dict)
template_dirs = [
    f for f in os.scandir("templates") if f.is_dir() and f.name != "example"
]
# TODO: Find a good way to sort templates, e.g. by prepending a number to their name
#   (e.g. 1_Image classification_PyTorch).
template_dirs = sorted(template_dirs, key=lambda e: e.name)
for template_dir in template_dirs:
    try:
        # Templates with task + framework.
        task, framework = template_dir.name.split("_")
        template_dict[task][framework] = template_dir.path
    except ValueError:
        # Templates with task only.
        template_dict[template_dir.name] = template_dir.path
# print(template_dict)


# Show selectors for task and framework in sidebar (based on template_dict). These
# selectors determine which template (from template_dict) is used (and also which
# template-specific sidebar components are shown below).
with st.sidebar:
    st.info(
        "🎈 **NEW:** Add your own code template to this site! [Guide](https://github.com/jrieke/traingenerator#adding-new-templates)"
    )
    # st.error(
    #     "Found a bug? [Report it](https://github.com/jrieke/traingenerator/issues) 🐛"
    # )
    st.write("## Task")
    task = st.selectbox(
        "Which problem do you want to solve?", list(template_dict.keys())
    )
    if isinstance(template_dict[task], dict):
        framework = st.selectbox(
            "In which framework?", list(template_dict[task].keys())
        )
        template_dir = template_dict[task][framework]
    else:
        template_dir = template_dict[task]


# Show template-specific sidebar components (based on sidebar.py in the template dir).
template_sidebar = utils.import_from_file(
    "template_sidebar", os.path.join(template_dir, "sidebar.py")
)
inputs = template_sidebar.show()


# Generate code and notebook based on template.py.jinja file in the template dir.
env = Environment(
    loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True,
)
template = env.get_template("code-template.py.jinja")
code = template.render(header=utils.code_header, notebook=False, **inputs)
notebook_code = template.render(header=utils.notebook_header, notebook=True, **inputs)
notebook = utils.to_notebook(notebook_code)


# Display donwload/open buttons.
# TODO: Maybe refactor this (with some of the stuff in utils.py) to buttons.py.
st.write("")  # add vertical space
col1, col2, col3 = st.beta_columns(3)
open_colab = col1.button("🚀 Open in Colab")  # logic handled further down
with col2:
    utils.download_button(code, "generated-code.py", "🐍 Download (.py)")
with col3:
    utils.download_button(notebook, "generated-notebook.ipynb", "📓 Download (.ipynb)")
colab_error = st.empty()

# st.success(
#     "Enjoy this site? Leave a star on [the Github repo](https://github.com/jrieke/traingenerator) :)"
# )

# Display code.
# TODO: Think about writing Installs on extra line here.
st.code(code)


# Handle "Open Colab" button. Down here because to open the new web page, it
# needs to create a temporary element, which we don't want to show above.
if open_colab:
    if colab_enabled:
        colab_link = add_to_colab(notebook)
        utils.open_link(colab_link)
    else:
        colab_error.error(
            """
            **Colab support is disabled.** (If you are hosting this: Create a Github 
            repo to store notebooks and register it via a .env file)
            """
        )


# Tracking pixel to count number of visitors.
if os.getenv("TRACKING_NAME"):
    f"![](https://jrieke.goatcounter.com/count?p={os.getenv('TRACKING_NAME')})"
