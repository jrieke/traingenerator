import streamlit as st


# Define possible models in a dict.
# Format of the dict: model name -> model code
MODELS = {
    "Support vectors": "sklearn.svm.SVC",
    "Random forest": "sklearn.ensemble.RandomForestClassifier",
    "K-nearest neighbors": "sklearn.neighbors.KNeighborsClassifier",
    "Decision tree": "sklearn.tree.DecisionTreeClassifier",
    "Multinomial Naive Bayes": "sklearn.naive_bayes.MultinomialNB",
    "Bernoulli Naive Bayes": "sklearn.naive_bayes.BernoulliNB",
}

VECTORIZERS = {
    "CountVectorizer": "sklearn.feature_extraction.text.CountVectorizer",
    "TfidfVectorizer": "sklearn.feature_extraction.text.TfidfVectorizer",
}


def show():
    """Shows the sidebar components for the template and returns user inputs as dict."""

    inputs = {}

    with st.sidebar:
        st.write("## Model")
        model = st.selectbox("Which model?", list(MODELS.keys()))
        inputs["model_func"] = MODELS[model]

        st.write("## Text normalization")
        inputs["text_normalization"] = st.selectbox(
            "What normalization technique do you want to apply?",
            ("None", "Stemming", "Lemmatization"),
        )
        if inputs["text_normalization"] == "Stemming":
            st.write(
                """
                Stemming is the process of producing morphological variants of a root/base word.
                """
            )
        elif inputs["text_normalization"] == "Lemmatization":
            st.write(
                """
                Lemmatization looks beyond word reduction and considers a language’s full vocabulary to apply a morphological analysis to words.
                """
            )

        st.write("## Vectorizer")
        vectorizer = st.selectbox(
            "What vectorizer do you want to apply?", list(VECTORIZERS.keys())
        )
        inputs["vectorizer"] = VECTORIZERS[vectorizer]

        st.write("## Training")
        st.write("No additional parameters")

        st.write("## Metrics")
        inputs["report"] = st.checkbox(
            "Do you want to compute a classification report?", True
        )

    return inputs


if __name__ == "__main__":
    show()
