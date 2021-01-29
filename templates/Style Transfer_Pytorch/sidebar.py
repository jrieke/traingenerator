import streamlit as st

MODELS = {
     "VGG": {
        "VGG11": "vgg11",
        "VGG11 with batch normalization": "vgg11_bn",
        "VGG13": "vgg13",
        "VGG13 with batch normalization": "vgg13_bn",
        "VGG16": "vgg16",
        "VGG16 with batch normalization": "vgg16_bn",
        "VGG19": "vgg19",
        "VGG19 with batch normalization": "vgg19_bn",
    },
}


# Define possible optimizers in a dict.
# Format: optimizer -> default learning rate
OPTIMIZERS = {
    "Adam": 0.001,
    "Adadelta": 1.0,
    "Adagrad": 0.01,
    "Adamax": 0.002,
    "RMSprop": 0.01,
    "SGD": 0.1,
}



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
        inputs["model"] = st.selectbox("Which model?", list(MODELS.keys()))
        
        
        inputs["pretrained"] = st.checkbox("Use pre-trained model (Suggested Use is with a pretrained model)")
        
        st.write("## Input data")
        inputs["data_format"] = st.selectbox(
            "Which data do you want to use?",
            ("Public Image File", "Custom Image files"),
        )
        
        if input["data_format"]== "Public Image File":
          st.write("""
          ```
          It's a public image so you won't have to do anything.
          ```
          """)
        
        elif input["data_format"]== "Custom Image File":
          st.write("""
          ```
          Make sure you have two files the content image and the sytle image.
          ```
          """) 
        
        inputs["loss"] = st.selectbox(
            "Loss function", ("Mean Squared Error Loss")
        )
        
        inputs["optimizer"] = st.selectbox("Optimizer", list(OPTIMIZERS.keys()))
        
        default_lr = OPTIMIZERS[inputs["optimizer"]]
        inputs["lr"] = st.number_input(
            "Learning rate", 0.000, None, default_lr, format="%f"
        )
        
        inputs["num_epochs"] = st.number_input("Epochs", 1, None, 5)
               
        
    return inputs


# To test the sidebar independent of the app or template, just run 
# `streamlit run sidebar.py` from within this folder.
if __name__ == "__main__":
    show()
