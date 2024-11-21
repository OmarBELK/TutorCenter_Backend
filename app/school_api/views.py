from ast import mod
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

class GroupeListView(generics.ListCreateAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['niveau', 'filiere']
    ordering_fields = ['created_at']

@api_view(['POST'])
def create_groupe(request):
    if request.method == 'POST':
        # Ensure filiere_id is provided
        if 'filiere' not in request.data:
            return Response(
                {'error': 'filiere field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GroupeSerializer(data=request.data)
        if serializer.is_valid():
            groupe = serializer.save()
            
            # Handle professeurs assignments
            professeurs_data = request.data.get('professeurs', [])
            for prof_data in professeurs_data:
                GroupeProfesseur.objects.create(
                    groupe=groupe,
                    professeur_id=prof_data['id'],
                    commission_fixe=prof_data.get('commission_fixe', 100.0)
                )
            
            # Handle matieres assignments
            matieres_data = request.data.get('matieres', [])
            for matiere_data in matieres_data:
                GroupeMatiere.objects.create(
                    groupe=groupe,
                    matiere_id=matiere_data['id']
                )
            
            return Response(GroupeSerializer(groupe).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_groupe(request, pk):
    """
    Update an existing groupe and its relationships.
    """
    try:
        groupe = Groupe.objects.get(pk=pk)
    except Groupe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = GroupeSerializer(groupe, data=request.data)
    if serializer.is_valid():
        groupe = serializer.save()
        
        # Update professeurs assignments
        if 'professeurs' in request.data:
            # Clear existing relationships
            GroupeProfesseur.objects.filter(groupe=groupe).delete()
            # Create new relationships
            for prof_data in request.data['professeurs']:
                GroupeProfesseur.objects.create(
                    groupe=groupe,
                    professeur_id=prof_data['id'],
                    commission_fixe=prof_data.get('commission_fixe', 100.0)
                )
        
        # Update matieres assignments
        if 'matieres' in request.data:
            # Clear existing relationships
            GroupeMatiere.objects.filter(groupe=groupe).delete()
            # Create new relationships
            for matiere_data in request.data['matieres']:
                GroupeMatiere.objects.create(
                    groupe=groupe,
                    matiere_id=matiere_data['id']
                )
        
        return Response(GroupeSerializer(groupe).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_groupe(request, pk):
    """
    Delete an existing groupe and its relationships.
    """
    try:
        groupe = Groupe.objects.get(pk=pk)
        
        # Delete related records first
        GroupeProfesseur.objects.filter(groupe=groupe).delete()
        GroupeMatiere.objects.filter(groupe=groupe).delete()
        EtudiantGroupe.objects.filter(groupe=groupe).delete()
        
        groupe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Groupe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
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


class GroupeWithEtudiantsListView(generics.ListAPIView):
    queryset = Groupe.objects.all()
    serializer_class = GroupeWithEtudiantsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'nom_groupe', 'niveau', 'filiere']
    ordering_fields = ['id', 'nom_groupe', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Existing filters
        groupe_id = self.request.query_params.get('groupe_id')
        if groupe_id:
            queryset = queryset.filter(id=groupe_id)

        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])

        # New filters for professors and subjects
        professeur_id = self.request.query_params.get('professeur_id')
        matiere_id = self.request.query_params.get('matiere_id')
        
        if professeur_id:
            queryset = queryset.filter(groupeprofesseur__professeur_id=professeur_id)
        if matiere_id:
            queryset = queryset.filter(groupematiere__matiere_id=matiere_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        groupe_id = self.request.query_params.get('groupe_id')

        if groupe_id:
            try:
                groupe = queryset.get(id=groupe_id)
                serializer = self.get_serializer(groupe)
                return Response(serializer.data)
            except Groupe.DoesNotExist:
                return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        # Enhanced aggregations
        total_groups = queryset.count()
        total_students = EtudiantGroupe.objects.filter(groupe__in=queryset).count()
        total_professors = GroupeProfesseur.objects.filter(groupe__in=queryset).count()
        total_subjects = GroupeMatiere.objects.filter(groupe__in=queryset).count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'results': serializer.data,
                'total_groups': total_groups,
                'total_students': total_students,
                'total_professors': total_professors,
                'total_subjects': total_subjects
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'total_groups': total_groups,
            'total_students': total_students,
            'total_professors': total_professors,
            'total_subjects': total_subjects
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
def create_payment(request):
    """Create a new payment record"""
    data = request.data
    
    try:
        # Get the groupe's subscription price first
        groupe = Groupe.objects.get(id=data['groupe_id'])
        montant_total = groupe.prix_subscription  # Get this first
        print("montant_total",montant_total)
        
        montant = data['montant']
        frais_inscription = data.get('frais_inscription', 0)
        
        total_payment = montant + frais_inscription
        remaining = montant_total - total_payment    # Now this will be correct
        print("remaining",remaining)
        
        # Create payment with correct montant_total and remaining
        payment = Paiement.objects.create(
            montant=total_payment,                   # Total paid (montant + frais_inscription)
            montant_total=montant_total,            # From groupe.prix_subscription
            remaining=remaining,                     # montant_total - total_payment
            frais_inscription=frais_inscription,
            etudiant_id=data['etudiant_id'],
            groupe_id=data['groupe_id'],
            statut_paiement='PARTIAL' if remaining > 0 else 'PAID'
        )

        # Create commissions
        commission_percentage = data.get('commission_percentage', 0)
        groupe_professeurs = GroupeProfesseur.objects.filter(groupe=groupe)
        for gp in groupe_professeurs:
            commission_amount = min(total_payment, gp.commission_fixe) * (commission_percentage / 100)
            Comission.objects.create(
                montant=commission_amount,
                date_comission=payment.date_paiement,
                statut_comission='PAID',
                professeur=gp.professeur,
                etudiant_id=data['etudiant_id'],
                groupe=groupe
            )
        
        return Response({
            'payment': PaiementSerializer(payment).data,
            'message': f"Payment received. Total paid: {total_payment} DH (including {frais_inscription} DH registration fee), Remaining: {remaining} DH"
        }, status=201)

    except Groupe.DoesNotExist:
        return Response({
            'error': 'Groupe not found'
        }, status=404)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=400)


@api_view(['PUT'])
def update_payment(request, payment_id):
    """Update remaining amount of an existing payment"""
    try:
        payment = Paiement.objects.get(id=payment_id)
        new_payment_amount = request.data['montant']
        
        if new_payment_amount > payment.remaining:
            return Response({
                'error': f'Payment amount ({new_payment_amount}) cannot exceed remaining amount ({payment.remaining})'
            }, status=400)
        
        # Update the existing payment record
        payment.montant += new_payment_amount
        payment.remaining -= new_payment_amount
        payment.statut_paiement = 'PAID' if payment.remaining == 0 else 'PARTIAL'
        payment.save()
        
        return Response({
            'payment': PaiementSerializer(payment).data,
            'message': f"Payment updated. Remaining: {payment.remaining} DH"
        })
    except Paiement.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=404)

@api_view(['GET'])
def get_payment_history(request, etudiant_id, groupe_id):
    """Get all payments for a student in a group"""
    try:
        payments = Paiement.objects.filter(
            etudiant_id=etudiant_id,
            groupe_id=groupe_id
        ).order_by('-date_paiement')

        # Get the groupe's subscription price
        groupe = Groupe.objects.get(id=groupe_id)
        
        return Response({
            'student': f"{payments[0].etudiant.nom} {payments[0].etudiant.prenom}" if payments else None,
            'groupe': groupe.nom_groupe,
            'subscription_price': groupe.prix_subscription,
            'payment_history': [{
                'id': payment.id,
                'date': payment.date_paiement,
                'montant': payment.montant,
                'frais_inscription': payment.frais_inscription,
                'total_paid': payment.montant + payment.frais_inscription,
                'remaining': payment.remaining,
                'status': payment.statut_paiement
            } for payment in payments],
            'latest_payment': {
                'montant': payments[0].montant,
                'remaining': payments[0].remaining,
                'status': payments[0].statut_paiement,
                'date': payments[0].date_paiement
            } if payments else None
        })
    except Groupe.DoesNotExist:
        return Response({'error': 'Group not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
""" -------------------------------------                Comissions          ---------------------------------------"""

class ComissionListView(generics.ListAPIView):
    queryset = Comission.objects.all()
    serializer_class = ComissionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['professeur', 'etudiant', 'groupe', 'statut_comission']
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






""" -------------------------------------                Users          ---------------------------------------"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import StaffRegisterSerializer, UserSerializer

class StaffRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    #permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated]
    serializer_class = StaffRegisterSerializer

class StaffProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer
from django.contrib.auth.models import User

class StaffChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Set the new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Optional: Invalidate all existing tokens
            # If you want to force re-login after password change

            return Response({
                "message": "Password updated successfully",
                "status": "success"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" -------------------------------------                Dashboard Metrics          ---------------------------------------"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .models import *

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def dashboard_metrics(request):
    now = timezone.now()
    last_month = now.date() - timedelta(days=30)

    try:
        # Student Metrics
        student_metrics = {
            'total_students': Etudiant.objects.count(),
            'total_male_students': Etudiant.objects.filter(sexe='M').count(),
            'total_female_students': Etudiant.objects.filter(sexe='F').count(),
            'students_by_nationality': Etudiant.objects.values('nationalite')\
                .annotate(count=Count('id')),
            'new_students_this_month': Etudiant.objects.filter(
                created_at__gte=last_month
            ).count(),
        }

        # Teacher Metrics
        teacher_metrics = {
            'total_teachers': Professeur.objects.count(),
            'teachers_by_gender': {
                'male': Professeur.objects.filter(sexe='M').count(),
                'female': Professeur.objects.filter(sexe='F').count()
            },
            'teachers_by_nationality': Professeur.objects.values('nationalite')\
                .annotate(count=Count('id')),
            'teachers_by_specialite': Professeur.objects.values('specialite')\
                .annotate(count=Count('id')),
        }

        # Group Metrics
        group_metrics = {
            'total_groups': Groupe.objects.count(),
            'students_per_group': EtudiantGroupe.objects.values('groupe')\
                .annotate(count=Count('etudiant')),
        }

        # Payment Metrics
        payment_metrics = {
            'total_payments': Paiement.objects.count(),
            'total_amount': Paiement.objects.aggregate(total=Sum('montant'))['total'] or 0,
            'payments_this_month': {
                'count': Paiement.objects.filter(date_paiement__gte=last_month).count(),
                'amount': Paiement.objects.filter(date_paiement__gte=last_month)\
                    .aggregate(total=Sum('montant'))['total'] or 0
            },
            'payment_status': Paiement.objects.values('statut_paiement')\
                .annotate(count=Count('id'))
        }

        # Commission Metrics
        commission_metrics = {
            'total_commissions': Comission.objects.count(),
            'total_commission_amount': Comission.objects.aggregate(
                total=Sum('montant'))['total'] or 0,
            'commissions_this_month': {
                'count': Comission.objects.filter(date_comission__gte=last_month).count(),
                'amount': Comission.objects.filter(date_comission__gte=last_month)\
                    .aggregate(total=Sum('montant'))['total'] or 0
            },
            'commission_status': Comission.objects.values('statut_comission')\
                .annotate(count=Count('id'))
        }



        dashboard_data = {
            'student_metrics': student_metrics,
            'teacher_metrics': teacher_metrics,
            'group_metrics': group_metrics,
            'payment_metrics': payment_metrics,
            'commission_metrics': commission_metrics,
            'last_updated': now.isoformat()
        }

        return Response(dashboard_data)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)
    

""" ------------------------------------------ Financial Views -----------------------------------------------"""
from rest_framework import viewsets
class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date']
    ordering_fields = ['date', 'montant']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date__date__range=[start_date, end_date])

        return queryset

class SortieBanqueViewSet(viewsets.ModelViewSet):
    queryset = SortieBanque.objects.all()
    serializer_class = SortieBanqueSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'mode_paiement']
    ordering_fields = ['date', 'montant']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date__date__range=[start_date, end_date])

        return queryset
    
@api_view(['GET'])
def financial_metrics_by_month(request):
    # Get the date range from query parameters or default to current year
    year = request.query_params.get('year', timezone.now().year)
    
    # Get all months data for the specified year
    months_data = []
    
    for month in range(1, 13):
        # Get the month name
        month_name = datetime(int(year), month, 1).strftime('%b')
        
        # Get total depenses for the month
        depenses = Depense.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        # Get total sorties for the month
        sorties = SortieBanque.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        # Get total income (paiements) for the month
        income = Paiement.objects.filter(
            date_paiement__year=year,
            date_paiement__month=month
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        months_data.append({
            'name': month_name,
            'depenses': depenses,
            'sorties-banque': sorties,
            'recettes': income
        })
    
    return Response({
        'year': year,
        'data': months_data
    })

@api_view(['GET'])
def weekly_financial_metrics(request):
    # Get the start and end date from query params or default to current week
    end_date = request.query_params.get('end_date', timezone.now().date())
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Calculate start date (6 days before end date to get a full week)
    start_date = end_date - timezone.timedelta(days=6)
    
    # Initialize data structure for the week
    days_data = []
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Loop through each day of the week
    current_date = start_date
    while current_date <= end_date:
        # Get day name
        day_name = day_names[current_date.weekday()]
        
        # Get total paiements for the day
        paiements = Paiement.objects.filter(
            date_paiement__date=current_date
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        # Get total commissions for the day
        commissions = Comission.objects.filter(
            date_comission__date=current_date
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        days_data.append({
            'name': day_name,
            'paiements': float(paiements),
            'commissions': float(commissions)
        })
        
        current_date += timezone.timedelta(days=1)
    
    return Response({
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'data': days_data
    })


""" ------------------------------------------ Detail of a Etudiant -----------------------------------------------"""

@api_view(['GET'])
def etudiant_details(request, pk):
    try:
        etudiant = Etudiant.objects.get(pk=pk)
        
        # Get all groups the student is in
        etudiant_groupes = EtudiantGroupe.objects.filter(etudiant=etudiant)
        
        groups_data = []
        for eg in etudiant_groupes:
            groupe = eg.groupe
            
            # Get matieres for this group
            matieres = GroupeMatiere.objects.filter(groupe=groupe)
            matieres_data = [{
                'id': gm.matiere.id,
                'nom_matiere': gm.matiere.nom_matiere
            } for gm in matieres]
            
            # Get professeurs for this group
            professeurs = GroupeProfesseur.objects.filter(groupe=groupe)
            professeurs_data = [{
                'id': gp.professeur.id,
                'nom': gp.professeur.nom,
                'prenom': gp.professeur.prenom,
                'commission_fixe': gp.commission_fixe
            } for gp in professeurs]
            
            groups_data.append({
                'id': groupe.id,
                'nom_groupe': groupe.nom_groupe,
                'niveau': {
                    'id': groupe.niveau.id,
                    'nom_niveau': groupe.niveau.nom_niveau
                },
                'filiere': {
                    'id': groupe.filiere.id,
                    'nom_filiere': groupe.filiere.nom_filiere
                },
                'matieres': matieres_data,
                'professeurs': professeurs_data
            })
        
        # Get all payments made by the student
        paiements = Paiement.objects.filter(etudiant=etudiant)
        paiements_data = [{
            'id': p.id,
            'montant': p.montant,
            'date_paiement': p.date_paiement,
            'statut_paiement': p.statut_paiement,
            'groupe': p.groupe.nom_groupe
        } for p in paiements]

        response_data = {
            'id': etudiant.id,
            'nom': etudiant.nom,
            'prenom': etudiant.prenom,
            'date_naissance': etudiant.date_naissance,
            'telephone': etudiant.telephone,
            'adresse': etudiant.adresse,
            'sexe': etudiant.sexe,
            'nationalite': etudiant.nationalite,
            'contact_urgence': etudiant.contact_urgence,
            'created_at': etudiant.created_at,
            'groupes': groups_data,
            'paiements': paiements_data,
            'total_paiements': sum(p.montant for p in paiements),
            'total_groupes': len(groups_data)
        }
        
        return Response(response_data)
        
    except Etudiant.DoesNotExist:
        return Response(
            {'error': 'Etudiant not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    

@api_view(['GET'])
def professeur_details(request, pk):
    try:
        professeur = Professeur.objects.get(pk=pk)
        
        # Get all groups the professor teaches
        groupe_professeurs = GroupeProfesseur.objects.filter(professeur=professeur)
        groups_data = []
        
        for gp in groupe_professeurs:
            groupe = gp.groupe
            
            # Get matieres for this group
            matieres = GroupeMatiere.objects.filter(groupe=groupe)
            matieres_data = [{
                'id': gm.matiere.id,
                'nom_matiere': gm.matiere.nom_matiere
            } for gm in matieres]
            
            # Get students for this group
            etudiants = EtudiantGroupe.objects.filter(groupe=groupe)
            etudiants_data = [{
                'id': eg.etudiant.id,
                'nom': eg.etudiant.nom,
                'prenom': eg.etudiant.prenom
            } for eg in etudiants]
            
            groups_data.append({
                'id': groupe.id,
                'nom_groupe': groupe.nom_groupe,
                'commission_fixe': gp.commission_fixe,
                'filiere': {
                    'id': groupe.filiere.id,
                    'nom_filiere': groupe.filiere.nom_filiere
                },
                'niveau': {
                    'id': groupe.niveau.id,
                    'nom_niveau': groupe.niveau.nom_niveau
                },
                'max_etudiants': groupe.max_etudiants,
                'matieres': matieres_data,
                'etudiants': etudiants_data,
                'total_etudiants': len(etudiants_data)
            })

        # Get all commissions for the professor
        commissions = Comission.objects.filter(professeur=professeur)
        commissions_data = [{
            'id': c.id,
            'montant': c.montant,
            'date_comission': c.date_comission,
            'statut_comission': c.statut_comission,
            'etudiant': {
                'id': c.etudiant.id,
                'nom': c.etudiant.nom,
                'prenom': c.etudiant.prenom
            },
            'groupe': {
                'id': c.groupe.id,
                'nom_groupe': c.groupe.nom_groupe
            }
        } for c in commissions]

        # Calculate total commissions
        total_commissions = commissions.aggregate(total=Sum('montant'))['total'] or 0

        response_data = {
            'id': professeur.id,
            'nom': professeur.nom,
            'prenom': professeur.prenom,
            'telephone': professeur.telephone,
            'adresse': professeur.adresse,
            'date_naissance': professeur.date_naissance,
            'sexe': professeur.sexe,
            'nationalite': professeur.nationalite,
            'specialite': professeur.specialite,
            'created_at': professeur.created_at,
            'groupes': groups_data,
            'commissions': commissions_data,
            'total_commissions': total_commissions,
            'total_groupes': len(groups_data)
        }
        
        return Response(response_data)
        
    except Professeur.DoesNotExist:
        return Response(
            {'error': 'Professeur not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )