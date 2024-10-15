from django.db import models

# Create your models here.
# relacoes de 1 para 1
# um user participa uma vez numa competicao

class user(models.Model):
    id = models.AutoField(primary_key=True) # auto increment
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

class competition(models.Model):
    id = models.AutoField(primary_key=True) # auto increment
    name = models.CharField(max_length=50)
    date = models.DateField()
    
    def __str__(self):
        return self.nome
    
# entidade fraca entre user e competition
class route(models.Model):
    id = models.AutoField(primary_key=True) # auto increment
    id_user = models.ForeignKey(user, on_delete=models.CASCADE) # usa o id do user como chave estrangeira
    id_competition = models.ForeignKey(competition, on_delete=models.CASCADE) # usa o id da competition como chave estrangeira
    name = models.CharField(max_length=50)
    distance = models.FloatField()
    # TODO ver como funcionam os ficheiros em django
    # file = models.FileField(upload_to='ficheiros/')
    
    def __str__(self):
        return self.nome

