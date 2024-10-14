from rest_framework import serializers
from .models import Etudiant, Professeur, Comission, Paiement
from .models import Niveau, Filiere, Matiere, Groupe, EtudiantGroupe





class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = '__all__'

class ProfesseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professeur
        fields = '__all__'

class ComissionSerializer(serializers.ModelSerializer):

    professeur = ProfesseurSerializer(read_only=True)
    etudiant   = EtudiantSerializer(read_only=True) 

    class Meta:
        model = Comission
        fields = ['id', 'montant', 'date_comission', 'statut_comission', 'professeur', 'etudiant']

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'

class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = '__all__'

class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = '__all__'

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'



class EtudiantGroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtudiantGroupe
        fields = '__all__'
        

class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = ['id', 'professeur', 'niveau', 'max_etudiants', 'filiere', 'matiere']

class GroupeDetailSerializer(serializers.ModelSerializer):

    professeur = ProfesseurSerializer(read_only=True)
    niveau     = NiveauSerializer(read_only=True)
    filiere    = FiliereSerializer(read_only=True)
    matiere    = MatiereSerializer(read_only=True)

    class Meta:
        model = Groupe
        fields = ['id', 'professeur', 'niveau', 'max_etudiants', 'filiere', 'matiere']


class GroupeWithEtudiantsSerializer(serializers.ModelSerializer):

    etudiants  = serializers.SerializerMethodField()
    professeur = ProfesseurSerializer(read_only=True)
    niveau     = NiveauSerializer(read_only=True)
    filiere    = FiliereSerializer(read_only=True)
    matiere    = MatiereSerializer(read_only=True)

    class Meta:
        model  = Groupe
        fields = ['id', 'professeur', 'niveau', 'max_etudiants', 'filiere', 'matiere', 'etudiants']

    # Custom method to retrieve students assigned to each group
    def get_etudiants(self, obj):
        etudiants_in_group = EtudiantGroupe.objects.filter(groupe=obj)
        return EtudiantSerializer([eg.etudiant for eg in etudiants_in_group], many=True).data


""" ---------------------------------------  Update Serializer for Paiement ------------------------------------"""

from rest_framework import serializers
from .models import Paiement, Comission, Groupe

class PaiementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paiement
        fields = ['id', 'montant', 'date_paiement', 'statut_paiement', 'etudiant', 'groupe', 'commission_percentage']

    def validate(self, data):
        """
        Ensure that the student belongs to the specific groupe
        """
        etudiant = data['etudiant']
        groupe   = data['groupe']

        if not EtudiantGroupe.objects.filter(etudiant=etudiant, groupe=groupe).exists():
            raise serializers.ValidationError(
                {"detail": f"The student with ID {etudiant.id} is not assigned to the group with ID {groupe.id}."}
            )
        return data

    def create(self, validated_data):
        # Create the Paiement object
        paiement = Paiement.objects.create(**validated_data)

        # Fetch the group and its professor directly using groupe_id from the paiement
        groupe = paiement.groupe  # Get the group directly from the payment
        professeur = self.get_professeur_for_groupe(groupe)  # Fetch the professor for the specified group

        # Generate the commission for the professor
        if professeur:
            commission_amount = self.calculate_commission_amount(paiement.montant, paiement.commission_percentage)
            Comission.objects.create(
                montant=commission_amount,
                date_comission=paiement.date_paiement,  # Set the date to payment date
                statut_comission=paiement.statut_paiement,  # The Same 
                professeur=professeur,
                etudiant=paiement.etudiant  # Link the same student
            )

        return paiement

    def get_professeur_for_groupe(self, groupe):
        """
        Retrieve the professor for a specific group.
        """
        try:
            return groupe.professeur  # Directly get the professor linked to the group
        except Groupe.DoesNotExist:
            return None

    def calculate_commission_amount(self, paiement_amount, commission_percentage):
        # Calculate the commission amount based on the percentage
        return paiement_amount * (commission_percentage / 100)





""" ---------------------------------------  Detail Serializer for Etudiant ------------------------------------"""

class EtudiantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'date_naissance', 'groupes', 'paiements']

    groupes   = serializers.SerializerMethodField()
    paiements = serializers.SerializerMethodField()

    def get_groupes(self, obj):
        etudiant_groupes = EtudiantGroupe.objects.filter(etudiant=obj)
        return [{
            'id': eg.groupe.id,
            'matiere': eg.groupe.matiere.nom_matiere,
            'filiere':eg.groupe.filiere.nom_filiere,
            'niveau': eg.groupe.niveau.nom_niveau,
            'professeur': f"{eg.groupe.professeur.nom} {eg.groupe.professeur.prenom}"
        } for eg in etudiant_groupes]
    
    def get_paiements(self, obj):
        paiements = Paiement.objects.filter(etudiant=obj)
        return [{
            'id': p.id,
            'montant': p.montant,
            'date_paiement': p.date_paiement,
            'statut_paiement': p.statut_paiement,
            'groupe': p.groupe.id,
            'commission_percentage': p.commission_percentage
        } for p in paiements]




