# s3_uploader/views.py
import boto3
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import logging
from .models import UploadedImage

logger = logging.getLogger(__name__)

@api_view(['POST'])
def get_presigned_url(request):
    """
    Generate a presigned URL for uploading a file directly to S3
    """
    try:
        file_name = request.data.get('fileName')
        file_type = request.data.get('fileType')
        
        if not file_name or not file_type:
            return Response(
                {'error': 'fileName and fileType are required'}, 
                status=400
            )
            
        # Create a unique file key to prevent overwrites
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        s3_key = f"uploads/{timestamp}-{file_name}"
        
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # Generate the presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': s3_key,
                'ContentType': file_type
            },
            ExpiresIn=300  # URL expires in 5 minutes
        )
        
        # Construct the public URL for the uploaded file
        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}"
        
        # Save record in database
        UploadedImage.objects.create(
            file_name=file_name,
            s3_key=s3_key,
            s3_url=file_url,
            content_type=file_type
        )
        
        return Response({
            'uploadUrl': presigned_url,
            'fileUrl': file_url
        })
        
    except Exception as e:
        logger.error(f"Error generating presigned URL: {str(e)}")
        return Response({'error': 'Failed to generate upload URL'}, status=500)