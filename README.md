Description:
The Daily Mood Journal is a web application built with Flask, designed to help users track their moods, 
express gratitude, and gain insights into their emotional well-being. 
The application provides a user-friendly interface with features to add mood and gratitude entries, 
view mood trends through visualizations, and maintain a personal gratitude wall.

Features:
1. User Authentication:
    **Secure login and registration with hashed passwords using Flask-Login
2. Mood Tracking:
    **Log daily moods with optional journal entries
    **View mood trends visualized in a line chart
3. Gratitude Wall:
    **Add gratitude entries and reflect on positive experiences
4. Responsive Design:
    **Mobile-friendly layout with retro-inspired design elements
5. Interactive UI:
    **Character counters, flash message auto-dismissal, and form validation

Project Structure:
├── templates/               # HTML Templates
│   ├── base.html            # Base layout
│   ├── index.html           # Homepage
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # User dashboard
│   ├── add_mood.html        # Add mood entry page
│   ├── add_gratitude.html   # Add gratitude entry page
│   ├── mood_trends.html     # Mood trends visualization
│   ├── gratitude_wall.html  # Gratitude wall
├── static/                  # Static files
│   ├── app.js               # JavaScript for interactivity
│   ├── styles.css           # Styles
├── data/                    # Database folder
│   ├── database.db          # SQLite database
├── app.py                   # Flask application

Technologies Used:
**Backend: Flask, SQLAlchemy
**Frontend: HTML, CSS, JavaScript, Bootstrap
**Visualization: Matplotlib
**Database: SQLite

Personal Touch:
1. Interative UI Elements: 
    **Character counters for text areas, flash message auto-dismissal, and form validation. 
    These features enhance user experience and are handled in app.js
2. Custom Hover Effects:
    **Custom hover effects for buttons and cards, such as .retro-btn:hover and .gratitude-card:hover styles in styles.css
3. Mood Trends Visualization:
    **Visualize mood trends over time using Matplotlib. This is implemented in the /mood_trends route in app.py
4. Mood and Gratitude Tracking:
    **The application allows users to log their moods and gratitude entries, providing a personal space for reflection and emotional tracking. 
    This functionality is implemented through various routes and templates, such as add_mood.html and gratitude_wall.html
5. Flash Messages:
    **Flash messages are used to provide feedback to users, such as successful logins, registrations, and form submissions. 
    These messages are styled and managed in styles.css and app.js
6. Custom Navigation Bar:
    **A custom navigation bar with links to different sections of the application, 
    such as the dashboard, mood trends, and gratitude wall, is implemented in base.html
