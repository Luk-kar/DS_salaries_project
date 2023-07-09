from flask import Flask, jsonify, request
import pickle
import numpy as np

app = Flask(__name__)


def load_models():
    file_name = "models/model_file.p"
    with open(file_name, "rb") as pickled:
        data = pickle.load(pickled)
        model = data["model"]
    return model


@app.route("/predict", methods=["GET"])
def predict():
    if request.method == "GET" and request.is_json:
        input_data = request.get_json().get("input")
        data_reshaped = np.array(input_data).reshape(1, -1)
        model = load_models()
        salary = model.predict(data_reshaped)[0]

        prediction = round(salary)
        html_code = 200

    else:
        prediction = "invalid input"
        html_code = 400

    response = jsonify({"salary_predicted": prediction, "currency": "USD"})
    response.headers.add("Content-Type", "application/json")
    return response, html_code


if __name__ == "__main__":
    app.run()
