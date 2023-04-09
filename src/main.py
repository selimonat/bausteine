from flask import Flask, request, render_template
from PIL import Image
from circles import svg_circles, apply_palette

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the image file from the request object
        img_file = request.files['file']

        # Open the image using PIL
        img = Image.open(img_file)

        # Save the image to the static folder
        img.save('./static/image.png')

        # Apply the palette to the image
        apply_palette(img_file)

        # Render the template with the black and white image file
        return render_template('index.html',
                               image_file='image_palette.png',
                               png_image='image.png')

    # Render the template with no image file
    return render_template('index.html')


# @app.route('/', methods=['GET', 'POST'])
# def slider_submit():
#     if request.method == 'POST':
#         slider_value = request.form['sliderValue']
#         print(slider_value)
#         return f'The value of the slider is {slider_value}'
#     return render_template('slider.html')


if __name__ == '__main__':
    app.run(debug=False)
