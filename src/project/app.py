from flask import Flask, render_template, request, redirect, url_for, session
import os
import time
import uuid
from werkzeug.utils import secure_filename
from flask import Request
from src.project.utils.main import image_to_circles


class CustomRequest(Request):
    def __init__(self, *args, **kwargs):
        super(CustomRequest, self).__init__(*args, **kwargs)
        self.max_form_parts = 2000000


app = Flask(__name__)
app.request_class = CustomRequest

app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


def process_image(image_path):
    print(f"Processing image: {image_path}")
    # Placeholder function for image processing
    processed_image_path = image_to_circles(image_path)
    print(f"Processed image saved as {processed_image_path}")
    return processed_image_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Received a POST request")
        if 'file' not in request.files:
            print("No file part in the request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename).lower()
            print(f"Original filename: {filename}")
            session_id = str(uuid.uuid4())
            print(f"Generated session ID: {session_id}")
            timestamp = int(time.time())
            print(f"Current timestamp: {timestamp}")
            filename = f"{session_id}_{timestamp}_{filename}"
            print(f"Secure filename: {filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"File path to save: {file_path}")
            file.save(file_path)
            print(f"File saved to: {file_path}")
            processed_image_path = process_image(file_path)
            return render_template('index.html',
                                   uploaded_image=url_for('static', filename=f'uploads/{filename}'),
                                   processed_image=url_for('static',
                                                           filename=f'uploads/results/{os.path.basename(processed_image_path)}'))
    print("Received a GET request")
    return render_template('index.html')


if __name__ == '__main__':
    print("Starting Flask app")
    app.run(debug=True)
