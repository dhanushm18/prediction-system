from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the prediction model and scalers
model = pickle.load(open('model.pkl', 'rb'))
mx = pickle.load(open('minmaxscaler.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
dtr = pickle.load(open('dtr.pkl', 'rb'))
preprocessor = pickle.load(open('/Users/dhanushm17/Documents/project/prediction/preprocesser.pkl', 'rb'))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/yield", methods=['POST', 'GET'])
def yields():
    if request.method == 'POST':
        Year = request.form['Year']
        average_rain_fall_mm_per_year = request.form['average_rain_fall_mm_per_year']
        pesticides_tonnes = request.form['pesticides_tonnes']
        avg_temp = request.form['avg_temp']
        Area = request.form['Area']
        Item = request.form['Item']

        features = np.array([[Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item]], dtype=object)
        transformed_features = preprocessor.transform(features)
        prediction = dtr.predict(transformed_features).reshape(1, -1)
        return render_template("yield_res.html", prediction=prediction[0][0])
    return render_template("yield.html")

@app.route("/crop", methods=['POST', 'GET'])  # POST for handling form submission
def crop():
    if request.method == 'POST':
        N = request.form['N']
        P = request.form['P']
        K = request.form['K']
        temp = request.form['temperature']
        humidity = request.form['humidity']
        ph = request.form['ph']
        rainfall = request.form['rainfall']

        # Convert form data to a list of floats
        feature_list = [float(x) for x in [N, P, K, temp, humidity, ph, rainfall]]

        # Reshape the list to a single-row NumPy array
        single_pred = np.array(feature_list).reshape(1, -1)

        # Apply transformations using the loaded scalers
        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)

        # Make prediction using the model
        prediction = model.predict(sc_mx_features)

        # Crop dictionary for mapping prediction to crop names
        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                     8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                     14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                     19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

        # Return the rendered template with the prediction result
        return render_template('crop_result.html', result=result)

    # If the request method is not POST, the route likely serves the form.
    return render_template('predict_crop.html')

if __name__ == "__main__":
    app.run(debug=True)
