from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length= 50)
    Classe = models.CharField(max_length= 50)
    
    def __str__(self):
        return f"{self.user.username} - {self.matricule}"


class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
    
class Matiere(models.Model):
    nom = models.CharField(max_length=50)
    enseignant=models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    def __str__(self):
        return self.nom
    
    
class Note(models.Model):
    etudiant=models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere=models.ForeignKey(Matiere, on_delete=models.CASCADE)
    valeur=models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.etudiant}--{self.matiere} : {self.valeur}"
    
    