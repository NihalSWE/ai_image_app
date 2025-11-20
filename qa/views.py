from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import ask_gemini

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question')
        detections = request.data.get('detections')

        if not question:
            return Response({"error": "No question provided"}, status=400)

        # Call the AI function
        answer = ask_gemini(question, detections)
        
        return Response({"answer": answer})