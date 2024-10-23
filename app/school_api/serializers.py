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
        fields = ['id', 'nom', 'prenom', 'date_naissance', 'groupe_id', 'telephone', 'adresse', 'sexe', 'nationalite', 'contact_urgence']

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
        fields = ['id', 'nom', 'prenom', 'date_naissance','telephone', 'adresse', 'sexe', 'nationalite', 'contact_urgence','groupes', 'paiements',]

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
        fields = ['id', 'nom', 'prenom', 'telephone', 'adresse', 'date_naissance', 'sexe', 'nationalite', 'specialite', 'groupes', 'commissions']

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
        fields = ['id', 'nom_groupe', 'professeur', 'niveau', 'max_etudiants', 'filiere', 'matiere']

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

    class Meta:
        model = Paiement
        fields = ['id', 'montant', 'date_paiement', 'statut_paiement', 'etudiant_id', 'groupe_id', 'commission_percentage']

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
