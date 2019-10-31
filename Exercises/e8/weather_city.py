import sys
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

OUTPUT_TEMPLATE = (
    'Score : {score:.3f}'
)

labelled_data = pd.read_csv(sys.argv[1])
city_labelled_data = labelled_data['city']
del labelled_data['city']
del labelled_data['year']

unlabelled_data = pd.read_csv(sys.argv[2])
del unlabelled_data['city']
del unlabelled_data['year']

X_train, X_valid, y_train, y_valid = train_test_split(labelled_data, city_labelled_data)

model = make_pipeline(StandardScaler(), SVC(kernel='linear', C=0.1))
model.fit(X_train, y_train)
print(OUTPUT_TEMPLATE.format(
        score=model.score(X_valid, y_valid)
    ))

predictions = model.predict(unlabelled_data)
pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)