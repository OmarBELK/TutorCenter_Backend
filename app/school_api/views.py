from django.shortcuts import render

# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


""" ------------------------------------------------- Etudiant Views ----------------------------------------------------"""
from .models import *
from .serializers import *

# @api_view(['GET','POST'])
# def etudiant_list_create(request):    
#     if request.method == 'GET':
#         etudiants = Etudiant.objects.all()
#         serializer = EtudiantSerializer(etudiants, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = EtudiantSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','POST'])
def list_create_etudiants(request):    
    if request.method == 'GET':
        if 'id' in request.query_params:
            id = int(request.query_params['id'])
            try:
                etudiant = Etudiant.objects.get(pk=id)
                serializer = EtudiantDetailSerializer(etudiant)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except Etudiant.DoesNotExist:
                return Response(status = status.HTTP_404_NOT_FOUND)
        else:
            # Get all students with details
            etudiants = Etudiant.objects.all()
            serializer = EtudiantDetailSerializer(etudiants, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EtudiantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
def etudiant_detail(request):
    id = int(request.data['id'])
    try:
        etudiant = Etudiant.objects.get(pk=id)
    except Etudiant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EtudiantSerializer(etudiant)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EtudiantSerializer(etudiant, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        etudiant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






""" -------------------------------------     Professeur    -----------------------------------"""

@api_view(['GET', 'POST'])
def professeur_list(request):
    if request.method =='GET':
        professeurs = Professeur.objects.all()
        serializer = ProfesseurSerializer(professeurs, many=True)
        print('serializer: ',serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProfesseurSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
def professeur_detail(request):
    id = request.data['id']    
    try:
        professeur = Professeur.objects.get(pk=id)
    except Professeur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProfesseurSerializer(professeur, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ProfesseurSerializer(request.data, professeur)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        professeur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" -------------------------------------     Niveau    ---------------------------------------"""

@api_view(['GET', 'POST'])
def niveau_list(request):
    if request.method == 'GET':
        niveaux = Niveau.objects.all()
        serializer = NiveauSerializer(niveaux, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NiveauSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def niveau_detail(request):
    id = request.data['id']
    try:
        niveau = Niveau.objects.get(pk=id)
    except Niveau.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = NiveauSerializer(niveau)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = NiveauSerializer(request.data, niveau)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        niveau.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




""" -------------------------------------     Filiere    ---------------------------------------"""

@api_view(['GET', 'POST'])
def filiere_list(request):
    if request.method == 'GET':
        filieres = Filiere.objects.all()
        serializer = FiliereSerializer(filieres, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FiliereSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def filiere_detail(request):
    id = request.data['id']
    try:
        filiere = Filiere.objects.get(pk=id)
    except Niveau.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FiliereSerializer(filiere)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FiliereSerializer(request.data, filiere)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        filiere.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
""" -------------------------------------     Matiere    ---------------------------------------"""



@api_view(['GET', 'POST'])
def matiere_list(request):
    if request.method == 'GET':
        matieres = Matiere.objects.all()
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MatiereSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def matiere_detail(request):
    id = request.data['id']
    try:
        matiere = Matiere.objects.get(pk=id)
    except Matiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MatiereSerializer(matiere)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MatiereSerializer(request.data, Matiere)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        matiere.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


""" -------------------------------------     Groupe    ---------------------------------------"""


@api_view(['GET', 'POST'])
def list_create_groupe(request):
    if request.method == 'GET':
        groupes = Groupe.objects.all()
        serializer = GroupeDetailSerializer(groupes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = GroupeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET', 'PUT', 'DELETE'])
def groupe_detail(request):
    id = request.data['id']
    # Fetch the Groupe object, or return 404 if not found
    groupe = get_object_or_404(Groupe, pk=id)
    
    if request.method == 'GET':
        serializer = GroupeDetailSerializer(groupe)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = GroupeSerializer(request.data, groupe)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        groupe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
""" -------------------------------------     Etudiant - Groupe    ---------------------------------------"""
from rest_framework.exceptions import ValidationError

# @api_view(['POST'])
# def assign_etudiant_group(request):
#     """
#     Handle assigning etudiant to groupe.
#     - POST: Assign a student to an existing groupe
#     """
#     # Deserialize the incoming data
#     serializer = EtudiantGroupeSerializer(data=request.data)
#     try:
#         # This will raise a validation error if the unique constraint is violated
#         serializer.is_valid(raise_exception=True)

#         # Check if the student is already assigned to this group manually
#         etudiant_id = serializer.validated_data['etudiant'].id
#         groupe_id = serializer.validated_data['groupe'].id


#         existing_assignment = EtudiantGroupe.objects.filter(etudiant_id=etudiant_id, groupe_id=groupe_id).exists()
#         print("existing_assignment" ,existing_assignment)

#         if existing_assignment:
#             return Response(
#                 {"error": "This student is already assigned to this group."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Save the new EtudiantGroupe entry
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     except ValidationError as e:
#         # Handle validation errors and provide a custom error message
#         return Response(
#             {"error": "This student is already assigned to this group."},
#             status=status.HTTP_400_BAD_REQUEST
#         )


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
    if request.method == 'GET':
        groupes = Groupe.objects.all()
        serializer = GroupeWithEtudiantsSerializer(groupes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def groupe_with_etudiants(request):
    id = request.data['id']
    try:
        groupe = Groupe.objects.get(pk = id)
    except Groupe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = GroupeWithEtudiantsSerializer(groupe)
    return Response(serializer.data, status=status.HTTP_200_OK)




""" -------------------------------------                Paiement          ---------------------------------------"""

@api_view(['GET', 'POST'])
def list_create_paiement(request):
    """
    Handle both listing and creating paiements.
    - GET: List all paiements.
    - POST: Create a new paiement, and automatically generate a commission for the professor
            associated with the specified group.
    """
    # Handle GET request: List all payments
    if request.method == 'GET':
        paiements = Paiement.objects.all()
        serializer = PaiementSerializer(paiements, many=True)
        return Response(serializer.data)

    # Handle POST request: Create a new payment
    elif request.method == 'POST':
        serializer = PaiementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will create the payment and trigger the auto-creation of the commission
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

""" -------------------------------------                Comissions          ---------------------------------------"""


@api_view(['GET'])
def list_comissions(request):

    if request.method == 'GET':
        comissions = Comission.objects.all()
        serializer = ComissionSerializer(comissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST) 


""" -------------------------------------                Etudiant Details          ---------------------------------------"""

