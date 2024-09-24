from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageEnhance
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance_image():
    data = request.json
    sharpness_value = float(data['sharpness'])
    contrast_value = float(data['contrast'])
    color_value = float(data['color'])

    # The image data is coming as a Base64 string from the frontend
    image_data = data['image'].split(",")[1]
    image_bytes = base64.b64decode(image_data)
    
    # Open the image from the byte stream
    image = Image.open(io.BytesIO(image_bytes))
    
    # Apply the sharpness enhancement first
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness_value)
    
    # Apply contrast enhancement
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_value)
    
    # Apply color enhancement
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(color_value)
    
    # Save the enhanced image to a byte stream
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Convert the image back to Base64 to return it to the frontend
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return jsonify({"enhanced_image": f"data:image/png;base64,{img_base64}"})

if __name__ == "__main__":
    app.run(debug=True)
