import google.generativeai as genai
import os
import json

# 1. GET API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBzuhEdaF75IjnXexqeV9_JynxsY1gapIQ")

def smart_backup_response(question, detections):
    """
    ✅ DYNAMIC FALLBACK: Uses the REAL detected objects from YOLO.
    It does NOT guess. It reads what YOLO found.
    """
    found_objects = []
    
    # Extract object names from the detection list
    if detections and isinstance(detections, list):
        for d in detections:
            if isinstance(d, dict):
                # Get the 'class' (e.g., 'bird', 'car')
                obj_class = d.get('class', 'object')
                found_objects.append(obj_class)
    
    
    unique_objects = list(set(found_objects))
    count = len(detections)
    
    # Scenario 1: No objects found
    if not unique_objects:
        return "I analyzed the image, but I did not detect any specific objects."
        
    
    obj_string = ', '.join(unique_objects)
    return f"Analysis complete. I detected {count} object(s) in this image, specifically: {obj_string}. The detection confidence is high."

def ask_gemini(question, detections):
    # Debug Print
    print(f"🔑 GEMINI KEY LOADED: {str(GEMINI_API_KEY)[:10]}...", flush=True)

    if not GEMINI_API_KEY:
        return smart_backup_response(question, detections)

    # Setup Safety Settings (Prevents empty responses)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    context = f"""
    You are an AI assistant.
    OBJECTS DETECTED: {json.dumps(detections)}
    USER QUESTION: {question}
    Answer the question based on the objects above. Keep it short.
    """

    genai.configure(api_key=GEMINI_API_KEY)

    # 🔄 ATTEMPT 1: Gemini 1.5 Flash
    try:
        print("🔄 Trying Gemini 1.5 Flash...", flush=True)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(context, safety_settings=safety_settings)
        if response and response.text:
             return response.text.strip()
    except Exception:
        pass 

    # 🔄 ATTEMPT 2: Gemini Pro
    try:
        print("🔄 Trying Gemini Pro...", flush=True)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(context, safety_settings=safety_settings)
        if response and response.text:
             return response.text.strip()
    except Exception:
        pass


    return smart_backup_response(question, detections)