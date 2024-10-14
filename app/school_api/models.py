from django.db import models

# Create your models here.


class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()

    def __str__(self) -> str:
        return f"{self.nom} {self.prenom}"
    

class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    comission_fixe = models.FloatField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Comission(models.Model):
    montant = models.FloatField()  # The amount of commission
    date_comission = models.DateField()
    statut_comission = models.CharField(max_length=50)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comission of {self.montant} for {self.professeur.nom} from {self.etudiant.nom}"


class Niveau(models.Model):
    nom_niveau = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_niveau

class Filiere(models.Model):
    nom_filiere = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_filiere

class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_matiere


class Groupe(models.Model):
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    max_etudiants = models.IntegerField()
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"Groupe de {self.matiere.nom_matiere} - {self.niveau.nom_niveau}"


class EtudiantGroupe(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('etudiant', 'groupe')  # Ensure unique student-group assignment



class Paiement(models.Model):
    montant = models.FloatField()
    date_paiement = models.DateField()
    statut_paiement = models.CharField(max_length=50)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, default=1)  # Associate with a specific group
    commission_percentage = models.FloatField(default=100.0)  # Default commission percentage

    def __str__(self):
        return f"Paiement by {self.etudiant.nom} for group {self.groupe.id} on {self.date_paiement}"
    



