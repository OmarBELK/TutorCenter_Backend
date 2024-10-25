from django.shortcuts import render
# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Comission
from .serializers import ComissionSerializer
from django.db.models import Sum
from datetime import datetime
from .models import *
from .serializers import *
from rest_framework import generics, filters, status
from rest_framework.response import Response
from .models import Groupe
from .serializers import GroupeWithEtudiantsSerializer
from django.utils import timezone
from django.db.models import Count
""" ------------------------------------------------- Etudiant Views ----------------------------------------------------"""

class EtudiantListView(generics.ListAPIView):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom', 'prenom', 'sexe', 'nationalite']  # Added 'id' here
    ordering_fields = ['id', 'nom', 'prenom', 'created_at']  # Also added 'id' here for ordering

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering for created_at
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def create_etudiant(request):
    """
    Create a new student.

    POST:
    - Creates a new student.

    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    if request.method == 'POST':
        serializer = EtudiantSerializer(data=request.data)
        if serializer.is_valid():
            etudiant = serializer.save()
            # If a groupe_id was provided and the assignment was successful
            if 'groupe_id' in serializer.validated_data:
                return Response({
                    'etudiant': EtudiantSerializer(etudiant).data,
                    'message': 'Etudiant created and assigned to group successfully.'
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_etudiant(request, pk):
    """
    Update an existing student.

    PUT:
    - Updates an existing student identified by the pk (primary key).

    Returns:
    - 200 OK: Successful update
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Student with given ID not found
    """
    try:
        etudiant = Etudiant.objects.get(pk=pk)
    except Etudiant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EtudiantSerializer(etudiant, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_etudiant(request, pk):
    """
    Delete an existing student.

    DELETE:
    - Deletes an existing student identified by the pk (primary key).

    Returns:
    - 204 No Content: Successful deletion
    - 404 Not Found: Student with given ID not found
    """
    try:
        etudiant = Etudiant.objects.get(pk=pk)
    except Etudiant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    etudiant.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
""" -------------------------------------     Professeur    -----------------------------------"""

class ProfesseurListView(generics.ListAPIView):
    queryset = Professeur.objects.all()
    serializer_class = ProfesseurSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom', 'prenom', 'specialite']
    ordering_fields = ['id', 'nom', 'prenom', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering for created_at
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_professeur(request):
    """
    Create a new professor.

    POST:
    - Creates a new professor.

    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    if request.method == 'POST':
        serializer = ProfesseurSerializer(data=request.data)
        if serializer.is_valid():
            professeur = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .models import Professeur
from .serializers import ProfesseurSerializer

