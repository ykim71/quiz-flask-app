from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import random
import pymysql
from datetime import datetime
import os
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the MySQL database connection
app.config['MYSQL_HOST'] = 'database-rhetsen.c1eie2062f9x.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = 'quiz_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Create a MySQL database connection
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)

# Load questions from JSON file
with open('questions_rhetsen.json', 'r') as file:
    questions = json.load(file)

with open('questions_demo.json', 'r') as file:
    demo_questions = json.load(file)
    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rhetsen')
def rhetsen():
    session['current_questions'] = questions
    session['session_id'] = generate_session_id()  # Generate a session ID
    session['page_load_time'] = datetime.now()  # Store the page load time

    session['demo_questions'] = demo_questions


    # Pass the num_questions variable to the template
    return render_template('rhetsen.html', questions=questions, demo_questions=demo_questions)

# Function to generate a unique session ID
def generate_session_id():
    import uuid
    return str(uuid.uuid4())


@app.route('/submit', methods=['POST'])
def submit():

    Sensitivity_level = 0  
    Assertiveness_level = 0  
    Reflector_level = 0 

    results = []
    questions = session.get('current_questions', [])
    demo_questions = session.get('demo_questions', [])

    question_number = 1

    question_response_mapping = {
    1: {  # A01Frank
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    },
    2: {  # A05Sleep
        "Almost never true": (0, 2, 0),
        "Rarely true": (1, 1, 0),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 0, 1),
        "Almost always true": (0, 0, 2),
    },
    3: {  # A07Hide
        "Almost never true": (0, 2, 0),
        "Rarely true": (1, 1, 0),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 0, 1),
        "Almost always true": (0, 0, 2),
    },
    4: {  # A13Tell
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    },
    5: {  # A15Mistake
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    },   
    6: {  # A16First
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    },  
    7: {  # A17Want
        "Almost never true": (0, 2, 0),
        "Rarely true": (1, 1, 0),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 0, 1),
        "Almost always true": (0, 0, 2),
    },    
    8: {  # A20Habit
        "Almost never true": (0, 2, 2),
        "Rarely true": (1, 1, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 0, 0),
        "Almost always true": (0, 0, 0),
    },  
    9: {  # A21Adjust
        "Almost never true": (0, 2, 0),
        "Rarely true": (1, 1, 0),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 0, 1),
        "Almost always true": (0, 0, 2),
    }, 
    10: {  # A25Words
        "Almost never true": (0, 0, 0),
        "Rarely true": (1, 0, 0),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 1),
        "Almost always true": (0, 2, 2),
    }, 
    11: {  # A26Breath
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    }, 
    12: {  # A28Open
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    }, 
    13: {  # A30Embarrass
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    }, 
    14: {  # A31Voice
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    }, 
    15: {  # A33Advice
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    }, 
    16: {  # A34Friendship
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    }, 
    17: {  # A38Bush
        "Almost never true": (0, 0, 2),
        "Rarely true": (1, 0, 1),
        "Sometimes true": (2, 0, 0),
        "Often true": (1, 1, 0),
        "Almost always true": (0, 2, 0),
    } }

    demo_answers = []
    for demo_question in demo_questions:
        question_id = demo_question['question_id']
        demo_answers.append(request.form.getlist(str(question_id)))

    cursor = mysql.cursor()
    cursor.execute(
        "INSERT INTO session_info (session_id, page_load_time, submission_time, gender, education, age, religion, political_ideology, occupation, household_income, relationship, news_use, social_media_use) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (session.get('session_id'), session.get('page_load_time'), datetime.now(), demo_answers[0], demo_answers[1], demo_answers[2], demo_answers[3], demo_answers[4],demo_answers[5],demo_answers[6],demo_answers[7], demo_answers[8], demo_answers[9])
    )

    for question in questions:
        question_id = question['question_id']
        user_answers = request.form.getlist(str(question_id))
        answer_string = '|'.join(user_answers) if user_answers else ''

        # Save the quiz log for each selected answer with timestamp
        query = '''INSERT INTO quiz_log (session_id, question_number, question_id, variable_name, question, answer_string) VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (session.get('session_id'), question_number, question['question_id'], question['variable_name'], question['question'], answer_string))

        results.append({
            'question_id': question['question_id'],
            'question': question['question'],
            'user_answers': answer_string

        })
        

        if user_answers:
            sensitivity, assertiveness, reflector = question_response_mapping[question_number][answer_string]
            Sensitivity_level += sensitivity
            Assertiveness_level += assertiveness
            Reflector_level += reflector
        
        question_number += 1
            

    # Commit the changes to the database
    mysql.commit()
    cursor.close()

    return render_template('result.html', Sensitivity_level=Sensitivity_level, Assertiveness_level=Assertiveness_level, Reflector_level=Reflector_level, results=results)

if __name__ == '__main__':
    app.run(debug=True)