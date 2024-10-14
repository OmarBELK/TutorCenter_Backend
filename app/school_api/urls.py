from django.urls import path
from . import views



urlpatterns = [
    path('list_create_etudiants/', views.list_create_etudiants),
    path('etudiant_detail/', views.etudiant_detail),

    path('professeurs/', views.professeur_list),
    path('professeur_detail/', views.professeur_detail),

    path('niveaux/', views.niveau_list),
    path('niveau_detail/', views.niveau_detail),

    path('filieres/', views.filiere_list),
    path('filiere_detail/', views.filiere_detail),

    path('matieres/', views.matiere_list),
    path('matiere_detail', views.matiere_detail),

    path('groupes/', views.list_create_groupe),
    path('groupe_detail/', views.groupe_detail),

    path('assign_student/', views.assign_etudiant_group),
    path('groupes-with-etudiants/', views.list_groupes_with_etudiants, name='list-groupes-with-etudiants'),
    path('groupe-with-etudiants/', views.groupe_with_etudiants, name='groupe-with-etudiants'),

    path('list_create_paiement/', views.list_create_paiement),
    path('list_comissions/', views.list_comissions)



]