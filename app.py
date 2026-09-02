from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import base64

basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(data_dir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Mood entry model
class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    journal_entry = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class GratitudeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'Welcome back, {current_user.username}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# User Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.desc()).all()
    return render_template('dashboard.html', user=current_user, entries=entries)

@app.route('/add_mood', methods=['GET', 'POST'])
@login_required
def add_mood():
    if request.method == 'POST':
        mood = request.form.get('mood')
        journal_entry = request.form.get('journal_entry')

        if not mood:
            flash('Please select a mood.', 'danger')
            return redirect(url_for('add_mood'))

        new_entry = MoodEntry(
            user_id=current_user.id,
            mood=mood,
            journal_entry=journal_entry
        )
        db.session.add(new_entry)
        db.session.commit()

        flash('Your mood entry has been saved!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_mood.html')

@app.route('/mood_trends')
@login_required
def mood_trends():
    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.asc()).all()
    if not entries:
        flash('No mood entries to display trends.', 'warning')
        return redirect(url_for('dashboard'))

    # Prepare data
    dates = [entry.timestamp.strftime('%Y-%m-%d') for entry in entries]
    moods = [entry.mood for entry in entries]

    
    mood_scores = []
    mood_mapping = {
        'Happy': 5,
        'Excited': 4,
        'Neutral': 3,
        'Sad': 2,
        'Stressed': 1,
        'Mad': 0,
    }
    for mood in moods:
        score = mood_mapping.get(mood, 0)
        mood_scores.append(score)

    # Plot the mood trend
    plt.figure(figsize=(10, 5))
    plt.plot(dates, mood_scores, marker='o', linestyle='-', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Mood Score')
    plt.title('Mood Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    plt.close()  

    return render_template('mood_trends.html', plot_url=plot_url)

@app.route('/add_gratitude', methods=['GET', 'POST'])
@login_required
def add_gratitude():
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content:
            flash('Please enter your gratitude entry.', 'danger')
            return redirect(url_for('add_gratitude'))
            
        new_entry = GratitudeEntry(
            user_id=current_user.id,
            content=content
        )
        db.session.add(new_entry)
        db.session.commit()
        
        flash('Your gratitude entry has been saved!', 'success')
        return redirect(url_for('gratitude_wall'))
        
    return render_template('add_gratitude.html')

@app.route('/gratitude_wall')
@login_required
def gratitude_wall():
    entries = GratitudeEntry.query.filter_by(user_id=current_user.id)\
        .order_by(GratitudeEntry.timestamp.desc()).all()
    return render_template('gratitude_wall.html', entries=entries)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
