"""
Adds tracking code for Google Analytics to a streamlit app.

WARNING: This changes your existing streamlit installation (specifically the file 
static/index.html in streamlit's main folder). It should only be called once after 
installation, so this file doesn't get cluttered!

The tag from Google Analytics (G-XXXXXXXXXX) has to be stored in an environment variable 
GOOGLE_ANALYTICS_TAG (or in a .env file).
"""

import streamlit as st
import os
from dotenv import load_dotenv


def replace_in_file(filename, oldvalue, newvalue):
    """Replace string in a file and optionally create backup_filename."""
    # Read in the file
    with open(filename, "r") as f:
        filedata = f.read()

    # Replace the target string
    filedata = filedata.replace(oldvalue, newvalue)

    # Write the file out again
    with open(filename, "w") as f:
        f.write(filedata)


# Load tag from environment variables.
load_dotenv()
tag = os.getenv("GOOGLE_ANALYTICS_TAG")

# Find path to streamlit's index.html.
st_dir = os.path.dirname(st.__file__)
index_filename = os.path.join(st_dir, "static", "index.html")

# Insert tracking code.
size_before = os.stat(index_filename).st_size
tracking_code = f"""<!-- Global site tag (gtag.js) - Google Analytics --><script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script><script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{tag}');</script>"""
replace_in_file(index_filename, "<head>", "<head>" + tracking_code)
size_after = os.stat(index_filename).st_size

print("Inserted tracking code into:", index_filename)
print("Size before:", size_before)
print("Size after: ", size_after)

