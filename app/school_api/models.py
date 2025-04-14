from django.db import models
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

# Create your models here.


class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    nationalite = models.CharField(max_length=100, null=True, blank=True, default='Marocain')
    contact_urgence = models.CharField(max_length=100, null=True, blank=True)
    etablissement = models.CharField(max_length=200, null=True, blank=True)  # Optional establishment field
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.nom} {self.prenom}"
    

class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    nationalite = models.CharField(max_length=100, null=True, blank=True, default='Marocain')
    specialite = models.CharField(max_length=100) # Added max_length
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Niveau(models.Model):
    nom_niveau = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom_niveau

class Filiere(models.Model):
    nom_filiere = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom_filiere

class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom_matiere


# class Groupe(models.Model):
#     nom_groupe = models.CharField(max_length=100, default='Groupe 1')
#     professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
#     niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
#     max_etudiants = models.IntegerField()
#     filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
#     matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
#     commission_fixe = models.FloatField(default=120.0)  
#     created_at = models.DateTimeField(default=timezone.now)  


#     def __str__(self):
#         return f"Groupe de {self.matiere.nom_matiere} - {self.niveau.nom_niveau}"



class Groupe(models.Model):
    nom_groupe = models.CharField(max_length=100)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    max_etudiants = models.IntegerField()
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    prix_subscription = models.FloatField(default=0)
    professeurs = models.ManyToManyField(Professeur, through='GroupeProfesseur')
    matieres = models.ManyToManyField(Matiere, through='GroupeMatiere')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom_groupe


class GroupeMatiere(models.Model):
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE)
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('groupe', 'matiere')

    def __str__(self):
        return f"{self.groupe.nom_groupe} - {self.matiere.nom_matiere}"


class GroupeProfesseur(models.Model):
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE)
    professeur = models.ForeignKey('Professeur', on_delete=models.CASCADE)
    commission_fixe = models.FloatField(default=100.0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('groupe', 'professeur')

    def __str__(self):
        return f"{self.professeur.nom} - {self.groupe.nom_groupe}"


class EtudiantGroupe(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('etudiant', 'groupe')  # Ensure unique student-group assignment

class Comission(models.Model):
    montant = models.FloatField()  # The amount of commission
    date_comission = models.DateTimeField(default=timezone.now)
    mois_comission = models.CharField(max_length=7)                       # Format: YYYY-MM
    statut_comission = models.CharField(max_length=50)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Comission of {self.montant} for {self.professeur.nom} from {self.etudiant.nom}"


class Paiement(models.Model):
    montant = models.FloatField(blank=True, null=True)                    # Amount paid
    montant_total = models.FloatField(blank=True, null=True)              # Total course cost
    remaining = models.FloatField(blank=True, null=True)                  # Remaining amount (we set this manually)
    frais_inscription = models.FloatField(default=100)                    # Registration fee, default 100
    date_paiement = models.DateTimeField(default=timezone.now)
    mois_paiement = models.CharField(max_length=7)                        # Format: YYYY-MM
    statut_paiement = models.CharField(max_length=50)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    is_registration_fee = models.BooleanField(default=False)              # Flag to identify registration fee payments

    def __str__(self):
        return f"{self.etudiant.nom} - Paid: {self.montant} - Remaining: {self.remaining}"

""" ------------------------------------------ Financial Models -----------------------------------------------"""
from django.db import models
from django.utils import timezone

class Depense(models.Model):
    date = models.DateTimeField(default=timezone.now)
    libele = models.CharField(max_length=200)
    montant = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.libele} - {self.montant}"

class SortieBanque(models.Model):
    PAYMENT_MODES = [
        ('CHEQUE', 'Chèque'),
        ('VIREMENT', 'Virement'),
        ('ESPECES', 'Espèces'),
        ('CARTE', 'Carte Bancaire'),
    ]

    date = models.DateTimeField(default=timezone.now)
    mode_paiement = models.CharField(max_length=50, choices=PAYMENT_MODES)
    montant = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.mode_paiement} - {self.montant}"