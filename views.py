from flask import render_template, redirect, url_for, Flask, request, jsonify, json
from datetime import datetime
from flask import Flask
import models

app = Flask(__name__)


@app.post("/make_report")
def make_roport():
    table_name = request.form['table_name']
    row_data = json.loads(request.form['row_data'])
    data = dict()
    column_names = []
    if table_name == 'Альбомы':
        column_names = ['Название', 'Год выхода', 'Исполнители', 'Треки']
        for i in range(len(column_names)):
            data[column_names[i]] = row_data[i+1]
        data['Исполнители'] = data['Исполнители'][2:-2].replace('\n', ', ')
        data['Треки'] = data['Треки'][2:-2].replace('\n', ', ')
    elif table_name == 'Рецепты':
        column_names = ['Название блюда', 'Кухня', 'Ингредиенты', 'Рецепт']
        for i in range(len(column_names)):
            data[column_names[i]] = row_data[i+1]
        data['Ингредиенты'] = data['Ингредиенты'][2:-2].split('\n')
        data['Рецепт'] = data['Рецепт'].split('\n')
    return render_template('report.html', table_name=table_name, columns=column_names, data=data)
    

@app.get("/table")
def table():
    table_type = request.args.get('filter', type=str)
    calls = {
        'alboms':  [models.get_albums, 'Альбомы'],
        'recepts':  [models.get_receptes, 'Рецепты']
    }
    data, columns = calls[table_type][0]()
    table_name = calls[table_type][1]
    return render_template('table.html', columns=columns, data=data, table_name=table_name)



@app.route('/handle_cell_click', methods=['POST'])
def handle_cell_click():
    data = request.json
    row_data = data.get('row_data')
    column_names = data.get('column_names')
    table_name = data.get('table_name')
    type_col = data.get('type_col')
    IsModified = data.get('IsModified')

    pattern = False
    if table_name == 'Альбомы':
        type_col = [0, 1, 1, 2, 2]
        if IsModified:
            while '  ' in row_data[3]: row_data[3] = row_data[3].replace('  ', ' ')
            while '  ' in row_data[4]: row_data[4] = row_data[4].replace('  ', ' ')
            row_data[3] = row_data[3].replace('\n \n', '\n')
            row_data[4] = row_data[4].replace('\n \n', '\n')
        pattern = ['', '', '', 'Исполнители в столбик', 'Треки в столбик']
    elif table_name == 'Рецепты':
        type_col = [0, 1, 1, 2, 2]
        if IsModified:
            while '  ' in row_data[3]: row_data[3] = row_data[3].replace('  ', ' ')
            row_data[3] = row_data[3].replace('\n \n', '\n')
        pattern = ['', '', '', 'Ингредиенты в столбик', '']

    # Возвращаем ответ клиенту
    response = {
        'row_data': row_data,
        'column_names': column_names,
        'table_name': table_name,
        'type_col': type_col,
        'pattern': pattern
    }
    return jsonify(response)

def check_data(table_name, data, columns):
    if table_name == 'Альбомы':
        for i in range(1, 3):
            if data[i] == '': return [True, f'Поле "{columns[i]}" не может быть пустым']
        if data[4] == '': return [True, f'Поле "{columns[4]}" не может быть пустым']
        if not data[2].isnumeric(): return [True, 'Год должен быть целым положительным числом']
        if int(data[2]) >= datetime.now().year: return [True, 'Альбом не может быть выпущен в будущем']
    elif table_name == 'Рецепты':
        for i in [1, 3, 4]:
            if data[i] == '': return [True, f'Поле "{columns[i]}" не может быть пустым']
    return [False]

@app.route('/save_changes', methods=['POST'])
def save_changes():
    data = request.json
    row_data = data.get('row_data')
    column_names = data.get('column_names')
    table_name = data.get('table_name')

    messange = check_data(table_name, row_data, column_names)
    if messange[0]:
        response = {
            'IsCorrect': False,
            'message': messange[1]
        }
        return jsonify(response)
    models.edit_data(table_name, row_data)

    # Возвращаем ответ клиенту
    response = {
        'IsCorrect': True,
        'message': 'Изменения сохранены'
    }
    return jsonify(response)

@app.route('/add_new_row', methods=['POST'])
def add_new_row():
    data = request.json
    row_data = data.get('row_data')
    column_names = data.get('column_names')
    table_name = data.get('table_name')
    
    messange = check_data(table_name, row_data, column_names)
    if messange[0]:
        response = {
            'IsCorrect': False,
            'message': messange[1]
        }
        return jsonify(response)
    models.create_newRow(table_name, row_data)

    # Возвращаем ответ клиенту
    response = {
        'IsCorrect': True,
        'message': 'Запись сохранена'
    }
    return jsonify(response)

@app.route('/delete_row', methods=['POST'])
def delete_row():
    data = request.json
    delID = data.get('del_id')
    table_name = data.get('table_name')
    
    models.delete_data(table_name, delID)

    # Возвращаем ответ клиенту
    response = {
        'IsCorrect': True,
        'message': 'Запись удалена'
    }
    return jsonify(response)


@app.get("/")
def index():
    return render_template(
        "main-page.html"
    )
    

if __name__ == "__main__":
    app.run(debug=True)