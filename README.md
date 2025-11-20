# AI_Image_App

A Django-based AI image processing application with REST API support.

## Requirements

Install all dependencies:
```bash
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install Pillow
pip install ultralytics
pip install google-generativeai
pip install python-dotenv
pip install django-cors-headers
```

Or install all at once using the requirements.txt file:
```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/NihalSWE/ai_image_app.git
cd ai_image_app
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create requirements.txt (if needed):
```bash
pip freeze > requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Technologies Used

- Django
- Django REST Framework
- JWT Authentication
- Pillow (Image Processing)
- Ultralytics (YOLO)
- Google Generative AI
- CORS Headers