@api_view(['PUT'])
def update_professeur(request, pk):
    """
    Update an existing professor.

    PUT:
    - Updates an existing professor identified by the pk (primary key).

    Returns:
    - 200 OK: Successful update
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Professor with given ID not found
    """
    try:
        professeur = Professeur.objects.get(pk=pk)
    except Professeur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProfesseurSerializer(professeur, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_professeur(request, pk):
    """
    Delete an existing professor.

    DELETE:
    - Deletes an existing professor identified by the pk (primary key).

    Returns:
    - 204 No Content: Successful deletion
    - 404 Not Found: Professor with given ID not found
    """
    try:
        professeur = Professeur.objects.get(pk=pk)
    except Professeur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    professeur.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
""" -------------------------------------     Niveau    ---------------------------------------"""

from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Niveau
from .serializers import NiveauSerializer
from django.utils import timezone

class NiveauListView(generics.ListAPIView):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom_niveau']
    ordering_fields = ['id', 'nom_niveau', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering for created_at
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_niveau(request):
    """
    Create a new niveau (level).

    POST:
    - Creates a new niveau.

    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    if request.method == 'POST':
        serializer = NiveauSerializer(data=request.data)
        if serializer.is_valid():
            niveau = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_niveau(request, pk):
    """
    Update an existing niveau.

    PUT:
    - Updates an existing niveau identified by the pk (primary key).

    Returns:
    - 200 OK: Successful update
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Niveau with given ID not found
    """
    try:
        niveau = Niveau.objects.get(pk=pk)
    except Niveau.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = NiveauSerializer(niveau, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_niveau(request, pk):
    """
    Delete an existing niveau.

    DELETE:
    - Deletes an existing niveau identified by the pk (primary key).

    Returns:
    - 204 No Content: Successful deletion
    - 404 Not Found: Niveau with given ID not found
    """
    try:
        niveau = Niveau.objects.get(pk=pk)
    except Niveau.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    niveau.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


""" -------------------------------------     Filiere    ---------------------------------------"""

class FiliereListView(generics.ListAPIView):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom_filiere']
    ordering_fields = ['id', 'nom_filiere', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering for created_at
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_filiere(request):
    """
    Create a new filiere (branch).

    POST:
    - Creates a new filiere.

    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    if request.method == 'POST':
        serializer = FiliereSerializer(data=request.data)
        if serializer.is_valid():
            filiere = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_filiere(request, pk):
    """
    Update an existing filiere.

    PUT:
    - Updates an existing filiere identified by the pk (primary key).

    Returns:
    - 200 OK: Successful update
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Filiere with given ID not found
    """
    try:
        filiere = Filiere.objects.get(pk=pk)
    except Filiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FiliereSerializer(filiere, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_filiere(request, pk):
    """
    Delete an existing filiere.

    DELETE:
    - Deletes an existing filiere identified by the pk (primary key).

    Returns:
    - 204 No Content: Successful deletion
    - 404 Not Found: Filiere with given ID not found
    """
    try:
        filiere = Filiere.objects.get(pk=pk)
    except Filiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    filiere.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
""" -------------------------------------     Matiere    ---------------------------------------"""



class MatiereListView(generics.ListAPIView):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom_matiere']
    ordering_fields = ['id', 'nom_matiere', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering for created_at
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_matiere(request):
    """
    Create a new matiere (subject).

    POST:
    - Creates a new matiere.

    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    if request.method == 'POST':
        serializer = MatiereSerializer(data=request.data)
        if serializer.is_valid():
            matiere = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_matiere(request, pk):
    """
    Update an existing matiere.

    PUT:
    - Updates an existing matiere identified by the pk (primary key).

    Returns:
    - 200 OK: Successful update
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Matiere with given ID not found
    """
    try:
        matiere = Matiere.objects.get(pk=pk)
    except Matiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MatiereSerializer(matiere, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_matiere(request, pk):
    """
    Delete an existing matiere.

    DELETE:
    - Deletes an existing matiere identified by the pk (primary key).

    Returns:
    - 204 No Content: Successful deletion
    - 404 Not Found: Matiere with given ID not found
    """
    try:
        matiere = Matiere.objects.get(pk=pk)
    except Matiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    matiere.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


""" -------------------------------------     Groupe    ---------------------------------------"""

class GroupeListView(generics.ListAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom_groupe', 'niveau', 'filiere']
    ordering_fields = ['id', 'nom_groupe', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering for created_at
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_groupe(request):
    """
    Create a new groupe.

    POST:
    - Creates a new groupe.

    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    if request.method == 'POST':
        serializer = GroupeSerializer(data=request.data)
        if serializer.is_valid():
            groupe = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_groupe(request, pk):
    """
    Update an existing groupe.

    PUT:
    - Updates an existing groupe identified by the pk (primary key).

    Returns:
    - 200 OK: Successful update
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Groupe with given ID not found
    """
    try:
        groupe = Groupe.objects.get(pk=pk)
    except Groupe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GroupeSerializer(groupe, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_groupe(request, pk):
    """
    Delete an existing groupe.

    DELETE:
    - Deletes an existing groupe identified by the pk (primary key).

    Returns:
    - 204 No Content: Successful deletion
    - 404 Not Found: Groupe with given ID not found
    """
    try:
        groupe = Groupe.objects.get(pk=pk)
    except Groupe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    groupe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
""" -------------------------------------     Etudiant - Groupe    ---------------------------------------"""
from rest_framework.exceptions import ValidationError

@api_view(['POST'])
def assign_etudiant_group(request):
    """
    Handle assigning a student to a group.
    - POST: Assign an Etudiant to an existing Groupe.
    """
    # Deserialize the incoming data
    serializer = EtudiantGroupeSerializer(data=request.data)

    try:
        # Validate the input data and save the new assignment
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Save the assignment if valid
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        # Handle unique constraint or validation errors gracefully
        return Response(
            {"error": str(e.detail)},  # Use Django's built-in error detail
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
def unassign_etudiant_from_groupe(request):
    """
    Unassign a student from a group.

    DELETE:
    - Removes the association between a student and a group.

    Required:
    - 'etudiant_id' in request.data
    - 'groupe_id' in request.data

    Returns:
    - 204 No Content: Successful unassignment
    - 404 Not Found: Assignment not found
    """
    etudiant_id = request.data['etudiant_id']
    groupe_id   = request.data['groupe_id']
    try:
        etudiant_groupe = EtudiantGroupe.objects.get(etudiant_id=etudiant_id, groupe_id=groupe_id)
        etudiant_groupe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except EtudiantGroupe.DoesNotExist:
        return Response({"error": "Assignment not found."}, status=status.HTTP_404_NOT_FOUND)

""" -------------------------------------     View to List All Groups with Their Students   ---------------------------------------"""

@api_view(['GET'])
def list_groupes_with_etudiants(request):
    """
    List all students or students of a specific group.

    GET:
    - If 'groupe_id' is provided in query params, returns students of that specific group.
    - Otherwise, returns a list of all groups with their students.

    Returns:
    - 200 OK: Successful GET request
    - 404 Not Found: Group with given ID not found
    """
    if 'groupe_id' in request.query_params:
        groupe_id = request.query_params['groupe_id']
        try:
            groupe = Groupe.objects.get(pk=groupe_id)
            serializer = GroupeWithEtudiantsSerializer(groupe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Groupe.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        groupes = Groupe.objects.all()
        serializer = GroupeWithEtudiantsSerializer(groupes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class GroupeWithEtudiantsListView(generics.ListAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeWithEtudiantsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom_groupe', 'niveau', 'filiere']
    ordering_fields = ['id', 'nom_groupe', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Check if a specific groupe_id is requested
        groupe_id = self.request.query_params.get('groupe_id')
        if groupe_id:
            queryset = queryset.filter(id=groupe_id)

        # Date range filtering for created_at
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Check if a specific groupe_id is requested
        groupe_id = self.request.query_params.get('groupe_id')
        if groupe_id:
            try:
                groupe = queryset.get(id=groupe_id)
                serializer = self.get_serializer(groupe)
                return Response(serializer.data)
            except Groupe.DoesNotExist:
                return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        # Aggregation
        total_groups = queryset.count()
        total_students = queryset.aggregate(total_students=Count('etudiants'))['total_students']

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'results': serializer.data,
                'total_groups': total_groups,
                'total_students': total_students
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'total_groups': total_groups,
            'total_students': total_students
        })
""" -------------------------------------                Paiement          ---------------------------------------"""

class PaiementListView(generics.ListAPIView):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['etudiant', 'groupe', 'statut_paiement']
    ordering_fields = ['date_paiement', 'montant']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date_paiement__range=[start_date, end_date])

        # Aggregation
        total_amount = queryset.aggregate(total=Sum('montant'))['total']

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'results': serializer.data,
                'total_amount': total_amount
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'total_amount': total_amount
        })
    

@api_view(['POST'])
def create_paiement(request):
    """
    Create a new paiement.
    
    POST:
    - Creates a new paiement, and automatically generates a commission for the professor
      associated with the specified group.
    
    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    serializer = PaiementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # This will create the payment and trigger the auto-creation of the commission
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
""" -------------------------------------                Comissions          ---------------------------------------"""


class ComissionListView(generics.ListAPIView):
    queryset = Comission.objects.all()
    serializer_class = ComissionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['professeur', 'etudiant', 'groupe']
    ordering_fields = ['date_comission', 'montant']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date_comission__range=[start_date, end_date])

        # Aggregation
        total_amount = queryset.aggregate(total=Sum('montant'))['total']

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'results': serializer.data,
                'total_amount': total_amount
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'total_amount': total_amount
        })

""" -------------------------------------                Event          ---------------------------------------"""
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer
from django.utils import timezone

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'event_type', 'start_date', 'end_date']
    ordering_fields = ['id', 'title', 'start_date', 'end_date', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Date range filtering for created_at
        start_date = self.request.query_params.get('created_start_date')
        end_date = self.request.query_params.get('created_end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_event(request):
    """
    Create a new event.

    POST:
    - Creates a new event.

    Returns:
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_event(request, pk):
    """
    Update an existing event.

    PUT:
    - Updates an existing event identified by the pk (primary key).

    Returns:
    - 200 OK: Successful update
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Event with given ID not found
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_event(request, pk):
    """
    Delete an existing event.

    DELETE:
    - Deletes an existing event identified by the pk (primary key).

    Returns:
    - 204 No Content: Successful deletion
    - 404 Not Found: Event with given ID not found
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)













