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
    specialite = models.CharField()

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


class Groupe(models.Model):
    nom_groupe = models.CharField(max_length=100, default='Groupe 1')
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    max_etudiants = models.IntegerField()
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    commission_fixe = models.FloatField(default=120.0)  # Add this line


    def __str__(self):
        return f"Groupe de {self.matiere.nom_matiere} - {self.niveau.nom_niveau}"


class EtudiantGroupe(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('etudiant', 'groupe')  # Ensure unique student-group assignment

class Comission(models.Model):
    montant = models.FloatField()  # The amount of commission
    date_comission = models.DateTimeField(default=timezone.now)
    statut_comission = models.CharField(max_length=50)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Comission of {self.montant} for {self.professeur.nom} from {self.etudiant.nom}"


class Paiement(models.Model):
    montant = models.FloatField()
    date_paiement = models.DateTimeField(default=timezone.now)
    statut_paiement = models.CharField(max_length=50)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, default=1)  # Associate with a specific group
    commission_percentage = models.FloatField(default=100.0)  # Default commission percentage

    def __str__(self):
        return f"Paiement by {self.etudiant.nom} for group {self.groupe.id} on {self.date_paiement}"
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='events')
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.title
