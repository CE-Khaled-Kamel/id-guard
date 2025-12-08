# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import extract_id_from_image
from django.http import HttpResponse

class IDVerificationView(APIView):
    def post(self, request):
        # 1. Check if file exists
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image provided. Key must be 'image'."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Get the file
        uploaded_file = request.FILES['image']

        # 3. Call your Logic
        try:
            data = extract_id_from_image(uploaded_file)
            
            if data.get("dl_number"):
                return Response({
                    "status": "success",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "failed",
                    "message": "Could not detect a valid California ID pattern."
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def home(request):
        return HttpResponse("""
        <html>
            <head>
                <title>ID-Guard API 🛡️</title>
                <style>
                    body { font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f4f4f9; }
                    h1 { color: #333; }
                    .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                    code { background: #eee; padding: 5px; border-radius: 5px; display: block; margin: 10px 0; text-align: left; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>ID-Guard API is Live 🟢</h1>
                    <p>Welcome to the Automated Identity Verification Microservice.</p>
                    <hr>
                    <h3>How to use:</h3>
                    <p>Send a POST request with an image file to:</p>
                    <code>POST /api/verify/</code>
                    
                    <h3>Example (Terminal):</h3>
                    <code>curl -X POST -F "image=@test_id.jpg" https://id-guard-api.onrender.com/api/verify/</code>
                </div>
            </body>
        </html>
        """)