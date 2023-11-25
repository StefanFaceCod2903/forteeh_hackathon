from flask import Flask, render_template, session, request
from flask_session import Session
from flask_cors import CORS


from utils import generateQuiz, getCorrectAnswers, calculate_score

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Save the uploaded file to a desired location
    file.save('uploads/' + file.filename)

    return render_template("uploadSuccess.html") 

@app.route("/quiz")
def quiz():

    questions = generateQuiz()
    #questions = read_json_file('example.json')
    session['correctAnswers'] = getCorrectAnswers(questions=questions)
    return render_template("quiz.html", questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = []

    correctAnswersArray = session['correctAnswers'].split(',')
    for index, answer in enumerate(correctAnswersArray):
        user_answers.append(request.form[str(index)])

    # Now you can check user answers against correct answers
    score = calculate_score(user_answers, correctAnswersArray)
    
    return render_template("results.html", user_answers=user_answers, correctAnswersArray=correctAnswersArray, score=score)
