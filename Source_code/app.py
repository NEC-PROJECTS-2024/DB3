# import libraires
import pickle
import numpy as np
from flask import Flask , render_template , request

#load model
model = pickle.load(open('mymodel.pkl', "rb"))

#flask consructor
app = Flask(__name__)

def generate_fitness_suggestions(age, gender, heart_rate):
    suggestions = []

    # Example fitness suggestions based on age
    if age < 18:
        suggestions.append("Consider age-appropriate activities and sports.")
    elif 18 <= age <= 30:
        suggestions.append("Include both cardio and strength training in your routine.")
    elif 31 <= age <= 50:
        suggestions.append("Focus on maintaining a balanced workout routine for overall health.")
    else:
        suggestions.append("Consult with a fitness professional for personalized advice.")

    # Example fitness suggestions based on gender
    if gender == 'Male':
        suggestions.append("Incorporate strength training to build muscle.")
    else:
        suggestions.append("Include weight-bearing exercises for bone health.")

    # Example fitness suggestions based on heart rate
    if heart_rate > 160:
        suggestions.append("Ensure you are not overexerting yourself; consider lowering intensity.")
    elif heart_rate < 100:
        suggestions.append("Consider increasing the intensity of your workouts for better cardiovascular benefits.")

    return suggestions

# Function to generate fitness exercises based on user attributes
def generate_fitness_exercises(age, gender, heart_rate):
    exercises = []

    # Example fitness exercises based on age
    if age < 18:
        exercises.append("Swimming")
        exercises.append("Cycling")
    elif 18 <= age <= 30:
        exercises.append("Running")
        exercises.append("Weightlifting")
    elif 31 <= age <= 50:
        exercises.append("Yoga")
        exercises.append("Pilates")
    else:
        exercises.append("Walking")
        exercises.append("Gentle stretching")

    # Example fitness exercises based on gender
    if gender == 'Male':
        exercises.append("Bench Press")
        exercises.append("Deadlifts")
    else:
        exercises.append("Leg Press")
        exercises.append("Yoga or Pilates")

    # Example fitness exercises based on heart rate
    if heart_rate > 160:
        exercises.append("High-Intensity Interval Training (HIIT)")
    elif heart_rate < 100:
        exercises.append("Aerobic Exercises")
        exercises.append("Brisk Walking")

    return exercises


@app.route('/')

@app.route('/main_template',methods=["GET"])
def main_template():

    #render form
    return render_template('index.html')

#get form data
@app.route('/predict',methods=['GET','POST'])
def predict():

    #checking request type
    str_req_type = request.method

    #convert string value into numeric value
    if request.method == str(str_req_type):

        if request.args.get('gender') == 'Male':
            gender = 1

        else:
            gender = 0

        age = int(request.args.get('age'))

        duration = request.args.get('duration')

        heart_Rate = int(request.args.get('heart_rate'))

        temp = request.args.get('temp')

        height = request.args.get('height')

        weight = request.args.get('weight')

        #store form values into set
        values = [float(gender), float(age), float(height), float(weight), float(duration), float(heart_Rate), float(temp)]

        #turn into array & reshape array for prediction
        input_array = np.asarray(values)
        input_array_reshape = input_array.reshape(1, -1)

        suggestions = generate_fitness_suggestions(age, gender, heart_Rate)
        exercises = generate_fitness_exercises(age, gender, heart_Rate)

        # predict with inputed values
        predicted = model.predict(input_array_reshape)

        #display predicted valuesin result.html file
        return  render_template('result.html', predicted_value=predicted[0] ,suggestions=suggestions, exercises=exercises)

    else:

        return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)