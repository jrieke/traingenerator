import streamlit as st


# Define possible models in a dict.
# Format of the dict:
# option 1: model -> code
# option 2 – if model has multiple variants: model -> model variant -> code
MODELS = {
    "ResNet": {  # multiple model variants
        "ResNet 50": "ResNet50",
        "ResNet 101": "ResNet101",
        "ResNet 152": "ResNet152",
    }, 
    "ResNet_V2": {
        "ResNet 50v2": "ResNet50V2",
        "ResNet 101v2": "ResNet101V2",
        "ResNet 152v2": "ResNet152V2",
    },
    "Xception": "Xception",  # single model variant
    "DenseNet": {
        "DenseNet 121": "DenseNet121",
        "DenseNet 169": "DenseNet169",
        "DenseNet 201": "DenseNet201",
    },
    "EfficientNet": {
        "EfficientNet B0": "EfficientNetB0",
        "EfficientNet B1": "EfficientNetB1",
        "EfficientNet B2": "EfficientNetB2",
        "EfficientNet B3": "EfficientNetB3",
        "EfficientNet B4": "EfficientNetB4",
        "EfficientNet B5": "EfficientNetB5",
        "EfficientNet B6": "EfficientNetB6",
        "EfficientNet B7": "EfficientNetB7",
    },
    
    "Inception_ResNet_V2": "InceptionResNetV2",
    "Inception_V3": "InceptionV3",
    
    "VGG16": "VGG16",
    "VGG19": "vgg19",
    
    "MobileNet": "MobileNet",
    "MobileNet_V2": "MobileNetV2",

    "MobileNet_V3": {
        "MobileNet V3Large": "MobileNetV3Large",
        "MobileNet V3Small": "MobileNetV3Small",
    },
    "NASNet": {
        "NASNet Large": "NASNetLarge",
        "NASNet Mobile": "NASNetMobile",
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

    inputs = {}

    with st.sidebar:
        st.write("## Model")
        model = st.selectbox("Which model?", list(MODELS.keys()))

        # Show model variants if model has multiple ones.
        if isinstance(MODELS[model], dict):  # different model variants
            model_variant = st.selectbox("Which variant?", list(MODELS[model].keys()))
            inputs["model_func"] = MODELS[model][model_variant]
            inputs["model_pre"] = model.lower()  # Model Preprocessing
        else:  # only one variant
            inputs["model_func"] = MODELS[model]
            inputs["model_pre"] = model.lower()

        inputs["num_classes"] = st.number_input(
            "How many classes/output units?",
            1,
            None,
            1000,
        )
        st.markdown(
            "<sup>Default: 1000 classes for training on ImageNet</sup>",
            unsafe_allow_html=True,
        )

        inputs["pretrained"] = st.checkbox("Use pre-trained model")
        if inputs["pretrained"]:
            inputs["pretrained"] = "imagenet"
            if inputs["num_classes"] != 1000:
                classes_note = "<br><b>Note: Final layer will not be trained if using more/less than 1000 classes!</b>"
            else:
                classes_note = ""
            st.markdown(
                f'<sup>Pre-training on ImageNet with 1k classes, <a href="https://www.tensorflow.org/api_docs/python/tf/keras/applications">details</a>{classes_note}</sup>',
                unsafe_allow_html=True,
            )

        st.write("## Input data")
        inputs["data_format"] = st.selectbox(
            "Which data do you want to use?",
            ("Public dataset", "Numpy arrays", "Image files"),
        )
        if inputs["data_format"] == "Numpy arrays":
            st.write(
                """
            Expected format: `[images, labels]`
            - `images` has array shape (num samples, color channels, height, width)
            - `labels` has array shape (num samples, )
            """
            )
        elif inputs["data_format"] == "Image files":
            st.write(
                """
            Expected format: One folder per class, e.g.
            ```
            train
            +-- dogs
            |   +-- lassie.jpg
            |   +-- komissar-rex.png
            +-- cats
            |   +-- garfield.png
            |   +-- smelly-cat.png
            ```
            
            See also [this example dir](https://github.com/jrieke/traingenerator/tree/main/data/image-data)
            """
            )
        elif inputs["data_format"] == "Public dataset":
            inputs["dataset"] = st.selectbox(
                "Which one?", ("mnist", "fashion_mnist", "cifar10")
            )

        st.write("## Training")
        # inputs["gpu"] = st.checkbox("Use GPU if available", True)
        inputs["checkpoint"] = st.checkbox("Save model checkpoint each epoch")
        if inputs["checkpoint"]:
            st.markdown(
                "<sup>Checkpoints are saved to timestamped dir in `./checkpoints`. They may consume a lot of storage!</sup>",
                unsafe_allow_html=True,
            )
        inputs["loss"] = st.selectbox(
            "Loss function", ("sparse_categorical_crossentropy", "binary_crossentropy")
        )
        inputs["optimizer"] = st.selectbox("Optimizer", list(OPTIMIZERS.keys()))
        default_lr = OPTIMIZERS[inputs["optimizer"]]
        inputs["lr"] = st.number_input(
            "Learning rate", 0.000, None, default_lr, format="%f"
        )
        inputs["batch_size"] = st.number_input("Batch size", 1, None, 128)
        inputs["num_epochs"] = st.number_input("Epochs", 1, None, 3)

        st.write("## Visualizations")
        inputs["visualization_tool"] = st.selectbox(
            "How to log metrics?", ("Not at all", "Tensorboard")
        )
        if inputs["visualization_tool"] == "Tensorboard":
            st.markdown(
                "<sup>Logs are saved to timestamped dir in `./logs`. View by running: `tensorboard --logdir=./logs`</sup>",
                unsafe_allow_html=True,
            )

    # "Which plots do you want to add?"
    # # TODO: Show some examples.
    # st.checkbox("Sample images", True)
    # st.checkbox("Confusion matrix", True)

    # "## Saving"
    # st.checkbox("Save config file", True)
    # st.checkbox("Save console output", True)
    # st.checkbox("Save finished model", True)
    # if model in TORCH_MODELS:
    #     st.checkbox("Save checkpoint after each epoch", True)

    return inputs


if __name__ == "__main__":
    show()
