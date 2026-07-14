import numpy as np
from sklearn.linear_model import LinearRegression


def predict_temperature(df):

    if len(df) < 5:
        return None

    y = df["temperature"].values

    x = np.arange(len(y)).reshape(-1, 1)

    model = LinearRegression()

    model.fit(x, y)

    prediction = model.predict([[len(y)]])[0]

    return round(prediction, 2)