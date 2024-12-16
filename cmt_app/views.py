from django.shortcuts import render
from django.http.response import JsonResponse 
from .models import Guest , Reservation , Movie
from rest_framework.decorators import api_view # For the Function Based Viwes
from .searializers import GuestSearializer , MovieSearializer , ReservationSearializer
from rest_framework import status ,filters # Status gives us the status in the internet like 404 , 200 .. 
from rest_framework.response import Response # Responce return the Status for the request 
from rest_framework.views import APIView # For the Classes Based Viwes
from rest_framework import generics ,mixins ,viewsets # Tool Help with writing an End point classes
from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#1 without REST and no model query
def no_rest_no_model(request) :


    guests = [
        {
            'id' : 1,
            'name' : 'Omaar',
            'mobile' : 31231231,
        },
        {
            'id' : 2 ,
            'name' : 'Kareem',
            'mobile' : 433431
        }

    ]
    return JsonResponse(guests , safe = False)

#2
def no_rest_from_model(request) :
    data = Guest.objects.all()
    response = {
        'guests' : list(data.values('name','mobile'))
    }
    return JsonResponse(response)

#3 Function Based Views
#3.1 GET POST

@api_view(['GET' , 'POST'])
def fbv_list(request) :

    # GET
    if request.method == 'GET' :
        guests = Guest.objects.all()
        searializer = GuestSearializer(guests , many = True)
        return Response(searializer.data)
    # POST
    elif request.method == "POST" :
        searializer = GuestSearializer(data= request.data)
        if searializer.is_valid() :
            searializer.save()
            return Response(searializer.data, status = status.HTTP_201_CREATED)
        return Response(searializer.data , status = status.HTTP_400_BAD_REQUEST)

#3.2 GET PUT DELETE
@api_view(['GET' , 'PUT' , 'DELETE'])
def fbv_pk(request , pk) :

    try : 
        guest = Guest.objects.get(pk = pk)
    except Guest.DoesNotExist :
        return Response(status = status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET' :
        searializer = GuestSearializer(guest)
        return Response(searializer.data)
    # PUT
    elif request.method == "PUT" :
        searializer = GuestSearializer(guest,data= request.data)
        if searializer.is_valid() :
            searializer.save()
            return Response(searializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(searializer.errors , status = status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE' :
        guest.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

#4 Class Based Views
#4.1 GET POST
class cbv_list(APIView) :
    def get(self , request) :
        guest = Guest.objects.all()
        serializer = GuestSearializer(guest , many = True)
        return Response(serializer.data)
    def post(self , requset) :
        serializer = GuestSearializer(data = requset.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status = status.HTTP_201_CREATED)
        return Response(serializer.data , status = status.HTTP_400_BAD_REQUEST )

#4.2 GET PUT DELETE
class cbv_pk (APIView) :
    def get_obj(self , pk) :
        try : 
            return Guest.objects.get(pk = pk)
        except Guest.DoesNotExist :
            return Response(status = status.HTTP_404_NOT_FOUND)
    # GET
    def get(self , request , pk) :
        guest = self.get_obj(pk)
        searializer = GuestSearializer(guest)
        return Response(searializer.data)
    # PUT
    def put(self , request , pk) :
        guest = self.get_obj(pk)
        searializer = GuestSearializer(guest,data= request.data)
        if searializer.is_valid() :
            searializer.save()
            return Response(searializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(searializer.errors , status = status.HTTP_400_BAD_REQUEST)
    # DELETE
    def delete(self , request , pk) :
        guest = self.get_obj(pk)
        guest.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

#5 Mixins
#5.1 mixins list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSearializer
    

    def get(self , request) :
        return self.list(request)
    def post(self , request) :
        return self.create(request)
    
#5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSearializer

    def get(self , request,pk) :
        return self.retrieve(request)
    def put(self , request,pk) :
        return self.update(request)
    def delet(self , request,pk) :
        return self.destroy(request)
    
#Generics
#6.1 get post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSearializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

#6.2 get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSearializer


#7 ViewSet
class viewset_guest (viewsets.ModelViewSet) :
    queryset = Guest.objects.all()
    serializer_class = GuestSearializer

class viewset_movie(viewsets.ModelViewSet) :
    queryset = Movie.objects.all()
    serializer_class = MovieSearializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewset_reservations(viewsets.ModelViewSet) :
    queryset =Reservation.objects.all()
    serializer_class = ReservationSearializer


#8 find movie 
@api_view(['GET'])
def find_movie(request) :
    movie = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie']
    )
    searializer = MovieSearializer(movie , many = True)
    return Response(searializer.data)

# create new Reservations 
@api_view(['POST'])
def newr(request) :
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie']
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    return Response( status= status.HTTP_201_CREATED)