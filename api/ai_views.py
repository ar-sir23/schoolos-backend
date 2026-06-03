import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import anthropic
from django.conf import settings

class ChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = request.data.get('message', '').strip()
        history = request.data.get('history', [])
        if not message:
            return Response({'error': 'message required'}, status=400)
        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            messages = history + [{'role': 'user', 'content': message}]
            response = client.messages.create(
                model=settings.AI_MODEL,
                max_tokens=1000,
                system="You are SchoolOS Assistant, a helpful AI for school management. Help with students, fees, attendance, and results.",
                messages=messages,
            )
            return Response({'reply': response.content[0].text})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
