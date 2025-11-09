from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.secret_key = 'NewYouwontguess'

  
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'tasks' not in session:
        session['tasks'] = []

    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        if task:
            session['tasks'].append({'name': task, 'done': False})
            session.modified = True
            flash('Task added successfully!', 'success')
        else:
            flash('Please enter a valid task', 'error')
        return redirect(url_for('index'))
    
    return render_template('index.html', tasks=session['tasks'])

@app.route('/delete/<int:task_id>')
def delete(task_id):
    try:
        session['tasks'].pop(task_id)
        session.modified = True
        flash('Task deleted!', 'info')
    except IndexError:
        flash('Invalid task ID', 'error')

    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>')
def complete(task_id):
    try:
        session['tasks'][task_id]['done'] = True
        session.modified = True
        flash('Task marked complete!', 'info')
    except IndexError:
        flash('Invalid task ID', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)