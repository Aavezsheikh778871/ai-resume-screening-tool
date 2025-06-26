from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd

def get_skill_distribution(texts, labels):
    """Return skill frequency vectors for radar chart"""
    vectorizer = CountVectorizer(max_features=10, stop_words='english')
    vectors = vectorizer.fit_transform(texts).toarray()
    feature_names = vectorizer.get_feature_names_out()

    df = pd.DataFrame(vectors, columns=feature_names)
    df["Label"] = labels
    return df.set_index("Label")

