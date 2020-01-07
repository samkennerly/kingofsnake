"""
Supervised classification with scikit-learn.
"""
from pandas import Categorical, DataFrame, Series
from sklearn import linear_model

class Classify:

    def __init__(self, clues, answers, model='LogisticRegressionCV', **kwargs):
        answers = Categorical(answers)
        clues = DataFrame(clues)
        model = getattr(linear_model, str(model))

        #kwargs.setdefault('class_weight', 'balanced')
        #kwargs.setdefault('Cs', 10)
        #kwargs.setdefault('fit_intercept', True)
        #kwargs.setdefault('max_iter', 100)
        #kwargs.setdefault('penalty', 'l1')
        #kwargs.setdefault('solver', 'liblinear')
        #kwargs.setdefault('tol', 1e-4)

        self.cats = answers.categories.tolist()
        self.columns = clues.columns.tolist()
        self.model = model(**kwargs).fit(clues, answers.codes)

    def __call__(self, clues):
        cats, model = self.cats, self.model

        clues = DataFrame(clues)
        if hasattr(model, 'predict_proba'):
            data = DataFrame(model.predict_proba(clues), columns=cats)
            data.index = clues.index
        else:
            data = Categorical.from_codes(model.predict(clues), categories=cats)
            data = Series(data, index=clues.index, name='guess')

        return data

    def __repr__(self):
        clsname = type(self).__name__
        modname = type(self.model).__name__
        keyvals = " ".join( f"\n    {k}={v}" for k, v in self.params.items() )

        return f"{clsname}(\n    model={modname}, {keyvals})"

    @property
    def params(self):
        return self.model.get_params()

    @property
    def coefs(self):
        return DataFrame(self.model.coef_, index=self.cats, columns=self.columns)
