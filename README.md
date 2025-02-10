# SurveyAnalytics

SurveyAnalytics is a Django web application that allows users to:

- **Register** and **log in**.
- **Upload surveys** via CSV, XLS, or XLSX files containing user responses.
- **Analyze the data**: the system processes the file, generates charts and insights (statistical summaries) from the responses.
- **Visualize surveys**: a list of uploaded surveys is displayed with options to open (view charts and insights) or delete a survey.
- **Download a PDF report**: a PDF report containing the charts and insights is generated and available for download.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation and Configuration](#installation-and-configuration)
- [Project Structure](#project-structure)
- [Usage and Application Flow](#usage-and-application-flow)
- [Libraries and Tools](#libraries-and-tools)
- [Deployment and Production](#deployment-and-production)
- [Additional Notes](#additional-notes)
- [Conclusion](#conclusion)

## Features

- **User Authentication:** Register, log in, email activation, password change, and password reset.
- **Survey Upload and Analysis:** Users can upload files in CSV, XLS, or XLSX formats containing survey responses. Data is processed using **Pandas** and charts are generated using **Matplotlib**.
- **Insights:** Basic insights (averages, counts, most common responses, etc.) are extracted from the survey data.
- **PDF Report:** Users can download a PDF report containing the generated charts and insights, created with **WeasyPrint**.
- **Survey Management:** A “Last Surveys” view lists the uploaded surveys with options to open (view analysis) and delete surveys.

## Requirements

- **Python 3.12** (or higher)
- **Django 5.1.5**
- **Pandas**
- **Matplotlib**
- **WeasyPrint**
- **python-decouple** (for managing environment variables)
- **django-widget-tweaks** (to improve form rendering in templates)

> **Note:** Ensure that your system has the necessary fonts for the charts (or configure Matplotlib to use fallback fonts such as “DejaVu Sans”).

## Installation and Configuration

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/tinocoAlexander/SurveyAnalytics.git
   cd survey_analytics

2. **Create a Virtual Environment:**
   ```bash
    python -m venv env
    source env/bin/activate   # On Linux/Mac
    env\Scripts\activate     # On Windows

3. **Install Dependencies: Create a requirements.txt file with the following (adjust versions as needed):**
   ```bash
    Django==5.1.5
    pandas
    matplotlib
    weasyprint
    python-decouple
    django-widget-tweaks
Then run:

pip install -r requirements.txt
    
4. **Configure Environment Variables: Create a .env file in the project root with essential variables, for example:**
   ```bash
    SECRET_KEY=your_secret_key_here
    DEBUG=True
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.your_email.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your_email@your_email.com
    EMAIL_HOST_PASSWORD=your_password
    DEFAULT_FROM_EMAIL=your_email@your_email.com
These variables are managed using python-decouple in your settings.py.

5. **Apply Migrations and Create a Superuser:**
   ```bash
    python manage.py migrate
    python manage.py createsuperuser

6. **Run the Development Server:**
   ```bash
    python manage.py runserver 8000
Then navigate to http://0.0.0.0:8000/ in your web browser.

# Project Structure
    survey_analytics/
    │
    ├── analysis/                  # Application for survey analysis
    │   ├── migrations/
    │   ├── templates/
    │   │   └── analysis/
    │   │       ├── analysisGraphs.html        # Template for displaying charts and insights
    │   │       ├── analysisGraphs_pdf.html      # Template for the PDF report
    │   │       ├── analysisSurveys.html         # Template for survey upload
    │   │       └── lastSurveys.html             # Template for listing surveys
    │   ├── urls.py
    │   └── views.py
    │
    ├── users/                     # Application for authentication and user management
    │   ├── migrations/
    │   ├── templates/
    │   │   └── users/
    │   │       ├── index.html
    │   │       ├── login.html
    │   │       ├── register.html
    │   │       ├── forgot_password.html
    │   │       └── ... (other authentication templates)
    │   ├── urls.py
    │   └── views.py
    │
    ├── errors/                    # Application for error pages
    │   ├── templates/
    │   │   └── errors/
    │   │       ├── 404.html
    │   │       ├── 401.html
    │   │       └── 400.html
    │   └── views.py
    │
    ├── static/                    # Static files (CSS, JS, images, fonts)
    │   ├── css/
    │   │   ├── analysisGraphs.css
    │   │   ├── analysisSurveys.css
    │   │   └── lastSurveys.css
    │   ├── js/
    │   │   ├── uploadFiles.js
    │   │   ├── lastSurveys.js
    │   │   └── ... (other scripts)
    │   └── images/
    │       ├── icons/
    │       │   ├── addIcon.svg
    │       │   ├── documentIcon.svg
    │       │   ├── optionsIcon.svg
    │       │   ├── uploadIcon.svg
    │       │   └── ... (other icons)
    │
    ├── media/                     # Uploaded files (surveys, images, etc.)
    │
    ├── survey_analytics/          # Django project configuration
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    └── manage.py


# Usage and Application Flow

**Authentication:**
- Users register and activate their account via an email verification.
- They can log in, reset, or change their password.

**Survey Upload:**
- In the "Add Surveys" section, users enter the survey name and upload a file (CSV, XLS, or XLSX) containing responses.
- The system validates the file, creates a Survey object, and saves the file as a SurveyFile.
- After successful upload, the user is redirected to the analysis view.

**Survey Analysis:**
- In the charts view (analysisGraphs), the file is processed using Pandas and charts are generated using Matplotlib.
- Insights (such as averages, most common responses, etc.) are extracted and displayed alongside the charts.
- Users can also download a PDF report of the charts and insights via WeasyPrint.

**Survey Management:**
- The "Last Surveys" view lists uploaded surveys (both recent and all).
- Each survey provides two options: Open (view analysis) and Delete (remove the survey from the database).

**Libraries and Tools**
- Django: Main web framework.
- Pandas: For data manipulation and analysis.
- Matplotlib: To generate charts from the data.
- WeasyPrint: To generate the PDF report.
- python-decouple: To manage environment variables.
- django-widget-tweaks: To enhance form rendering in templates.

**Deployment and Production**
- Set DEBUG to False in production.
- Configure ALLOWED_HOSTS properly in settings.py.
- Use a production-grade web server (such as Gunicorn or uWSGI) with Nginx to serve the application.
- Ensure all environment variables (email settings, secret key, etc.) are correctly set on the production server.

**Additional Notes**
**Fonts in Charts:**
- To avoid Matplotlib warnings like "findfont: Font family 'Poppins' not found", we use "DejaVu Sans" as a fallback. You can install your desired fonts on the system or configure Matplotlib accordingly.

**File Handling:**
- Uploaded files are stored in the media/surveys/ directory. Ensure MEDIA_ROOT and MEDIA_URL are correctly configured in settings.py.

**Custom Error Pages:**
- The project includes an errors app to manage custom 404, 401, and 400 error pages.

**PDF Report Download:**
- The downloadPDF view generates a PDF report containing charts and insights using WeasyPrint. The report can be downloaded by clicking the corresponding button in the analysis view.

# Conclusion

SurveyAnalytics is a comprehensive application for collecting, analyzing, and visualizing survey data. It combines Django, Pandas, Matplotlib, and WeasyPrint to offer users a complete tool—from authentication to generating PDF reports with visual insights.

Enjoy using SurveyAnalytics, and feel free to contribute or customize it to fit your needs!


Feel free to adjust any sections (e.g., repository URLs, environment variable values, or additional instructions) to match your actual project configuration.

