# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import extract_id_from_image

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