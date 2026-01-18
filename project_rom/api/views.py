from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import MenuSerializer, CategorySerializer
from app_restaurant.models import Menu, Category
from django.http import Http404

# Create your views here.
class MenuListCreateAPIView(APIView):
    # to handle get request
    def get(self, request):
        try:
            menus = Menu.objects.all() # fetching all menu items from db
            serializer = MenuSerializer(menus, many=True) # serializing the data
            context = {
                "status": status.HTTP_200_OK,
                "message": "Menu items fetched successfully",
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No menu items found",
                "error": str(e)
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    # to handle post request
    def post(self, request):
        data = request.data # taking data from request body
        serializer = MenuSerializer(data=data) # deserializing the data from request
        if serializer.is_valid(): # validating the data
            serializer.save() # saving the data to db
            context = {
                "status": status.HTTP_201_CREATED,
                "message": "Menu item created successfully",
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Menu item creation failed",
                "errors": serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class MenuDetailEditDeleteAPIView(APIView):
    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(instance=menu)
        context = {
            "status": status.HTTP_200_OK,
            "message": "Menu item fetched successfully",
            "data": serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        menu = self.get_object(pk)
        data = request.data
        serializer = MenuSerializer(instance=menu, data=data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "status": status.HTTP_200_OK,
                "message": "Menu item updated successfully",
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Menu item update failed",
                "errors": serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        menu = self.get_object(pk)
        menu.delete()
        context = {
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Menu item deleted successfully"
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)