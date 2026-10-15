import os
import psycopg2
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT")
    )

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'Message': 'Welcome to my API test!'})

students = [
    {'id':1, 'name':'Mary'},
    {'id':2, 'name':'John'},
    {'id':3, 'name':'Bob'},
    {'id':4, 'name':'Alice'},
    {'id':5, 'name':'David'},
    {'id':6, 'name':'Charlie'},
    {'id':7, 'name':'Eve'},
    {'id':8, 'name':'Frank'},
    {'id':9, 'name':'George'},
    {'id':10, 'name':'Allan'},
    {'id':11, 'name':'Lílian'}
]
@app.route("/students", methods=['GET'])
def showStudents():
    return jsonify({'students':students})

@app.route("/students", methods=['POST'])
def add_students():
    new_student = request.json
    students.append(new_student)
    return jsonify({'Message': 'Student added', 'Student': new_student})


@app.route("/students/<int:id>", methods=['PUT'])
def update_students(id):
    for student in students:
        if student['id'] == id:
            student.update(request.json)
            return jsonify({'Message': 'Student updated', 'Student': student})
    return jsonify({'Error': 'Student not found'}), 404

@app.route("/students/<int:id>", methods=['DELETE'])
def delete_students(id):
    for student in students:
        if student['id'] == id:
            students.remove(student)
            return jsonify({'Message': 'Student deleted', 'Student': student})
    return jsonify({'Erro': 'Student not found'}), 404

@app.route("/people", methods=['GET'])
def show_people():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM people ORDER BY id ASC ")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    people_list = []
    for row in rows:
        people_list.append({
            'id': row[0],
            'name': row[1],
            "age": row[2],
        })

    return jsonify({'People': people_list})


@app.route("/people", methods=['POST'])
def add_people():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    if not name or name.strip() == "":
        return jsonify({
            "Error": "Name is required"
        }), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO people (name, age) VALUES (%s, %s) RETURNING id, name, age",
            (name, age)
        )
        new_dados_people = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({
            "Error": str(e)
        }), 500

    return jsonify({
        "Message": "Person added",
        "Person": {
            "id":new_dados_people[0],
            "name":new_dados_people[1],
            "age":new_dados_people[2]
        }
    })

@app.route("/people/<int:id>", methods = ['PUT'])
def update_people(id):
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE people SET name=%s, age=%s WHERE id=%s RETURNING id, name,age",
        (name,age, id)
    )
    update = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if update:
        return jsonify({
            "Message": "Person updated",
            "Person": {
                "id":update[0],
                "name":update[1],
                "age":update[2]
            }
        })
    else:
        return jsonify({ "Error": "Person not found" }), 404

@app.route("/people/<int:id>", methods = ['DELETE'])
def delete_people(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute( "DELETE FROM people WHERE id=%s RETURNING id, name, age",(id,))
    delete = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if delete:
        return jsonify({
            "Message": "Person deleted",
            "Person": {
                "id":delete[0],
                "name":delete[1],
                "age":delete[2]
            }
        })
    else:
        return jsonify({ "Error": "Person not found" }), 404

@app.route("/professor", methods=['GET'])
def showProfessor():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM professor ORDER BY professor.name ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    professor_list = []
    for row in rows:
        professor_list.append({
            "professor_id": row[0],
            "professor_name": row[1]

        })

    return jsonify({'Professor': professor_list})

@app.route("/professor", methods=['POST'])
def add_professor():
    data = request.get_json()
    name = data.get("name")

    if not name or name.strip() == "":
        return jsonify({
            "Error": "Name is required"
        }), 400
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO professor(name) VALUES (%s) RETURNING id, name",(name,))

        new_professor = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({
            "Error": str(e)
        }), 500

    return jsonify({
        "Message": "Professor added",
        "Professor": {
            "id":new_professor[0],
            "name":new_professor[1]
        }
    })

@app.route("/professor/<int:id>", methods = ['PUT'])
def update_professor(id):
    data = request.get_json()
    name = data.get("name")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE professor SET name=%s WHERE id=%s RETURNING id,name",(name, id))
    update = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if update:
        return jsonify({
            "Message": "Professor updated",
            "Professor": {
                "id":update[0],
                "name":update[1],
            }
        })
    else:
        return jsonify({ "Error": "Professor not found" }), 404

@app.route("/professor/<int:id>", methods = ['DELETE'])
def delete_professor(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM professor WHERE id=%s RETURNING id, name",(id,))
    delete_prof = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if delete_prof:
        return jsonify({
            "Message": "Professor deleted",
            "Professor": {
                "id":delete_prof[0],
                "name":delete_prof[1]
            }
        })
    else:
        return jsonify({ "Error": "Professor not found" }), 404

@app.route("/discipline", methods=['GET'])
def show_disciplines():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM discipline ORDER BY discipline.name ASC")
    rows = cur.fetchall()
    cur.close()
    discipline_list = []
    for row in rows:
        discipline_list.append({
            "discipline_id": row[0],
            "discipline_name": row[1],
            "discipline_professor_id": row[2]

        })

    return jsonify({'Disciplines': discipline_list})

@app.route("/discipline", methods=['POST'])
def add_discipline():
    data = request.get_json()
    name = data.get("discipline_name")
    professor_id = data.get("professor_id")

    if not name or name.strip() == "":
        return jsonify({ "Error": "Discipline name is required" }), 400
    if not professor_id or professor_id == "":
        return jsonify({ "Error": "Professor_id is required" }), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO discipline(name,professor_id) VALUES ( %s, %s) RETURNING id,name,professor_id",(name, professor_id))
    new_discipline = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "Message": "Discipline added",
        "Discipline": {
            "discipline_id": new_discipline[0],
            "discipline_name": new_discipline[1],
            "professor_id": new_discipline[2]

        }
    })


@app.route("/discipline/<int:id>", methods = ['PUT'])
def update_discipline(id):
    data = request.get_json()
    name = data.get("discipline_name")
    professor_id = data.get("professor_id")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE discipline SET name=%s, professor_id=%s WHERE id=%s RETURNING id,name, professor_id",(name,professor_id,id))

    update_disc = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if update_disc:
        return jsonify({
            "Message": "Discipline updated",
            "Discipline": {
                "Discipline_id":update_disc[0],
                "discipline_name":update_disc[1],
                "professor_id":update_disc[2]

            }
        })

    else:
        return jsonify({ "Error": "Discipline not found" }), 404


@app.route("/discipline/<int:id>", methods = ['DELETE'])
def delete_discipline(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM discipline WHERE id=%s RETURNING id, name",(id,))
    conn.commit()
    delete_disc = cur.fetchone()
    cur.close()
    conn.close()
    if delete_disc:
        return jsonify({
            "Message": "Discipline deleted",
            "Discipline": {
                "id":delete_disc[0],
                "discipline_name":delete_disc[1]

            }
        })
    else:
        return jsonify({ "Error": "Discipline not found" }), 404


if __name__ == '__main__':
    app.run(debug=True)


