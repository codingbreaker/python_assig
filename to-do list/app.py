from flask import Flask, render_template, request, redirect, url_for
from flask_graphql import GraphQLView
from schema import schema
import requests

app = Flask(__name__)

# Home page to display all To-Dos

@app.route('/')
def index():
    # Query the GraphQL endpoint to fetch todos
    graphql_query = '{ todos { id title description time } }'
    response = requests.post('http://localhost:5000/graphql', json={'query': graphql_query})
    
    if response.status_code == 200:
        todos = response.json()['data']['todos']
        return render_template('index.html', todos=todos)
    else:
        return 'Error fetching todos', response.status_code
# Add a new To-Do
# Initialize an empty list for todos_data globally


@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    description = request.form['description']
    time = request.form['time']
    global todos_data  # Access the global todos_data list
    new_todo = {'id': len(todos_data) + 1, 'title': title, 'description': description, 'time': time}
    todos_data.append(new_todo)  # Append the new todo item directly to todos_data
    return redirect(url_for('index'))



# Delete a To-Do
@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    global todos
    schema.todos = [todo for todo in schema.todos if todo['id'] != id]
    return redirect(url_for('index'))

# Edit a To-Do
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = next((todo for todo in schema.todos if todo['id'] == id), None)
    if todo is None:
        return "To-Do not found", 404

    if request.method == 'POST':
        todo['title'] = request.form['title']
        todo['description'] = request.form['description']
        todo['time'] = request.form['time']
        return redirect('/')

    return render_template('edit.html', todos=todos)

# GraphQL endpoint
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
