import pickle
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="*")


def load_vectorizer():
    return pickle.load(open('vectorizer.pkl', 'rb'))


def load_model():
    return pickle.load(open('model.pkl', 'rb'))


def get_categories_dict():
    return {
        0: {
            'hebrew': 'ספורט',
            'english': 'Sport'
        },
        1: {
            'hebrew': 'תרבות',
            'english': 'Entertainment'
        },
        2: {
            'hebrew': 'כלכלה',
            'english': 'Economy'
        },
        3: {
            'hebrew': 'בריאות',
            'english': 'Health'
        },
        4: {
            'hebrew': 'רכב',
            'english': 'Car'
        },
        5: {
            'hebrew': 'אוכל',
            'english': 'Food'
        },
        6: {
            'hebrew': 'יחסים',
            'english': 'Dating'
        },
        7: {
            'hebrew': 'הורים',
            'english': 'Parents'
        }
    }


def get_vectorized_text(text):
    return vectorizer.transform([text])


def get_model_prediction_probabilities(vectorized_text):
    categories_dict = get_categories_dict()

    prediction_probabilities = model.predict_proba(vectorized_text)[0]

    for i in range(len(prediction_probabilities)):
        confidence_percentage = prediction_probabilities[i]
        categories_dict[i]['confidence_percentage'] = confidence_percentage

    return categories_dict


def get_category(prediction):
    categories_dict = get_categories_dict()
    return categories_dict[prediction[0]]


@app.route("/predict", methods=['POST'])
def predict():
    text = request.get_json()['text']
    vectorized_text = get_vectorized_text(text)
    prediction_probabilities = get_model_prediction_probabilities(vectorized_text)
    return prediction_probabilities

model = load_model()
vectorizer = load_vectorizer()

if __name__ == "__main__":
    app.run(port=5000)
