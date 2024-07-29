from django.contrib.auth.models import User
import cloudinary.uploader
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer, GenreSerializer, ActorSerializer, DirectorSerializer, MovieSerializer, TrailerSerializer
from .models import Genre, Actor, Director, Movie, Trailer
from trailers import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        poster = self.request.FILES.get('poster')

        if poster:
            try:
                upload_result = cloudinary.uploader.upload(poster)
                poster_url = upload_result.get("url")
            except Exception as e:
                raise serializers.ValidationError({"poster": str(e)})
        else:
            poster_url = None

        serializer.save(user=self.request.user, poster_url=poster_url)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        poster = request.FILES.get('poster')

        if poster:
            try:
                upload_result = cloudinary.uploader.upload(poster)
                poster_url = upload_result.get("url")
                instance.poster_url = poster_url
                instance.save()
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class TrailerViewSet(viewsets.ModelViewSet):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('video')
        
        if not file:
            return Response({"detail": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            upload_result = cloudinary.uploader.upload(file, resource_type="video")
            video_url = upload_result.get("secure_url")  # Utiliza "secure_url" en lugar de "url"
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        trailer_data = {
            'movie': request.data.get('movie'),
            'release_date': request.data.get('release_date'),
            'trailer_url': video_url  # Guarda la URL correcta del video
        }

        serializer = self.get_serializer(data=trailer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class TrailerViewSet(viewsets.ModelViewSet):
#     queryset = Trailer.objects.all()
#     serializer_class = TrailerSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         try:
#             file = request.data['video']  # Obtiene el archivo de video directamente
#             upload_result = cloudinary.uploader.upload(file, resource_type="video")
#             video_url = upload_result.get("url")
#         except KeyError:
#             return Response({"detail": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         trailer_data = {
#             'movie': request.data.get('movie'),  # Obtiene el ID de la película
#             'release_date': request.data.get('release_date'),  # Obtiene la fecha de lanzamiento
#             'trailer_url': video_url  # Incluye la URL del video en Cloudinary
#         }

#         serializer = self.get_serializer(data=trailer_data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)
