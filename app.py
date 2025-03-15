from flask import Flask, request, render_template_string, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google # type: ignore
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook # type: ignore

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Store messages in a list (in-memory storage for simplicity)
messages = []

# Google OAuth setup
google_bp = make_google_blueprint(
    client_id='YOUR_GOOGLE_CLIENT_ID', 
    client_secret='YOUR_GOOGLE_CLIENT_SECRET', 
    redirect_to='google_login'
)
app.register_blueprint(google_bp, url_prefix='/google_login')

# Facebook OAuth setup
facebook_bp = make_facebook_blueprint(
    client_id='YOUR_FACEBOOK_CLIENT_ID', 
    client_secret='YOUR_FACEBOOK_CLIENT_SECRET', 
    redirect_to='facebook_login'
)
app.register_blueprint(facebook_bp, url_prefix='/facebook_login')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the message from the form
        message = request.form.get('message')
        user_ip = request.remote_addr  # Get the user's IP address
        if message:
            # Create a formatted message
            formatted_message = f"{user_ip}: {message}"
            # Check for duplicates
            if formatted_message not in messages:
                messages.append(formatted_message)
            else:
                print("Duplicate message detected, not adding to the list.")

    return render_template_string("""
    <html>
    <head>
        <title>Professional Chat App</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7fa;
                margin: 0;
                padding: 20px;
            }
            .navtop {
                background-color: #2f3947;
                height: 60px;
                width: 100%;
                border: 0;
            }
            .navtop div {
                display: flex;
                margin: 0 auto;
                width: 900px;
                height: 100%;
                align-items: center;
            }
            .navtop div h1 {
                flex: 1;
                font-size: 24px;
                padding: 0;
                margin: 0;
                color: #eaebed;
            }
            .navtop div a {
                padding: 0 20px;
                text-decoration: none;
                color: #c1c4c8;
                font-weight: bold;
            }
            .navtop div a:hover {
                color: #ffffff;
            }
            .container {
                max-width: 900px;
                margin: auto;
                background: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #007bff;
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            h2 {
                color: #343a40;
                border-bottom: 2px solid #007bff;
                padding-bottom: 10px;
                margin-top: 20px;
            }
            p, ul, ol {
                color: #495057;
                line-height: 1.6;
            }
            ul, ol {
                margin-left: 20px;
            }
            .box {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                border-left: 5px solid #007bff;
            }
            form {
                margin-top: 20px;
                background: #f1f3f5;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                resize: none;
            }
            input[type="submit"] {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
                font-size: 1em;
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
            .message-list {
                margin-top: 20px;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-height: 400px;
                overflow-y: auto;
            }
            .message-list li {
                margin-bottom: 10px;
                padding: 12px;
                background: #e2e6ea;
                border-radius: 5px;
            }
            footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
            }
            .message-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #007bff;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 50%;
                cursor: pointer;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
                font-size: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .message-button:hover {
                background-color: #0056b3;
            }
            .message-count {
                position: absolute;
                top: -5px;
                right: -5px;
                background: red;
                color: white;
                border-radius: 50%;
                padding: 5px 10px;
                font-size: 12px;
                font-weight: bold;
            }
            .message-form {
                display: none;
                position: fixed;
                bottom: 80px;
                right: 20px;
                background: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
                width: 300px;
            }
        </style>
        <script>
            function toggleMessageForm() {
                var form = document.getElementById('messageForm');
                form.style.display = form.style.display === 'none' || form.style.display === '' ? 'block' : 'none';
            }
        </script>
    </head>
    <body>
        <div class="navtop">
            <div>
                <h1>Professional Chat App</h1>
                <a href="/google_login">Login with Google</a>
                <a href="/facebook_login">Login with Facebook</a>
            </div>
        </div>
        <div class="container">
            <h1>Welcome to the Online Chatting Platform</h1>
            <div class="box">
                <p>Connect with each other and share your thoughts. Messages are displayed with the sender's IP address for transparency.</p>
            </div>
            
            <h2>About Us</h2>
            <div class="box">
                <p>We are Hanan Ali Khan and Hussain, students of SCD Semester 6 at the University of Lahore. We are passionate about technology and programming.</p>
            </div>
            
            <h2>Interests</h2>
            <div class="box">
                <ul>
                    <li>Web Development</li>
                    <li>Data Science</li>
                    <li>Machine Learning</li>
                    <li>Artificial Intelligence</li>
                </ul>
            </div>
            
            <h2>Hobbies</h2>
            <div class="box">
                <p>In our free time, we enjoy:</p>
                <ol>
                    <li>Reading books</li>
                    <li>Playing video games</li>
                    <li>Exploring new technologies</li>
                    <li>Traveling and experiencing different cultures</li>
                </ol>
            </div>
            
            <h2>Contact Us</h2>
            <div class="box">
                <p>If you would like to get in touch, feel free to reach out via email:</p>
                <ul>
                    <li>Hanan Ali Khan: <a href="mailto:70132163@student.uol.edu.pk">70132163@student.uol.edu.pk</a></li>
                    <li>Hussain: <a href="mailto:70131680@student.uol.edu.pk">70131680@student.uol.edu.pk</a></li>
                </ul>
            </div>

            <h2>Messages</h2>
            <div class="message-list">
                <ul>
                    {% for msg in messages %}
                        <li>{{ msg }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        <button class="message-button" onclick="toggleMessageForm()">
            💬
            <span class="message-count">{{ messages|length }}</span>
        </button>
        <div id="messageForm" class="message-form">
            <form method="POST">
                <textarea name="message" rows="4" placeholder="Type your message here..." required></textarea><br>
                <input type="submit" value="Send">
            </form>
        </div>
        <footer>
            <p>&copy; 2023 Hanan Ali Khan and Hussain. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """, messages=messages)

@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    return f'You are logged in as: {resp.json()["displayName"]}'

@app.route('/facebook_login')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    resp = facebook.get('/me?fields=name,email')
    assert resp.ok, resp.text
    return f'You are logged in as: {resp.json()["name"]}'

if __name__ == '__main__':
    app.run(debug=True)