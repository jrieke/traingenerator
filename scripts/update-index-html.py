"""
Update index.html from streamlit by 

- adding tracking code for Google Analytics
- adding meta tags for search engines
- adding meta tags for social preview

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


# Find path to streamlit's index.html.
st_dir = os.path.dirname(st.__file__)
index_filename = os.path.join(st_dir, "static", "index.html")

# Insert tracking code for Google Analytics.
load_dotenv()
tag = os.getenv("GOOGLE_ANALYTICS_TAG")
tracking_code = f"""<!-- Global site tag (gtag.js) - Google Analytics --><script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script><script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{tag}');</script>"""

size_before = os.stat(index_filename).st_size
replace_in_file(index_filename, "<head>", "<head>" + tracking_code)
size_after = os.stat(index_filename).st_size

print("Inserted tracking code into:", index_filename)
print("Size before:", size_before)
print("Size after: ", size_after)

# Insert meta tags for search & social preview.
# Older info but good summary: https://css-tricks.com/essential-meta-tags-social-media/
# 2020 info: https://stackoverflow.com/questions/19778620/provide-an-image-for-whatsapp-link-sharing
META_TAGS = """
<!-- Meta tags for search engines -->
<meta name="description" content="A web app to generate template code for machine learning">
<!-- Meta tags for social preview -->
<meta property="og:title" content="Traingenerator | Template Code for ML">
<meta property="og:description" content="A web app to generate template code for machine learning">
<meta property="og:image" content="https://github.com/jrieke/traingenerator/raw/main/docs/assets/social-preview-tiny.png">
<meta property="og:url" content="https://traingenerator.jrieke.com/">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:site_name" content="Traingenerator">
<meta name="twitter:image:alt" content="Traingenerator Preview">
"""

size_before = os.stat(index_filename).st_size
replace_in_file(index_filename, "<head>", "<head>" + META_TAGS)
size_after = os.stat(index_filename).st_size

print("Inserted meta tags into:", index_filename)
print("Size before:", size_before)
print("Size after: ", size_after)
