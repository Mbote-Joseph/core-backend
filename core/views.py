from rest_framework import status
from .models import SuperAdmin, Admin, Building, Visitor
from .serializers import SuperAdminSerializer, AdminSerializer, BuildingSerializer, VisitorSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import generics
from .serializers import SuperAdminSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Building
from .serializers import BuildingSerializer
from .permissions import IsSuperAdmin


@api_view(['POST'])
def superadmin_register(request):
    serializer = SuperAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def superadmin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user and isinstance(user, SuperAdmin):
        # Return some token or success response
        return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperAdmin]) # Make sure to define IsSuperAdmin permission
def superadmin_create_building(request):
    if request.method == 'POST':
        user = request.user
        if isinstance(user, SuperAdmin):
            serializer = BuildingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(superadmin=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Not a SuperAdmin'}, status=status.HTTP_403_FORBIDDEN)

class SuperAdminListView(generics.ListAPIView):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def superadmin_list_admins(request):
    user = request.user

    # Check if the user is an instance of SuperAdmin
    if not isinstance(user, SuperAdmin):
        return Response({'error': 'You must be a SuperAdmin to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

    # Query all the Admin instances that are associated with the authenticated SuperAdmin's building
    admins = Admin.objects.filter(building__superadmin=user)

    # Serialize the Admin instances
    serializer = AdminSerializer(admins, many=True)

    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def admin_register(request):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Admin verification logic can be added here
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user and isinstance(user, Admin) and user.is_verified:
        # Return some token or success response
        return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials or account not verified'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def admin_list_visitors(request):
    visitors = Visitor.objects.filter(building=request.user.building)
    serializer = VisitorSerializer(visitors, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def visitor_checking(request):
    serializer = VisitorSerializer(data=request.data)
    if serializer.is_valid():
        visitor = serializer.save()
        otp = generate_otp(visitor)  # Implement OTP generation logic
        send_otp(otp, visitor.phone_number)  # Implement sending OTP logic
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def visitor_verify_otp(request):
    otp = request.data.get('otp')
    visitor_id = request.data.get('visitor_id')
    visitor = Visitor.objects.get(id=visitor_id)
    if verify_otp(otp, visitor):  # Implement OTP verification logic
        return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def visitor_select_room(request):
    visitor_id = request.data.get('visitor_id')
    room_id = request.data.get('room_id')
    
    try:
        visitor = Visitor.objects.get(id=visitor_id)
        room = Room.objects.get(id=room_id)

        # You can add further validation, e.g., checking if the room is available, etc.
        
        visitor.room = room
        visitor.save()

        serializer = VisitorSerializer(visitor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Visitor.DoesNotExist:
        return Response({'error': 'Visitor not found'}, status=status.HTTP_404_NOT_FOUND)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)