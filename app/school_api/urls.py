from django.urls import path
from . import views



urlpatterns = [

    path('list_create_etudiant/', views.list_create_etudiant),
    path('update_delete_etudiant/', views.update_delete_etudiant),

    path('list_create_professeur/', views.list_create_professeur),
    path('update_delete_professeur/', views.update_delete_professeur),

    path('list_create_niveau/', views.list_create_niveau),
    path('update_delete_niveau/', views.update_delete_niveau),

    path('list_create_filiere/', views.list_create_filiere),
    path('update_delete_filiere/', views.update_delete_filiere),

    path('list_create_matiere/', views.list_create_matiere),
    path('update_delete_matiere/', views.update_delete_matiere),

    path('list_create_groupe/', views.list_create_groupe),
    path('update_delete_groupe/', views.update_delete_groupe),


    path('assign_etudiant_group/', views.assign_etudiant_group),
    path('unassign_etudiant_from_groupe/', views.unassign_etudiant_from_groupe),
    path('list_groupes_with_etudiants/', views.list_groupes_with_etudiants),
    
    #path('groupes-with-etudiants/', views.list_groupes_with_etudiants, name='list-groupes-with-etudiants'),
    #path('groupe-with-etudiants/', views.groupe_with_etudiants, name='groupe-with-etudiants'),

    path('list_create_paiement/', views.list_create_paiement),
    path('list_comissions/', views.list_comissions)

]