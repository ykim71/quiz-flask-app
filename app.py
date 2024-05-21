from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import random
import pymysql
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '5dk7dl1flsK!'
app.config['MYSQL_DB'] = 'testdb3'
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
    num_questions=17

    # Pass the num_questions variable to the template
    return render_template('rhetsen.html', questions=questions, num_questions=num_questions)

# Function to generate a unique session ID
def generate_session_id():
    import uuid
    return str(uuid.uuid4())


@app.route('/demo', methods=['POST'])
def demo():
    session['demo_questions'] = demo_questions

    return render_template('demo.html', questions=demo_questions)

@app.route('/submit', methods=['POST'])
def submit():

    Sensitivity_level = 0  
    Assertiveness_level = 0  
    Reflector_level = 0 

    results = []
    selected_questions = session.get('current_questions', [])
    num_questions=17
    passing_level=0
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
    }
}

    cursor = mysql.cursor()
    cursor.execute(
        "INSERT INTO session_info (session_id, page_load_time, submission_time, num_questions, passing_level) VALUES (%s, %s, %s, %s, %s)",
        (session.get('session_id'), session.get('page_load_time'), datetime.now(), num_questions, passing_level)
    )

    for question in selected_questions:
        user_answers = request.form.getlist(question['question'])

        if request.form.get("first_modified_" + str(question['question_id'])) == '':
            first_modified_time = None
        else:
            first_modified_time = request.form.get("first_modified_" + str(question['question_id']))

        if request.form.get("last_modified_" + str(question['question_id'])) == '':
            last_modified_time = None
        else:
            last_modified_time = request.form.get("last_modified_" + str(question['question_id']))

        # Save the quiz log for each selected answer with timestamp
        query = '''INSERT INTO quiz_log (session_id, question_number, question_id, variable_name, question, user_answers, first_modified_time, last_modified_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (session.get('session_id'), question_number, question['question_id'], question['variable_name'], question['question'], '|'.join(user_answers), first_modified_time, last_modified_time))

        results.append({
            'question_id': question['question_id'],
            'question': question['question'],
            'user_answers': user_answers,

        })
        

        if user_answers:
            sensitivity, assertiveness, reflector = question_response_mapping[question_number][user_answers]
            Sensitivity_level += sensitivity
            Assertiveness_level += assertiveness
            Reflector_level += reflector
        
        question_number += 1
            

    # Commit the changes to the database
    mysql.commit()
    cursor.close()

    return render_template('result.html', Sensitivity_level=Sensitivity_level, Assertiveness_level=Assertiveness_level, Reflector_level=Reflector_level, results=results, selected_questions=selected_questions)

if __name__ == '__main__':
    app.run(debug=True)