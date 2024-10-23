from django.shortcuts import render

# from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


""" ------------------------------------------------- Etudiant Views ----------------------------------------------------"""
from .models import *
from .serializers import *

@api_view(['GET', 'POST'])
def list_create_etudiant(request):
    """
    List all students or create a new student.

    GET:
    - If 'id' is provided in query params, returns details of a specific student.
    - Otherwise, returns a list of all students with their details.

    POST:
    - Creates a new student.

    Returns:
    - 200 OK: Successful GET request
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    - 404 Not Found: Student with given ID not found
    """
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
            serializer = EtudiantSerializer(etudiants, many=True)
            return Response(serializer.data)
        
    elif request.method == 'POST':
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


@api_view(['PUT', 'DELETE'])
def update_delete_etudiant(request):
    """
    Update or delete a student.

    PUT:
    - Updates details of a specific student.

    DELETE:
    - Deletes a specific student.

    Required:
    - 'id' in query parameters

    Returns:
    - 200 OK: Successful PUT request
    - 204 No Content: Successful DELETE request
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Student with given ID not found
    """
    id = request.query_params.get('id')
    if not id:
        return Response({"error": "ID is required in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        etudiant = Etudiant.objects.get(pk=id)
    except Etudiant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EtudiantSerializer(etudiant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        etudiant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

""" -------------------------------------     Professeur    -----------------------------------"""

@api_view(['GET', 'POST'])
def list_create_professeur(request):
    """
    List all professors or create a new professor.

    GET:
    - If 'id' is provided in query params, returns details of a specific professor.
    - Otherwise, returns a list of all professors with their details.

    POST:
    - Creates a new professor.

    Returns:
    - 200 OK: Successful GET request
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    - 404 Not Found: Professor with given ID not found
    """
    if request.method == 'GET':
        if 'id' in request.query_params:
            id = int(request.query_params['id'])
            try:
                professeur = Professeur.objects.get(pk=id)
                serializer = ProfesseurDetailSerializer(professeur)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Professeur.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # Get all professors with details
            professeurs = Professeur.objects.all()
            serializer = ProfesseurSerializer(professeurs, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProfesseurSerializer(data=request.data)
        if serializer.is_valid():
            professeur = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def update_delete_professeur(request):
    """
    Update or delete a professor.

    PUT:
    - Updates details of a specific professor.

    DELETE:
    - Deletes a specific professor.

    Required:
    - 'id' in query parameters

    Returns:
    - 200 OK: Successful PUT request
    - 204 No Content: Successful DELETE request
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Professor with given ID not found
    """
    id = request.query_params.get('id')
    if not id:
        return Response({"error": "ID is required in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        professeur = Professeur.objects.get(pk=id)
    except Professeur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProfesseurSerializer(professeur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        professeur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" -------------------------------------     Niveau    ---------------------------------------"""

@api_view(['GET', 'POST'])
def list_create_niveau(request):
    """
    List all levels (niveaux) or create a new level.

    GET:
    - Returns a list of all levels.

    POST:
    - Creates a new level.

    Returns:
    - 200 OK: Successful GET request
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
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


@api_view(['PUT', 'DELETE'])
def update_delete_niveau(request):
    """
    Update or delete a level.

    PUT:
    - Updates details of a specific level.

    DELETE:
    - Deletes a specific level.

    Required:
    - 'id' in query parameters

    Returns:
    - 200 OK: Successful PUT request
    - 204 No Content: Successful DELETE request
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Level with given ID not found
    """
    id = request.query_params.get('id')
    if not id:
        return Response({"error": "ID is required in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        niveau = Niveau.objects.get(pk=id)
    except Niveau.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = NiveauSerializer(niveau, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        niveau.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




""" -------------------------------------     Filiere    ---------------------------------------"""

@api_view(['GET', 'POST'])
def list_create_filiere(request):
    """
    List all filieres (branches) or create a new fieliere.

    GET:
    - Returns a list of all fielieres.

    POST:
    - Creates a new filiere.

    Returns:
    - 200 OK: Successful GET request
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
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

@api_view(['PUT', 'DELETE'])
def update_delete_filiere(request):
    """
    Update or delete a filiere.

    PUT:
    - Updates details of a specific filiere.

    DELETE:
    - Deletes a specific filiere.

    Required:
    - 'id' in query parameters

    Returns:
    - 200 OK: Successful PUT request
    - 204 No Content: Successful DELETE request
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Filiere with given ID not found
    """
    id = request.query_params.get('id')
    if not id:
        return Response({"error": "ID is required in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        filiere = Filiere.objects.get(pk=id)
    except Filiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = FiliereSerializer(filiere, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        filiere.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

""" -------------------------------------     Matiere    ---------------------------------------"""



@api_view(['GET', 'POST'])
def list_create_matiere(request):
    """
    List all subjects (matieres) or create a new subject.

    GET:
    - Returns a list of all subjects.

    POST:
    - Creates a new subject.

    Returns:
    - 200 OK: Successful GET request
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """
    if request.method == 'GET':
        matieres = Matiere.objects.all()
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MatiereSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def update_delete_matiere(request):
    """
    Update or delete a matiere (subject).

    PUT:
    - Updates details of a specific matiere.

    DELETE:
    - Deletes a specific matiere.

    Required:
    - 'id' in query parameters

    Returns:
    - 200 OK: Successful PUT request
    - 204 No Content: Successful DELETE request
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Matiere with given ID not found
    """
    id = request.query_params.get('id')
    if not id:
        return Response({"error": "ID is required in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        matiere = Matiere.objects.get(pk=id)
    except Matiere.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = MatiereSerializer(matiere, data=request.data)
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
    """
    List all groups or create a new group.

    GET:
    - Returns a list of all groups with their details.

    POST:
    - Creates a new group.

    Returns:
    - 200 OK: Successful GET request
    - 201 Created: Successful POST request
    - 400 Bad Request: Invalid data in POST request
    """

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
    



@api_view(['PUT', 'DELETE'])
def update_delete_groupe(request):
    """
    Update or delete a group.

    PUT:
    - Updates details of a specific group.

    DELETE:
    - Deletes a specific group.

    Required:
    - 'id' in query parameters

    Returns:
    - 200 OK: Successful PUT request
    - 204 No Content: Successful DELETE request
    - 400 Bad Request: Invalid data in PUT request
    - 404 Not Found: Group with given ID not found
    """
    id = request.query_params.get('id')
    if not id:
        return Response({"error": "ID is required in query parameters"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        groupe = Groupe.objects.get(pk=id)
    except Groupe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = GroupeSerializer(groupe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
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

# @api_view(['GET'])
# def list_groupes_with_etudiants(request):
#     if request.method == 'GET':
#         groupes = Groupe.objects.all()
#         serializer = GroupeWithEtudiantsSerializer(groupes, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# @api_view(['POST'])
# def groupe_with_etudiants(request):
#     id = request.data['id']
#     try:
#         groupe = Groupe.objects.get(pk = id)
#     except Groupe.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#     serializer = GroupeWithEtudiantsSerializer(groupe)
#     return Response(serializer.data, status=status.HTTP_200_OK)


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
    """
    List all commissions.

    GET:
    - Returns a list of all commissions with their details.

    Returns:
    - 200 OK: Successful GET request
    - 400 Bad Request: Invalid request method
    """

    if request.method == 'GET':
        comissions = Comission.objects.all()
        serializer = ComissionSerializer(comissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST) 



""" -------------------------------------                Event          ---------------------------------------"""

@api_view(['GET', 'POST'])
def list_create_event(request):
    if request.method == 'GET':
        events = Event.objects.all()
        groupe_id = request.query_params.get('groupe_id')
        professeur_id = request.query_params.get('professeur_id')

        if groupe_id:
            events = events.filter(groupe_id=groupe_id)
        if professeur_id:
            events = events.filter(professeur_id=professeur_id)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def update_delete_event(request):
    pk = request.query_params.get('pk')
    if not pk:
        return Response({"error": "Event ID (pk) is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)











