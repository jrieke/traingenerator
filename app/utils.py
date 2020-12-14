import streamlit as st
import pickle
import pandas as pd
import json
import base64
import uuid
import re
import jupytext
from bokeh.models.widgets import Div
import math


def notebook_header(text):
    """
    Insert section header into a jinja file, formatted as notebook cell.
    
    Leave 2 blank lines before the header.
    """
    return f"""# # {text}

"""


def code_header(text):
    """
    Insert section header into a jinja file, formatted as Python comment.
    
    Leave 2 blank lines before the header.
    """
    seperator_len = (75 - len(text)) / 2
    seperator_len_left = math.floor(seperator_len)
    seperator_len_right = math.ceil(seperator_len)
    return f"# {'-' * seperator_len_left} {text} {'-' * seperator_len_right}"


def to_notebook(code):
    """Converts Python code to Jupyter notebook format."""
    notebook = jupytext.reads(code, fmt="py")
    return jupytext.writes(notebook, fmt="ipynb")


def open_link(url, new_tab=True):
    """Dirty hack to open a new web page with a streamlit button."""
    # From: https://discuss.streamlit.io/t/how-to-link-a-button-to-a-webpage/1661/3
    if new_tab:
        js = f"window.open('{url}')"  # New tab or window
    else:
        js = f"window.location.href = '{url}'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)


def download_button(
    object_to_download, download_filename, button_text  # , pickle_it=False
):
    """
    Generates a link to download the given object_to_download.
    
    From: https://discuss.streamlit.io/t/a-download-button-with-custom-css/4220

    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.

    Returns:
    -------
    (str): the anchor tag to download object_to_download

    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')

    """
    # if pickle_it:
    #     try:
    #         object_to_download = pickle.dumps(object_to_download)
    #     except pickle.PicklingError as e:
    #         st.write(e)
    #         return None

    # else:
    #     if isinstance(object_to_download, bytes):
    #         pass

    #     elif isinstance(object_to_download, pd.DataFrame):
    #         object_to_download = object_to_download.to_csv(index=False)

    #     # Try JSON encode for everything else
    #     else:
    #         object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = (
        custom_css
        + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br><br>'
    )
    # dl_link = f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}"><input type="button" kind="primary" value="{button_text}"></a><br></br>'

    st.markdown(dl_link, unsafe_allow_html=True)


# def download_link(
#     content, label="Download", filename="file.txt", mimetype="text/plain"
# ):
#     """Create a HTML link to download a string as a file."""
#     # From: https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/9
#     b64 = base64.b64encode(
#         content.encode()
#     ).decode()  # some strings <-> bytes conversions necessary here
#     href = (
#         f'<a href="data:{mimetype};base64,{b64}" download="{filename}">{label}</a>'
#     )
#     return href

