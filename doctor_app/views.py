
from webbrowser import get
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
import requests
import logging


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        logging.warning("in loginview")
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        logging.warning("in appoinview")
       # print >> sys.sterr, 'hello login'
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        userDetails = {
            'doctorId' : user.id,
            'doctorName' : user.name,
            'doctorSpecialization' : user.specialization,
            'email' : user.email,
            'password': user.password,
            

        }

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'userDetails':userDetails
          
            
            
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logged out'
        }
        return response
    
class AllDocsView(APIView):
    def get(self,request,bid=None):
      queryset = User.objects.all()

      # Serialize list of todos item from Django queryset object to JSON formatted data
      read_serializer = UserSerializer(queryset, many=True)

    # Return a HTTP response object with the list of todo items as JSON
      return Response(read_serializer.data)  



class AppointmentAPIView(APIView):
    def get(self, request):
        logging.warning("in appoinview")
       
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        return Response(self.format_appointment(user.id))

    def format_appointment(self,doctor):
        appointment = requests.get('http://127.0.0.1:8001/Doctor/%d/appointment/'%doctor).json() 
        return{
            'doctor_id':doctor,
            'appointment':appointment

        }

   