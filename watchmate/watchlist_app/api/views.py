from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        #AttributeError at /movie/list/
        # Got AttributeError when attempting to get a value for field `name` on serializer `MovieSerializer`.
        # The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance.
        # Original exception text was: 'QuerySet' object has no attribute 'name'.
        serializer = MovieSerializer(movies, many = True) #serializer is an Object for multiple objects many = True
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data = request.data) #JSON request data
        if serializer.is_valid(): #Parse JSON request data
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED) #Complex DataType
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE']) #accepted renderer not set on response error
def movie_details(request, pk):
    if request.method  == 'GET':
        try:
             movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'Error':'Movie not found'},status = status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response("Movie Deleted", status = status.HTTP_204_NO_CONTENT)
