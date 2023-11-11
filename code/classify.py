from pandas import Categorical, DataFrame, Series, crosstab
from sklearn import linear_model


class Classifier:
    """
    Use a scikit-learn classifier with pandas DataFrames.
    Input training data to create and train a model.
    Call with new feature data to predict classes.
    Output is a Series with datatype 'category'.

    Constructor inputs:
        data    DataFrame: observations to use for training
        target  string: name of column to predict
        model   optional str: name of an sklearn.linear_model
        kwargs  are passed to the selected sklearn.linear_model

    Call inputs:
        data    DataFrame: features to use for prediction
    """

    def __init__(self, data, target, model="LogisticRegression", **kwargs):
        model = getattr(linear_model, str(model))
        feats = data.drop(columns=target)
        cats = Categorical(data[target])

        self.classes = cats.categories.tolist()
        self.features = feats.columns.tolist()
        self.target = target
        self.model = model(**kwargs).fit(feats, cats.codes)

    def __call__(self, data):
        classes = self.classes
        features = self.features
        model = self.model

        cats = model.predict(data[features])
        cats = Categorical.from_codes(cats, categories=classes)
        cats = Series(cats, index=data.index, name="predicted")

        return cats

    def __repr__(self):
        return f"{type(self).__name__}({type(self.model).__name__})"

    @property
    def coefs(self):
        """DataFrame: Model coefficients."""
        return DataFrame(self.model.coef_, index=self.classes, columns=self.features)

    @property
    def params(self):
        """dict: Model parameters."""
        return self.model.get_params()

    def confusion(self, data):
        """
        DataFrame: Confusion matrix of correct and wrong prediction counts.
        Rows are true classes. Columns are predicted classes.

        Inputs:
            data    DataFrame: observations to use for testing
        """
        return crosstab(data[self.target], self(data))

    def probs(self, data):
        """DataFrame: Predicted class probabilities for each row in data."""
        classes = self.classes
        features = self.features
        model = self.model

        if not hasattr(model, "predict_proba"):
            msg = f"{type(model).__name__} cannot predict probabilities"
            raise NotImplementedError(msg)

        probs = model.predict_proba(data[features])
        probs = DataFrame(probs, columns=classes, index=data.index)

        return probs
