import streamlit as st


def show():
    """Shows the sidebar components for the template and returns user inputs as dict."""
    
    # `show()` is the only method required in this module. You can add any other code 
    # you like above or below. 
    
    inputs = {}  # dict to store all user inputs until return
    
    with st.sidebar:
        
        # Render all template-specific sidebar components here. 

        # Use ## to denote sections. Common sections for training templates: 
        # Model, Input data, Preprocessing, Training, Visualizations
        st.write("## Model")
        
        # Store all user inputs in the `inputs` dict. This will be passed to the code
        # template later.
        inputs["model"] = st.selectbox("Which model?", ["Top model", "Role model"])
        st.write("You should probably finish this... ;)")
        
    return inputs


# To test the sidebar independent of the app or template, just run 
# `streamlit run sidebar.py` from within this folder.
if __name__ == "__main__":
    show()
    
    