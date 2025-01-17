from flask import Flask, request, jsonify, send_from_directory
from rembg import remove
from PIL import Image
from io import BytesIO

from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)


@app.route('/removebg', methods=['POST'])
def remove_bg():
    try:
        # Get the uploaded image from the request
        uploaded_file = request.files['image']
        
        # Read the image and remove the background
        img = Image.open(uploaded_file)
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        # Remove the background using rembg
        output_image = remove(img_bytes, alpha_matting=True, alpha_matting_background_threshold=50)
        
        # Save the output image locally
        output_path = 'masked/' + uploaded_file.filename
        with open(output_path, 'wb') as f:
            f.write(output_image)

        return jsonify({"message": "Background removed successfully", "data": output_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Add a route to serve the 'masked' directory
@app.route('/masked/<filename>')
def get_masked_image(filename):
    return send_from_directory('masked', filename)

if __name__ == '__main__':
    app.run(debug=True)
