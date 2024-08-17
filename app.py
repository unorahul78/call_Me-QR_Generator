from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_img = None  # Placeholder for the QR code image

    if request.method == 'POST':
        mobile_number = request.form['mobile_number']  # Get mobile number from form

        # Create the QR code data with the 'tel:' scheme
        qr_data = f"tel:{mobile_number}"

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create an image from the QR code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a BytesIO object
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Convert the image to base64 for rendering in HTML
        qr_code_img = base64.b64encode(img_io.getvalue()).decode('ascii')

        # Pass the image directly to the template
        return render_template('index.html', qr_code_img=qr_code_img)

    return render_template('index.html', qr_code_img=qr_code_img)

@app.route('/download', methods=['POST'])
def download():
    mobile_number = request.form['mobile_number']
    qr_data = f"tel:{mobile_number}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(debug=True)
