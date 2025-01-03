from os import write
from rest_framework import serializers
from .models import *


class EtudiantSerializer(serializers.ModelSerializer):

    groupe_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'date_naissance', 'groupe_id', 'telephone', 'adresse', 'sexe', 'nationalite', 'contact_urgence', 'etablissement', 'created_at']

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
            'matieres': [{
                'id': gm.matiere.id,
                'nom_matiere': gm.matiere.nom_matiere
            } for gm in GroupeMatiere.objects.filter(groupe=eg.groupe)],
            'filiere': eg.groupe.filiere.nom_filiere,
            'niveau': eg.groupe.niveau.nom_niveau,
            'professeurs': [{
                'id': gp.professeur.id,
                'nom': gp.professeur.nom,
                'prenom': gp.professeur.prenom,
                'commission_fixe': gp.commission_fixe
            } for gp in GroupeProfesseur.objects.filter(groupe=eg.groupe)]
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
        fields = ['id', 'nom', 'prenom', 'telephone', 'adresse', 'date_naissance', 
                 'sexe', 'nationalite', 'specialite', 'groupes', 'commissions', 'created_at']

    groupes = serializers.SerializerMethodField()
    commissions = serializers.SerializerMethodField()

    def get_groupes(self, obj):
        groupe_professeurs = GroupeProfesseur.objects.filter(professeur=obj)
        return [{
            'id': gp.groupe.id,
            'nom_groupe': gp.groupe.nom_groupe,
            'commission_fixe': gp.commission_fixe,
            'filiere': gp.groupe.filiere.nom_filiere,
            'niveau': gp.groupe.niveau.nom_niveau,
            'max_etudiants': gp.groupe.max_etudiants,
            'matieres': [{
                'id': gm.matiere.id,
                'nom_matiere': gm.matiere.nom_matiere
            } for gm in GroupeMatiere.objects.filter(groupe=gp.groupe)]
        } for gp in groupe_professeurs]

    def get_commissions(self, obj):
        commissions = Comission.objects.filter(professeur=obj)
        return [{
            'id': c.id,
            'montant': c.montant,
            'date_comission': c.date_comission,
            'statut_comission': c.statut_comission,
            'etudiant': f"{c.etudiant.nom} {c.etudiant.prenom}",
            'groupe': {
                'id': c.groupe.id,
                'nom_groupe': c.groupe.nom_groupe
            }
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
        fields = ['id', 'etudiant', 'groupe', 'date_inscription']
        
    def validate(self, data):
        """
        Check that the student isn't already in the group and the group isn't full
        """
        etudiant = data['etudiant']
        groupe = data['groupe']
        
        # Check if student is already in this group
        if EtudiantGroupe.objects.filter(etudiant=etudiant, groupe=groupe).exists():
            raise serializers.ValidationError(
                f"Student is already assigned to group {groupe.nom_groupe}"
            )
            
        # Check if group has space
        current_students = EtudiantGroupe.objects.filter(groupe=groupe).count()
        if current_students >= groupe.max_etudiants:
            raise serializers.ValidationError(
                f"Group {groupe.nom_groupe} is full ({groupe.max_etudiants} students maximum)"
            )
            
        return data


""" -------- These are two new serializers for the many to many relationship between groupe and professeur and groupe and matiere --------"""

class GroupeProfesseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeProfesseur
        fields = ['id', 'groupe', 'professeur', 'commission_fixe', 'created_at']

class GroupeMatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeMatiere
        fields = ['id', 'groupe', 'matiere', 'created_at']





class GroupeSerializer(serializers.ModelSerializer):
    professeurs = serializers.SerializerMethodField()
    matieres = serializers.SerializerMethodField()

    class Meta:
        model = Groupe
        fields = ['id', 'nom_groupe', 'niveau', 'max_etudiants', 'prix_subscription',
                 'filiere', 'professeurs', 'matieres', 'created_at']

    def get_professeurs(self, obj):
        groupe_professeurs = GroupeProfesseur.objects.filter(groupe=obj)
        return [{
            'id': gp.professeur.id,
            'nom': gp.professeur.nom,
            'prenom': gp.professeur.prenom,
            'commission_fixe': gp.commission_fixe
        } for gp in groupe_professeurs]

    def get_matieres(self, obj):
        groupe_matieres = GroupeMatiere.objects.filter(groupe=obj)
        return [{
            'id': gm.matiere.id,
            'nom_matiere': gm.matiere.nom_matiere
        } for gm in groupe_matieres]


class GroupeDetailSerializer(serializers.ModelSerializer):
    professeurs = serializers.SerializerMethodField()
    matieres = serializers.SerializerMethodField()
    niveau = NiveauSerializer(read_only=True)
    filiere = FiliereSerializer(read_only=True)

    class Meta:
        model = Groupe
        fields = ['id', 'nom_groupe', 'prix_subscription', 'niveau', 'max_etudiants', 
                 'filiere', 'professeurs', 'matieres', 'created_at']

    def get_professeurs(self, obj):
        groupe_professeurs = GroupeProfesseur.objects.filter(groupe=obj)
        return [{
            'id': gp.professeur.id,
            'nom': gp.professeur.nom,
            'prenom': gp.professeur.prenom,
            'commission_fixe': gp.commission_fixe
        } for gp in groupe_professeurs]

    def get_matieres(self, obj):
        groupe_matieres = GroupeMatiere.objects.filter(groupe=obj)
        return [{
            'id': gm.matiere.id,
            'nom_matiere': gm.matiere.nom_matiere
        } for gm in groupe_matieres]



class GroupeWithEtudiantsSerializer(serializers.ModelSerializer):
    etudiants = serializers.SerializerMethodField()
    professeurs = serializers.SerializerMethodField()
    matieres = serializers.SerializerMethodField()
    niveau = NiveauSerializer(read_only=True)
    filiere = FiliereSerializer(read_only=True)

    class Meta:
        model = Groupe
        fields = ['id', 'nom_groupe', 'professeurs', 'niveau', 
                 'max_etudiants', 'filiere', 'matieres', 'etudiants']

    def get_etudiants(self, obj):
        etudiants_in_group = EtudiantGroupe.objects.filter(groupe=obj)
        return EtudiantSerializer([eg.etudiant for eg in etudiants_in_group], many=True).data

    def get_professeurs(self, obj):
        groupe_professeurs = GroupeProfesseur.objects.filter(groupe=obj)
        return [{
            'id': gp.professeur.id,
            'nom': gp.professeur.nom,
            'prenom': gp.professeur.prenom,
            'commission_fixe': gp.commission_fixe
        } for gp in groupe_professeurs]

    def get_matieres(self, obj):
        groupe_matieres = GroupeMatiere.objects.filter(groupe=obj)
        return [{
            'id': gm.matiere.id,
            'nom_matiere': gm.matiere.nom_matiere
        } for gm in groupe_matieres]

""" ---------------------------------------  Update Serializer for Paiement ------------------------------------"""
class GroupeBasicSerializer(serializers.ModelSerializer):
    niveau_info = serializers.SerializerMethodField()
    filiere_info = serializers.SerializerMethodField()

    class Meta:
        model = Groupe
        fields = ['id', 'nom_groupe', 'niveau', 'max_etudiants', 'prix_subscription', 'filiere', 'niveau_info', 'filiere_info']

    def get_niveau_info(self, obj):
        return {
            'id': obj.niveau.id,
            'nom_niveau': obj.niveau.nom_niveau
        }

    def get_filiere_info(self, obj):
        return {
            'id': obj.filiere.id,
            'nom_filiere': obj.filiere.nom_filiere
        }
        
class PaiementSerializer(serializers.ModelSerializer):
    etudiant_id = serializers.IntegerField(write_only=True)
    groupe_id = serializers.IntegerField(write_only=True)
    etudiant = EtudiantSerializer(read_only=True)
    groupe = GroupeBasicSerializer(read_only=True)
    month_name = serializers.SerializerMethodField()

    class Meta:
        model = Paiement
        fields = [
            'id', 
            'montant',              # Total amount paid
            'montant_total',        # Subscription price
            'remaining',            # Remaining amount
            'frais_inscription',    # Registration fee
            'date_paiement',
            'mois_paiement',        # YYYY-MM format
            'month_name',           # French month name
            'statut_paiement',
            'etudiant',
            'groupe',
            'etudiant_id',
            'groupe_id'
        ]

    def get_month_name(self, obj):
        month_names = {
            '01': 'Janvier', '02': 'Février', '03': 'Mars',
            '04': 'Avril', '05': 'Mai', '06': 'Juin',
            '07': 'Juillet', '08': 'Août', '09': 'Septembre',
            '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
        }
        try:
            month = obj.mois_paiement.split('-')[1]
            return month_names.get(month, '')
        except:
            return ''

    def validate(self, data):
        etudiant_id = data.get('etudiant_id')
        groupe_id = data.get('groupe_id')

        try:
            etudiant = Etudiant.objects.get(pk=etudiant_id)
            groupe = Groupe.objects.get(pk=groupe_id)

            if not EtudiantGroupe.objects.filter(
                etudiant=etudiant, 
                groupe=groupe
            ).exists():
                raise serializers.ValidationError(
                    f"The student with ID {etudiant_id} is not assigned to the group with ID {groupe_id}."
                )

        except (Etudiant.DoesNotExist, Groupe.DoesNotExist):
            raise serializers.ValidationError("Invalid etudiant_id or groupe_id")

        return data

    def create(self, validated_data):
        etudiant_id = validated_data.pop('etudiant_id')
        groupe_id = validated_data.pop('groupe_id')
        etudiant = Etudiant.objects.get(pk=etudiant_id)
        groupe = Groupe.objects.get(pk=groupe_id)

        paiement = Paiement.objects.create(
            etudiant=etudiant, 
            groupe=groupe, 
            **validated_data
        )

        # Create commission for each professor in the group
        groupe_professeurs = GroupeProfesseur.objects.filter(groupe=groupe)
        for gp in groupe_professeurs:
            commission_amount = self.calculate_commission_amount(
                paiement.montant, 
                gp.commission_fixe, 
                paiement.commission_percentage
            )
            Comission.objects.create(
                montant=commission_amount,
                date_comission=paiement.date_paiement,
                statut_comission=paiement.statut_paiement,
                professeur=gp.professeur,
                etudiant=etudiant,
                groupe=groupe
            )
        return paiement
    
    def calculate_commission_amount(self, paiement_amount, commission_fixe, commission_percentage):
        commission_base = min(paiement_amount, commission_fixe)
        return commission_base * (commission_percentage / 100)

# class PaiementSerializer(serializers.ModelSerializer):
#     etudiant_id = serializers.IntegerField(write_only=True)
#     groupe_id = serializers.IntegerField(write_only=True)

#     etudiant = EtudiantSerializer(read_only=True)
#     groupe   = GroupeSerializer(read_only=True)

#     class Meta:
#         model = Paiement
#         fields = ['id', 'montant', 'date_paiement', 'statut_paiement','etudiant', 'groupe', 'etudiant_id', 'groupe_id', 'commission_percentage']

#     def validate(self, data):
#         etudiant_id = data.get('etudiant_id')
#         groupe_id = data.get('groupe_id')

#         try:
#             etudiant = Etudiant.objects.get(pk=etudiant_id)
#             groupe = Groupe.objects.get(pk=groupe_id)
#         except (Etudiant.DoesNotExist, Groupe.DoesNotExist):
#             raise serializers.ValidationError("Invalid etudiant_id or groupe_id")

#         if not EtudiantGroupe.objects.filter(etudiant=etudiant, groupe=groupe).exists():
#             raise serializers.ValidationError(
#                 f"The student with ID {etudiant_id} is not assigned to the group with ID {groupe_id}."
#             )
#         return data

#     def create(self, validated_data):
#         etudiant_id = validated_data.pop('etudiant_id')
#         groupe_id = validated_data.pop('groupe_id')
#         etudiant = Etudiant.objects.get(pk=etudiant_id)
#         groupe = Groupe.objects.get(pk=groupe_id)

#         paiement = Paiement.objects.create(etudiant=etudiant, groupe=groupe, **validated_data)

#         # Create commission for each professor in the group
#         groupe_professeurs = GroupeProfesseur.objects.filter(groupe=groupe)
#         for gp in groupe_professeurs:
#             commission_amount = self.calculate_commission_amount(
#                 paiement.montant, 
#                 gp.commission_fixe, 
#                 paiement.commission_percentage
#             )
#             Comission.objects.create(
#                 montant=commission_amount,
#                 date_comission=paiement.date_paiement,
#                 statut_comission=paiement.statut_paiement,
#                 professeur=gp.professeur,
#                 etudiant=etudiant,
#                 groupe=groupe
#             )
#         return paiement
    
#     def calculate_commission_amount(self, paiement_amount, commission_fixe, commission_percentage):
#         commission_base = min(paiement_amount, commission_fixe)
#         return commission_base * (commission_percentage / 100)





class ComissionSerializer(serializers.ModelSerializer):
    professeur = ProfesseurSerializer(read_only=True)
    etudiant = EtudiantSerializer(read_only=True) 
    groupe = GroupeBasicSerializer(read_only=True)
    month_name = serializers.SerializerMethodField()

    class Meta:
        model = Comission
        fields = [
            'id', 'montant', 'date_comission', 
            'mois_comission',  # YYYY-MM format
            'month_name',      # French month name
            'statut_comission', 'professeur',
            'etudiant', 'groupe'
        ]

    def get_month_name(self, obj):
        month_names = {
            '01': 'Janvier', '02': 'Février', '03': 'Mars',
            '04': 'Avril', '05': 'Mai', '06': 'Juin',
            '07': 'Juillet', '08': 'Août', '09': 'Septembre',
            '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
        }
        try:
            month = obj.mois_comission.split('-')[1]
            return month_names.get(month, '')
        except:
            return ''
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
    


""" ------------------------------------------ Financial Serializers -----------------------------------------------"""

class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = ['id', 'date', 'libele', 'montant', 'created_at']

class SortieBanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortieBanque
        fields = ['id', 'date', 'mode_paiement', 'montant', 'created_at']