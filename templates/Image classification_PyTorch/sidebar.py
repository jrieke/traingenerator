import streamlit as st


# Define possible models in a dict.
# Format of the dict:
# option 1: model -> code
# option 2 – if model has multiple variants: model -> model variant -> code
MODELS = {
    "AlexNet": "alexnet",  # single model variant
    "ResNet": {  # multiple model variants
        "ResNet 18": "resnet18",
        "ResNet 34": "resnet34",
        "ResNet 50": "resnet50",
        "ResNet 101": "resnet101",
        "ResNet 152": "resnet152",
    },
    "DenseNet": {
        "DenseNet-121": "densenet121",
        "DenseNet-161": "densenet161",
        "DenseNet-169": "densenet169",
        "DenseNet-201": "densenet201",
    },
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

    inputs = {}

    with st.sidebar:
        st.write("## Model")
        model = st.selectbox("Which model?", list(MODELS.keys()))

        # Show model variants if model has multiple ones.
        if isinstance(MODELS[model], dict):  # different model variants
            model_variant = st.selectbox("Which variant?", list(MODELS[model].keys()))
            inputs["model_func"] = MODELS[model][model_variant]
        else:  # only one variant
            inputs["model_func"] = MODELS[model]

        inputs["num_classes"] = st.number_input(
            "How many classes/output units?", 1, None, 1000,
        )
        st.markdown(
            "<sup>Default: 1000 classes for training on ImageNet</sup>",
            unsafe_allow_html=True,
        )

        inputs["pretrained"] = st.checkbox("Use pre-trained model")
        if inputs["pretrained"]:
            if inputs["num_classes"] != 1000:
                classes_note = "<br><b>Note: Final layer will not be trained if using more/less than 1000 classes!</b>"
            else:
                classes_note = ""
            st.markdown(
                f'<sup>Pre-training on ImageNet, <a href="https://pytorch.org/docs/stable/torchvision/models.html">details</a>{classes_note}</sup>',
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
                "Which one?", ("MNIST", "FashionMNIST", "CIFAR10")
            )

        st.write("## Preprocessing")
        # st.checkbox("Convert to grayscale")
        # st.checkbox("Convert to RGB", True)
        # TODO: Maybe show disabled checkbox here to make it more aligned with the
        #   display above.
        # st.markdown(
        #     '<label data-baseweb="checkbox" class="st-eb st-b4 st-ec st-d4 st-ed st-at st-as st-ee st-e5 st-av st-aw st-ay st-ax"><span role="checkbox" aria-checked="true" class="st-eg st-b2 st-bo st-eh st-ei st-ej st-ek st-el st-bb st-bj st-bk st-bl st-bm st-em st-en st-eo st-ep st-eq st-er st-es st-et st-av st-aw st-ax st-ay st-eu st-cb st-ev st-ew st-ex st-ey st-ez st-f0 st-f1 st-f2 st-c5 st-f3 st-f4 st-f5" style="background-color: rgb(150, 150, 150);"></span><input aria-checked="true" type="checkbox" class="st-b0 st-an st-cv st-bd st-di st-f6 st-cr" value=""><div class="st-ev st-f7 st-bp st-ae st-af st-ag st-f8 st-ai st-aj">sdf</div></label>',
        #     unsafe_allow_html=True,
        # )
        st.write("Resize images to 256 (required for this model)")
        st.write("Center-crop images to 224 (required for this model)")
        if inputs["pretrained"]:
            st.write("Scale mean and std for pre-trained model")

        st.write("## Training")
        inputs["gpu"] = st.checkbox("Use GPU if available", True)
        inputs["checkpoint"] = st.checkbox("Save model checkpoint each epoch")
        if inputs["checkpoint"]:
            st.markdown(
                "<sup>Checkpoints are saved to timestamped dir in `./checkpoints`. They may consume a lot of storage!</sup>",
                unsafe_allow_html=True,
            )
        inputs["loss"] = st.selectbox(
            "Loss function", ("CrossEntropyLoss", "BCEWithLogitsLoss")
        )
        inputs["optimizer"] = st.selectbox("Optimizer", list(OPTIMIZERS.keys()))
        default_lr = OPTIMIZERS[inputs["optimizer"]]
        inputs["lr"] = st.number_input(
            "Learning rate", 0.000, None, default_lr, format="%f"
        )
        inputs["batch_size"] = st.number_input("Batch size", 1, None, 128)
        inputs["num_epochs"] = st.number_input("Epochs", 1, None, 3)
        inputs["print_every"] = st.number_input(
            "Print progress every ... batches", 1, None, 1
        )

        st.write("## Visualizations")
        inputs["visualization_tool"] = st.selectbox(
            "How to log metrics?",
            ("Not at all", "Tensorboard", "Aim", "Weights & Biases", "comet.ml"),
        )
        if inputs["visualization_tool"] == "Aim":
            inputs["aim_experiment"] = st.text_input("Experiment name (optional)")
            st.markdown(
                '<sup>View by running: `aim up`</br>See full documentation <a href="https://github.com/aimhubio/aim#contents" target="_blank">here</a></sup>',
                unsafe_allow_html=True,
            )
        elif inputs["visualization_tool"] == "Weights & Biases":
            inputs["wb_project"] = st.text_input("W&B project name (optional)")
            inputs["wb_name"] = st.text_input("W&B experiment name (optional)")
        elif inputs["visualization_tool"] == "comet.ml":
            # TODO: Add a tracker how many people click on this link.
            "[Sign up for comet.ml](https://www.comet.ml/) :comet: "
            inputs["comet_api_key"] = st.text_input("Comet API key (required)")
            inputs["comet_project"] = st.text_input("Comet project name (optional)")
        elif inputs["visualization_tool"] == "Tensorboard":
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
