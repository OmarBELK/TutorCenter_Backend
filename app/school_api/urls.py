from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [

    # Etudiant paths
    path('etudiant_list/', EtudiantListView.as_view(), name='etudiant-list'),
    path('etudiants/create/', views.create_etudiant, name='create-etudiant'),
    path('etudiants/update/<int:pk>/', views.update_etudiant, name='update-etudiant'),
    path('etudiants/delete/<int:pk>/', views.delete_etudiant, name='delete-etudiant'),
    path('etudiants/<int:pk>/details/', etudiant_details, name='etudiant-details'),


    # Professeur paths
    path('professeur_list/', ProfesseurListView.as_view(), name='professeur-list'),
    path('professeurs/create/', views.create_professeur, name='create-professeur'),
    path('professeurs/update/<int:pk>/', views.update_professeur, name='update-professeur'),
    path('professeurs/delete/<int:pk>/', views.delete_professeur, name='delete-professeur'),
    path('professeurs/<int:pk>/details/', professeur_details, name='professeur-details'),

    # Niveau paths
    path('niveau_list/', NiveauListView.as_view(), name='niveau-list'),
    path('niveaux/create/', views.create_niveau, name='create-niveau'),
    path('niveaux/update/<int:pk>/', views.update_niveau, name='update-niveau'),
    path('niveaux/delete/<int:pk>/', views.delete_niveau, name='delete-niveau'),

    # Filiere paths
    path('filiere_list/', FiliereListView.as_view(), name='filiere-list'),
    path('filieres/create/', views.create_filiere, name='create-filiere'),
    path('filieres/update/<int:pk>/', views.update_filiere, name='update-filiere'),
    path('filieres/delete/<int:pk>/', views.delete_filiere, name='delete-filiere'),

    # Matiere paths
    path('matiere_list/', MatiereListView.as_view(), name='matiere-list'),
    path('matieres/create/', views.create_matiere, name='create-matiere'),
    path('matieres/update/<int:pk>/', views.update_matiere, name='update-matiere'),
    path('matieres/delete/<int:pk>/', views.delete_matiere, name='delete-matiere'),

    # Groupe paths
    path('groupe_list/', GroupeListView.as_view(), name='groupe-list'),
    path('groupes/create/', views.create_groupe, name='create-groupe'),
    path('groupes/update/<int:pk>/', views.update_groupe, name='update-groupe'),
    path('groupes/delete/<int:pk>/', views.delete_groupe, name='delete-groupe'),


    path('assign_etudiant_group/', views.assign_etudiant_group),
    path('unassign_etudiant_from_groupe/', views.unassign_etudiant_from_groupe),
    
    path('groupes-with-etudiants/', GroupeWithEtudiantsListView.as_view(), name='groupes-with-etudiants'),


    path('paiements/', PaiementListView.as_view(), name='paiement-list'),
    path('paiements/create/', views.create_paiement, name='create-paiement'),

    path('commissions/', ComissionListView.as_view(), name='commission-list'),

    path('events/', EventListView.as_view(), name='event-list'),
    path('events/create/', views.create_event, name='create-event'),
    path('events/update/<int:pk>/', views.update_event, name='update-event'),
    path('events/delete/<int:pk>/', views.delete_event, name='delete-event'),


    # JWT Authentication
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    # Staff Management
    path('staff/register/', views.StaffRegisterView.as_view(), name='staff-register'),
    path('staff/profile/', views.StaffProfileView.as_view(), name='staff-profile'),
    path('staff/change-password/', views.StaffChangePasswordView.as_view(), name='staff-change-password'),



    # Financial Tables

    path('depenses/', DepenseViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }), name='depense-list'),

    path('depenses/<int:pk>/', DepenseViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='depense-detail'),
        
    path('sorties-banque/', SortieBanqueViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }), name='sortie-banque-list'),

    path('sorties-banque/<int:pk>/', SortieBanqueViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='sortie-banque-detail'),

    # Dashboard Metrics
    path('dashboard/metrics/', dashboard_metrics, name='dashboard-metrics'),
    path('dashboard/financial-metrics/', financial_metrics_by_month, name='financial-metrics'),
    path('dashboard/weekly-financial-metrics/', weekly_financial_metrics, name='weekly-financial-metrics'),

]






