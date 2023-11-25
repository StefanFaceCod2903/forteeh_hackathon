from openai import OpenAI
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Accessing environment variables
api_key = os.environ.get('API_KEY')

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError:
        return {}  # Return an empty dictionary for file not found
    except json.JSONDecodeError as e:
        return {}  # Return an empty dictionary for JSON decoding error
    except Exception as e:
        return {}  # Return an empty dictionary for other errors


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generateQuiz():

    client = OpenAI(
    api_key=api_key,
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are trying to help a teacher to make quizes for his students. All your answers must be valid json. You will recieve questions in english but the text and the questions should be in roumanian."},
        {"role": "user", 
        "content": 
            "Give me based on the following text 3 questions. Each question should have between 4 possible answers where only one is correct. The answer to this prompt should be a json array, each object of the array should be of the following format : {question: "",answers: {'A' :'B' :},correctAnswer: 'letter corresponding to the correct answer'}. The text you should base the questions on is:" + read_file("uploads/text.txt")}
    ]
    )
    return json.loads(completion.choices[0].message.content)

def getCorrectAnswers(questions):
    return ",".join([x['correctAnswer'] for x in questions])

def calculate_score(user_answers, correct_answers):
    # Example: Calculate the score based on correct answers
    score = 0
    for index, answer in enumerate(user_answers):
        if answer == correct_answers[index]:
            score += 1
    return score