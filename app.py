from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

print("Connecting to database with the following:")
print("Host:", os.getenv("MYSQL_HOST"))
print("User:", os.getenv("MYSQL_USER"))
print("Database:", os.getenv("MYSQL_DATABASE"))
print("Port:", os.getenv("MYSQL_PORT"))

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
app.config['UPLOAD_FOLDER'] = 'static/uploads'

mysql = MySQL(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Sidebar Template
sidebar = '''
<div id="sidebar" class="sidebar">
    <div class="logo-container">
        <img src="/static/logo.png" alt="Website Logo" class="logo">
    </div>
    <a href="javascript:void(0)" class="closebtn" onclick="closeSidebar()">×</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/manage-outfits">Manage Outfits</a>
    <a href="/suggest-outfit">Outfit Suggestions</a>
    <a href="/calendar">Calendar</a>
    <div class="logout-container">
        <a href="/logout" class="logout">Logout</a>
    </div>
</div>
<div id="openSidebarButton">
    <button onclick="openSidebar()">☰ Open Sidebar</button>
</div>
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    transition: background-color 0.3s ease-in-out;
}

#openSidebarButton {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1002; /* Ensure this button is above everything else */
}

#openSidebarButton button {
    background-color: #4CAF50;
    color: white;
    font-size: 20px;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 5px;
}

#openSidebarButton button:hover {
    background-color: #45a049;
}

.hidden {
    display: none;
}

.container {
    margin-top: 80px; /* Ensure content starts below the Open Sidebar button */
    padding: 20px;
}

.sidebar {
    height: 100%;
    width: 0;
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(76, 175, 80, 0.9); /* Green background with transparency */
    overflow-x: hidden;
    transition: 0.5s ease-in-out; /* Smooth transition */
    padding-top: 20px;
    box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.2);
    z-index: 1000; /* Ensure it is above other elements */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.sidebar .logo-container {
    text-align: center;
    margin-bottom: 20px;
}

.sidebar .logo {
    width: 150px;
    height: auto;
    border-radius: 5px;
}

.sidebar a {
    padding: 15px 20px;
    text-decoration: none;
    font-size: 18px;
    color: white;
    display: block;
    transition: 0.3s ease-in-out;
    display: flex;
    align-items: center;
}

.sidebar a:hover {
    background-color: #45a049;
}

.sidebar .closebtn {
    position: absolute;
    top: 0;
    right: 25px;
    font-size: 36px;
    margin-left: 50px;
    color: white;
    text-decoration: none;
    z-index: 1001; /* Ensure the close button is above the sidebar */
}

.sidebar .logout-container {
    margin-top: auto; /* Push logout to the bottom */
    text-align: center;
    padding-bottom: 20px;
}

.sidebar .logout {
    background-color: rgba(255, 0, 0, 0.8); /* Red background */
    text-align: center;
    padding: 10px;
    border-radius: 5px;
    color: white;
    text-decoration: none;
    display: block;
}

.sidebar .logout:hover {
    background-color: rgba(255, 0, 0, 1);
}

#profileDropdown {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1003;
    display: inline-block;
}

#profileDropdown img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    object-fit: cover;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

#profileDropdownContent {
    display: none;
    position: absolute;
    right: 0;
    margin-top: 10px;
    background-color: white;
    min-width: 150px;
    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
    z-index: 1004;
    border-radius: 5px;
    overflow: hidden;
}

#profileDropdownContent a {
    text-decoration: none;
    color: black;
    padding: 10px 15px;
    display: block;
    transition: background-color 0.3s ease-in-out;
}

#profileDropdownContent a:hover {
    background-color: #f1f1f1;
}
</style>
<script>

function openSidebar() {
    document.getElementById("sidebar").style.width = "250px"; // Expand the sidebar
    document.querySelector("body").style.backgroundColor = "rgba(0,0,0,0.4)"; // Dim the background
    document.getElementById("openSidebarButton").classList.add("hidden"); // Hide the open button
}

function closeSidebar() {
    document.getElementById("sidebar").style.width = "0"; // Collapse the sidebar
    document.querySelector("body").style.backgroundColor = "white"; // Restore the background
    document.getElementById("openSidebarButton").classList.remove("hidden"); // Show the open button
}

function toggleDropdown() {
    const dropdown = document.getElementById("profileDropdownContent");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('#profileDropdown img')) {
        const dropdown = document.getElementById("profileDropdownContent");
        if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
        }
    }
}
</script>
'''

# Routes
@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        profile_picture = request.files['profile_picture']
        profile_picture_path = None

        if profile_picture and profile_picture.filename != '':
            filename = secure_filename(profile_picture.filename)
            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_picture.save(profile_picture_path)

            # Save relative path for display
            profile_picture_path = f'static/uploads/{filename}'
        else:
            # Use default profile picture if none is uploaded
            profile_picture_path = 'static/images/default_profile_picture.png'

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, password, profile_picture) VALUES (%s, %s, %s)",
                        (username, password, profile_picture_path))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('register.html', sidebar=sidebar, container_class="container")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['profile_picture'] = user[3]  # Save the relative path to the profile picture in the session
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    return render_template('login.html', sidebar=sidebar, container_class="container")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    profile_picture = session.get('profile_picture', 'static/images/default_profile_picture.png')

    return render_template(
        'dashboard.html',
        sidebar=sidebar,
        container_class="container",
        profile_picture=profile_picture
    )

@app.route('/manage-outfits', methods=['GET', 'POST'])
def manage_outfits():
    if 'user_id' not in session:
        return redirect('/login')

    profile_picture = session.get('profile_picture', 'static/images/default_profile_picture.png')

    user_id = session['user_id']
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if 'add_item' in request.form:
            category = request.form['category']
            item_name = request.form['item_name']
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)

                # Save relative path to database
                relative_path = f'uploads/{filename}'
                cur.execute("""
                    INSERT INTO outfits (user_id, category, item_name, image_path)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, category, item_name, relative_path))
                mysql.connection.commit()

        elif 'remove_item' in request.form:
            item_id = request.form['item_id']
            cur.execute("DELETE FROM outfits WHERE id = %s AND user_id = %s", (item_id, user_id))
            mysql.connection.commit()

    cur.execute("SELECT * FROM outfits WHERE user_id = %s", [user_id])
    outfits = cur.fetchall()
    cur.close()

    return render_template(
        'manage_outfits.html',
        outfits=outfits,
        sidebar=sidebar,
        container_class="container",
        profile_picture=profile_picture
    )

@app.route('/suggest-outfit')
def suggest_outfit():
    if 'user_id' not in session:
        return redirect('/login')

    profile_picture = session.get('profile_picture', 'static/images/default_profile_picture.png')

    user_id = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM outfits WHERE user_id = %s", [user_id])
    outfits = cur.fetchall()
    cur.close()

    # Randomized suggestion logic
    pants = [o for o in outfits if o[2] == 'Pants']
    shirts = [o for o in outfits if o[2] == 'Shirt']
    shoes = [o for o in outfits if o[2] == 'Shoes']

    suggestion = {
        'pants': random.choice(pants) if pants else None,
        'shirt': random.choice(shirts) if shirts else None,
        'shoes': random.choice(shoes) if shoes else None
    }

    return render_template('outfit_suggestion.html', suggestion=suggestion, sidebar=sidebar, container_class="container", profile_picture=profile_picture)

@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        return redirect('/login')

    profile_picture = session.get('profile_picture', 'static/images/default_profile_picture.png')

    return render_template('calendar.html', sidebar=sidebar, container_class="container", profile_picture=profile_picture)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('profile_picture', None)
    return redirect('/login')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)

