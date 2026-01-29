from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os

# Configure Flask to look for templates in the current directory
app = Flask(__name__, template_folder='.', static_folder='.')

def load_products():
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    products = load_products()
    return render_template('index.html', products=products)

@app.route('/products')
def product_list():
    products = load_products()
    return render_template('index.html', products=products, scroll_to="products")

@app.route('/contact', methods=['POST'])
def contact():
    data = request.form
    name = data.get('name')
    phone = data.get('phone')
    message = data.get('message')
    
    # Save to CSV file
    import csv
    from datetime import datetime
    
    file_exists = os.path.isfile('contacts.csv')
    
    with open('contacts.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Thời gian', 'Họ tên', 'Số điện thoại', 'Tin nhắn'])
        
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, phone, message])
        
    print(f"New Contact Request: Name={name}, Phone={phone}, Request={message}")
    return jsonify({"success": True, "message": "Cảm ơn bạn! Chúng tôi sẽ liên hệ sớm nhất."})

# Route to serve specific static files if needed (though static_folder='.' handles most)
@app.route('/<path:filename>')
def serve_static(filename):
    if filename == 'index.html':
        return home()
    return send_from_directory('.', filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
