from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import json
from .models import user , review  , Book , reservation




@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"]
        password = data["password"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        if password == "" or email == ""  or first_name == "" or last_name == "":
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data= {
                "message": "fields are required."
            })
        
        
        try:
            newuser = user.objects.create_user(email=email , password=password , first_name=first_name , last_name=last_name)
            newuser.save()
        except IntegrityError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data= {
                "message": "Email address already taken."
            })
        
        
        refresh = RefreshToken.for_user(newuser)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response(status=status.HTTP_201_CREATED, data= {
            "message": "User created successfully.",
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST , data= {
            "message": "POST request required."
        })
    
@api_view(['GET'])
@csrf_exempt
def search(request):
    if request.method == "GET":
        data = json.loads(request.body)
        query = data["search"]
        books = Book.objects.filter(name__icontains=query)
        response = []
        for book in books:
            response.append({
                "name": book.name,
                "description": book.description,
                "price": book.price,
                "seller": book.seller.email,
                "category": book.category
            })
        return Response(status=status.HTTP_200_OK, data= {
            "books": response
        })
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST , data= {
            "message": "GET request required."
        })
    

    
@api_view(['POST'])
@csrf_exempt
def addbook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data["name"]
        description = data["description"]
        price = data["price"]
        category = data["category"]
        picture =data["picture"]
        if name == "" or description == "" or price == "" or category == "" :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data= {
                "message": "All fields are required."
            })
        
        try:
            newbook = Book.objects.create(name=name , description=description , price=price , category=category , seller=request.user )
            if picture:
                newbook.picture = picture
            newbook.save()
        except IntegrityError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data= {
                "message": "Product already exists."
            })
        
        return Response(status=status.HTTP_201_CREATED, data= {
            "message": "Product added successfully."
        })
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST , data= {
            "message": "POST request required."
        })

@api_view(['POST'])
def addReview(request):
    if request.method == "POST":
        data = json.loads(request.body)
        book_id = data["book_id"]
        rating = data["rating"]
        review = data["review"]
        
        try:
            book = book.objects.get(id=book_id)
        except book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data= {
                "message": "Product not found."
            })
        
        newreview = review.objects.create(user=request.user , book=book , rating=rating , review=review)
        newreview.save()
        
        return Response(status=status.HTTP_201_CREATED, data= {
            "message": "Review added successfully."
        })
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST , data= {
            "message": "POST request required."
        })
    

@api_view(['POST'])
@csrf_exempt
def addPicture(request):
    if request.method == "POST" :
        data = json.loads(request.body)
        image = data["image"]
        book_id = data["book_id"]
        
        try:
            book = book.objects.get(id=book_id)
        except book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data= {
                "message": "Product not found."
            })
        
        newpicture = picture.objects.create(image=image , book=book)
        newpicture.save()
        
        return Response(status=status.HTTP_201_CREATED, data= {
            "message": "Picture added successfully."
        })
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST , data= {
            "message": "POST request required."
        })
    
@api_view(['POST'])
@csrf_exempt
def reservebook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        book_id = int(data["book_id"])
        
        try:
            book = book.objects.get(id=book_id)
        except book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data= {
                "message": "Product not found."
            })
        
        newreservation = reservation.objects.create(user=request.user , book=book)
        newreservation.save()

        book.delete()
        
        return Response(status=status.HTTP_201_CREATED, data= {
            "message": "Product reserved successfully."
        })
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST , data= {
            "message": "POST request required."
        })


