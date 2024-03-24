from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins 
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.parsers import MultiPartParser , FormParser
from .serializers import CustomUserSerializer
from django.contrib.auth import authenticate , login , logout 
from .models import CustomUser
from .csrf import CsrfExemptSessionAuthentication



class UserViews(APIView):
    
    #Changing this to IsAuthentcated will directly send 401 error if request.user is not authenticated
    permission_classes = [AllowAny]
    
    def get(self , request , *args ,**kwargs):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return Response(data={"message" : "Your not authenticated"} , status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(data = {"message" : "Your authenticated"})

class LoginViews(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [FormParser , MultiPartParser]
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get(self , request , *args , **kwargs):
            return Response(data={"message" : "send and POST request"})
    
    def post(self , request , *args , **kwargs):
        
        try:
            
            email = request.data.get("email" , None)
            password = request.data.get("password" , None)
            
            user =  authenticate(request,email = email , password = password)
            
            if user is None:
                return Response(data = {"message" : "No user found"}  , status=status.HTTP_404_NOT_FOUND)
            
            login(request , user = user)
            
            return Response(data = {"message" : "User logged in"})
            
        except Exception as e:  
            return Response(data={"message" :  str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RegisterViews(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [FormParser , MultiPartParser]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self , request , *args , **kwargs):
            return Response(data={"message" : "send and POST request"})
    
    def post(self , request , *args , **kwargs):
        
        try:
            
            email : str = request.data.get("email" , None)
            
            user_found : bool = CustomUser.objects.filter(email = email)
            
            if user_found:
                return Response(data={"message" : "choose a unique email"} , status=status.HTTP_400_BAD_REQUEST) 
                        
            serializer = CustomUserSerializer(data = request.data)
            
            if not serializer.is_valid():
                return Response(data={"message" : "validation error"} , status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()

            login(request , user=user)
            
            return Response(data={"message" : "User registered"})
            
        except Exception as e:
            
            return Response(data = {"message" : str(e)} , status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LogoutViews(APIView):
    
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def post(self , request , *args , **kwargs):
        
        logout(request)
        return Response(data={"message" : "Your logged out"})

class UserActionViews(GenericAPIView , mixins.ListModelMixin , mixins.RetrieveModelMixin , mixins.DestroyModelMixin):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get(self , request , *args , **kwargs):
        
        return self.list(self , request)
    
    def delete(self , request , *args ,  **kwargs):
        
        return self.destroy(self , request)
    
    # def get(self , request , *args , **kwargs):
        
    #     return self.retrieve(self , request)