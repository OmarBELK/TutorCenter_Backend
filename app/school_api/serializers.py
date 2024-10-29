from os import write
from rest_framework import serializers
from .models import Etudiant, Professeur, Comission, Paiement
from .models import Niveau, Filiere, Matiere, Groupe, EtudiantGroupe
from rest_framework import serializers
from .models import Paiement, Comission, Groupe, Event




# class EtudiantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Etudiant
#         fields = '__all__'


class EtudiantSerializer(serializers.ModelSerializer):

    groupe_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'date_naissance', 'groupe_id', 'telephone', 'adresse', 'sexe', 'nationalite', 'contact_urgence', 'created_at']

    def create(self, validated_data):
        groupe_id = validated_data.pop('groupe_id', None)
        etudiant  = Etudiant.objects.create(**validated_data)
        if groupe_id:
            groupe = Groupe.objects.get(pk=groupe_id)
            EtudiantGroupe.objects.create(etudiant=etudiant, groupe=groupe)
        return etudiant 


class EtudiantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'date_naissance','telephone', 'adresse', 'sexe', 'nationalite', 'contact_urgence','groupes', 'paiements', 'created_at']

    groupes   = serializers.SerializerMethodField()
    paiements = serializers.SerializerMethodField()

    def get_groupes(self, obj):
        etudiant_groupes = EtudiantGroupe.objects.filter(etudiant=obj)
        return [{
            'id': eg.groupe.id,
            'nom_groupe': eg.groupe.nom_groupe,
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



class ProfesseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professeur
        fields = '__all__'


class ProfesseurDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professeur
        fields = ['id', 'nom', 'prenom', 'telephone', 'adresse', 'date_naissance', 'sexe', 'nationalite', 'specialite', 'groupes', 'commissions', 'created_at']

    groupes    = serializers.SerializerMethodField()
    commissions = serializers.SerializerMethodField()

    def get_groupes(self, obj):
        groupes = Groupe.objects.filter(professeur=obj)
        return [{
            'id': g.id,
            'nom_groupe': g.nom_groupe,
            'matiere': g.matiere.nom_matiere,
            'filiere': g.filiere.nom_filiere,
            'niveau': g.niveau.nom_niveau,
            'max_etudiants': g.max_etudiants,
            'commission_fixe': g.commission_fixe,
        } for g in groupes]

    def get_commissions(self, obj):
        commissions = Comission.objects.filter(professeur=obj)
        return [{
            'id': c.id,
            'montant': c.montant,
            'date_comission': c.date_comission,
            'statut_comission': c.statut_comission,
            'etudiant': f"{c.etudiant.nom} {c.etudiant.prenom}",
            'groupe': c.groupe.id,
        } for c in commissions]
        

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
        fields = ['id', 'nom_groupe', 'professeur', 'niveau', 'max_etudiants', 'filiere', 'matiere', 'commission_fixe']

class GroupeDetailSerializer(serializers.ModelSerializer):

    professeur = ProfesseurSerializer(read_only=True)
    niveau     = NiveauSerializer(read_only=True)
    filiere    = FiliereSerializer(read_only=True)
    matiere    = MatiereSerializer(read_only=True)

    class Meta:
        model = Groupe
        fields = ['id','nom_groupe', 'professeur', 'commission_fixe','niveau', 'max_etudiants', 'filiere', 'matiere']


class GroupeWithEtudiantsSerializer(serializers.ModelSerializer):

    etudiants  = serializers.SerializerMethodField()
    professeur = ProfesseurSerializer(read_only=True)
    niveau     = NiveauSerializer(read_only=True)
    filiere    = FiliereSerializer(read_only=True)
    matiere    = MatiereSerializer(read_only=True)

    class Meta:
        model  = Groupe
        fields = ['id', 'nom_groupe', 'professeur', 'niveau', 'max_etudiants', 'filiere', 'matiere', 'etudiants']

    # Custom method to retrieve students assigned to each group
    def get_etudiants(self, obj):
        etudiants_in_group = EtudiantGroupe.objects.filter(groupe=obj)
        return EtudiantSerializer([eg.etudiant for eg in etudiants_in_group], many=True).data


""" ---------------------------------------  Update Serializer for Paiement ------------------------------------"""


class PaiementSerializer(serializers.ModelSerializer):
    etudiant_id = serializers.IntegerField(write_only=True)
    groupe_id = serializers.IntegerField(write_only=True)

    etudiant = EtudiantSerializer(read_only=True)
    groupe   = GroupeSerializer(read_only=True)

    class Meta:
        model = Paiement
        fields = ['id', 'montant', 'date_paiement', 'statut_paiement','etudiant', 'groupe', 'etudiant_id', 'groupe_id', 'commission_percentage']

    def validate(self, data):
        etudiant_id = data.get('etudiant_id')
        groupe_id = data.get('groupe_id')

        try:
            etudiant = Etudiant.objects.get(pk=etudiant_id)
            groupe = Groupe.objects.get(pk=groupe_id)
        except (Etudiant.DoesNotExist, Groupe.DoesNotExist):
            raise serializers.ValidationError("Invalid etudiant_id or groupe_id")

        if not EtudiantGroupe.objects.filter(etudiant=etudiant, groupe=groupe).exists():
            raise serializers.ValidationError(
                f"The student with ID {etudiant_id} is not assigned to the group with ID {groupe_id}."
            )
        return data

    def create(self, validated_data):
        etudiant_id = validated_data.pop('etudiant_id')
        groupe_id = validated_data.pop('groupe_id')
        etudiant = Etudiant.objects.get(pk=etudiant_id)
        groupe = Groupe.objects.get(pk=groupe_id)

        paiement = Paiement.objects.create(etudiant=etudiant, groupe=groupe, **validated_data)

        professeur = groupe.professeur
        if professeur:
            commission_amount = self.calculate_commission_amount(paiement.montant, groupe.commission_fixe, paiement.commission_percentage)
            Comission.objects.create(
                montant=commission_amount,
                date_comission=paiement.date_paiement,
                statut_comission=paiement.statut_paiement,
                professeur=professeur,
                etudiant=etudiant,
                groupe=groupe
            )
        return paiement
    
    def calculate_commission_amount(self, paiement_amount, commission_fixe, commission_percentage):
        commission_base = min(paiement_amount, commission_fixe)
        return commission_base * (commission_percentage / 100)

class ComissionSerializer(serializers.ModelSerializer):

    professeur = ProfesseurSerializer(read_only=True)
    etudiant   = EtudiantSerializer(read_only=True) 
    groupe     = GroupeSerializer(read_only=True)

    class Meta:
        model = Comission
        fields = ['id', 'montant', 'date_comission', 'statut_comission', 'professeur', 'etudiant', 'groupe']



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'start_time', 'end_time', 'description', 'groupe', 'professeur']    


"""---------------------------------------  Serializer for USERS  ------------------------------------"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class StaffRegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value

    def validate_new_password(self, value):
        # You can add custom password validation here if needed
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if value.isdigit():
            raise serializers.ValidationError("Password cannot be entirely numeric")
        return value