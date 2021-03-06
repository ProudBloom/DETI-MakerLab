# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from detimakerlab.technician_api.models import *
from detimakerlab.technician_api.serializers import EquipmentsSerializer, ProjectSerializer, RequestSerializer, \
    ExitSerializer, StudentSerializer, GroupSerializer, MissingSerializer, RequestPostSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    Create a token for user.
    Call this method within a valid username/password to generate da token. Then, use it in the headers:
    Authorization:Token **********
    Create user via: python manage.py createuser
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class MainPage(APIView):

    def get(self, request):
        msg = {'message': 'This is our main page!'}
        return Response(msg)


class ListAllEquipments(generics.ListCreateAPIView):
    """
        GET method to list all equipments in dB
        POST method to create a new equipment
    """
    queryset = Equipments.objects.all()
    serializer_class = EquipmentsSerializer


class EquipmentsDetails(generics.RetrieveUpdateDestroyAPIView):
    """
        GET, PUT, PATH, DELETE methods for a single equipment
    """
    queryset = Equipments.objects.all()
    serializer_class = EquipmentsSerializer


class ListAllProjects(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class BorrowEquipments(APIView):
    """
        When the technician authorize a student to borrow an equipment,
        this PUT method automatically updates the stock and update the availability.
    """

    def get_object(self, pk):
        try:
            return Equipments.objects.get(pk=pk)
        except Equipments.DoesNotExist:
            return Response('Equipment not found', status=HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        equipment = self.get_object(pk)
        a = equipment.borrow_equipment()
        if(a == HTTP_500_INTERNAL_SERVER_ERROR):
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=HTTP_200_OK)

class ReturnEquipments(APIView):
    """
            When the technician authorize a student return an equipment,
            this PUT method automatically updates the stock and update the availability.
        """

    def get_object(self, pk):
        try:
            return Equipments.objects.get(pk=pk)
        except Equipments.DoesNotExist:
            return Response('Equipment not found', status=HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        equipment = self.get_object(pk)
        a = equipment.return_equipment()
        print(a)
        if(a == 'INVALID'):
            print('----------HERE---------')
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=HTTP_200_OK)

# List of Requests
class ListAllRequests(generics.ListCreateAPIView):
    """
        GET Method return all requests.
        POST method creates a new request:
            @:param equipment_ref: <str>
            @:param project_ref: <str>
            Those parameters are passed in the body of the request.
    """

    queryset = Request.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return RequestPostSerializer
        else:
            return RequestSerializer


class RequestsDetails(generics.RetrieveUpdateDestroyAPIView):
    """
        GET method to retrieve details about a single request
            @:param id: <int>
        DELETE method to remove a request
            @:param id: <int>
    """
    queryset = Request.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return RequestPostSerializer
        else:
            return RequestSerializer


# Deal with requests
class ApproveRequest(APIView):
    """
        Method for the technician
        PUT method to approve a request
            @:param id: <int>
    """

    def get_object(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response('Request not found', status=HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        req = self.get_object(pk)
        serializer = RequestSerializer(req, data=request.data)
        if serializer.is_valid():
            req.approve()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response('{Error: request not found}', status=HTTP_404_NOT_FOUND)


class DenyRequest(APIView):
    """
            Methods for the techinician
            PUT method to deny a request
                @:param id: <int>
    """

    def get_object(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response('Request not found', status=HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        req = self.get_object(pk)
        serializer = RequestSerializer(req, data=request.data)
        if serializer.is_valid():
            req.deny()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response('{Error: request not found}', status=HTTP_404_NOT_FOUND)


# Exit functions
class ListAllExits(generics.ListCreateAPIView):
    """
        GET method to list all exits in dB
        POST method to create a new exit
    """
    queryset = Exit.objects.all()
    serializer_class = ExitSerializer


# Get all equipment borrowed by a project
class ExitsByProject(APIView):
    """
        Method for a group
        GET method to list equipment borrowed by a group
        @:param id: <int>
    """

    def get(self, request, pk):
        try:
            queryset = Exit.objects.filter(project=pk)
            serializer = ExitSerializer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Request.DoesNotExist:
            return Response('Group not found', status=HTTP_404_NOT_FOUND)
        except:
            return Response('Error processing request', status=HTTP_500_INTERNAL_SERVER_ERROR)


class Statistics(APIView):
    def get(self, pk):
        try:
            response_data = {}

            latestRequests = Request.objects.select_related().order_by("-timestamp")[:5]
            latestRequestsList = list(latestRequests.values())
            for r, l in zip(latestRequests, latestRequestsList):  # iterate over the 2 lists simultaneously
                l['equipmentDescription'] = r.equipment_ref.description
                l['equipmentFamily'] = r.equipment_ref.family
                l['projectThatRequested'] = r.project_ref.short_name
            response_data['latestRequests'] = latestRequestsList

            Projects = Project.objects.all()
            response_data['projects'] = list(Projects.values())

            okEquipmentCount = Equipments.objects.filter(broken='no').aggregate(Sum('total_items'))
            response_data['okEquipmentsTotal'] = okEquipmentCount["total_items__sum"] if okEquipmentCount[
                "total_items__sum"] else 0

            brokenEquipmentCount = Equipments.objects.filter(broken='yes').aggregate(Sum('total_items'))
            response_data['brokenEquipmentsTotal'] = brokenEquipmentCount["total_items__sum"] if brokenEquipmentCount[
                "total_items__sum"] else 0

            popularEquipments = Equipments.objects.annotate(TimesRequested=Count('request')).order_by('-TimesRequested')
            popularEquipmentsList = list(popularEquipments.values())
            for l in popularEquipmentsList:
                l['image_file'] = str(l['image_file'])
            response_data['popularRequests'] = popularEquipmentsList

            ExitsPerDay = (Exit.objects
                           # get specific dates (not hours for example) and store in "created"
                           .extra({'date': "date(timestamp)"})
                           # get a values list of only "created" defined earlier
                           .values('date')
                           # annotate each day by Count of Arrival objects
                           .annotate(created_count=Count('id')))
            ExitsPerDay = [i for i in ExitsPerDay]
            response_data['ExitsPerDay'] = ExitsPerDay

            return JsonResponse(response_data, json_dumps_params={'indent': 5})

        except Request:
            return Response('Error', status=HTTP_500_INTERNAL_SERVER_ERROR)


class StudentsView(generics.ListCreateAPIView):
    """
        Calls to students on db
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
        Calls to single students on db
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class GroupsView(generics.ListCreateAPIView):
    """
            Calls to groups on db
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
            Calls to groups on db
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MissingView(generics.ListCreateAPIView):
    """
            Calls to groups on db
    """
    queryset = Missing.objects.all()
    serializer_class = MissingSerializer


class MissingDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
            Calls to missing on db
    """
    queryset = Missing.objects.all()
    serializer_class = MissingSerializer


class StudentGroups(APIView):
    def get(self, request, pk):
        try:
            groups = Group.objects.filter(students__nmec=pk)

            projects =[]
            for group in groups:
                if hasattr(group, 'cod_project'):   # some groups might have no project, in that case they are ignored
                    projects.append(group.cod_project)

            serializer = ProjectSerializer(projects, many=True)

            return Response(serializer.data, status=HTTP_200_OK)

        except Request:
            return Response('Error', status=HTTP_500_INTERNAL_SERVER_ERROR)
