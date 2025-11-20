import google.generativeai as genai
from django.conf import settings

# ---------------------------------------------------------
# CONFIGURE GEMINI AI
# ---------------------------------------------------------
GEMINI_API_KEY = "AIzaSyBzuhEdaF75IjnXexqeV9_JynxsY1gapIQ"

# ---------------------------------------------------------
# 1. BACKUP FUNCTION (Must be first)
# ---------------------------------------------------------
def smart_backup_response(question, detections):
    found_objects = []
    if detections and isinstance(detections, list):
        for d in detections:
            if isinstance(d, dict):
                found_objects.append(d.get('class', 'object'))
    
    unique_objects = list(set(found_objects))
    
    if not unique_objects:
        return "I processed the image but couldn't identify specific objects. Try another image."
        
    return f"I detected these objects: {', '.join(unique_objects)}. (Note: Running in offline mode)."

# ---------------------------------------------------------
# 2. MAIN FUNCTION (Uses gemini-pro to fix 404 error)
# ---------------------------------------------------------
def ask_gemini(question, detections):
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # FIX: Using 'gemini-pro' because your account couldn't find 1.5-flash
        model = genai.GenerativeModel('gemini-pro')
        
        context = f"Objects detected: {detections}. "
        prompt = f"{context} User asks: '{question}'. Answer briefly."
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"⚠️ API Error ({e}). Switching to Backup.")
        return smart_backup_response(question, detections)