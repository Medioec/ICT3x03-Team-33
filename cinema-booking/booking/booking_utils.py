'''
    This file contains utility functions for the booking service.
'''
import qrcode
from io import BytesIO

# Generate QR code from booking details
def generateQRCode(bookingDetails):    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(bookingDetails))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_array = BytesIO()
    img.save(img_byte_array, format="PNG")
    img_data = img_byte_array.getvalue()
    return img_data

'''
This is sample of how to display QR code in frontend js (from chatgpt dont blame me if no work just edit if needed)

function fetchAndDisplayQRCode() {
            // Replace with the actual URL of your Flask server
            const serverUrl = 'http://your-flask-server-url/retrieveBooking/user_id/ticket_id'; // Update the URL

            fetch(serverUrl)
                .then(response => response.json())
                .then(data => {
                    // Get the QR code data from the response
                    const qrCodeData = data.qrCode;

                    // Set the QR code image source
                    const qrCodeImage = document.getElementById('qrCodeImage');
                    qrCodeImage.src = `data:image/png;base64, ${qrCodeData}`;
                })
                .catch(error => {
                    console.error('Error fetching QR code:', error);
                });
        }
'''