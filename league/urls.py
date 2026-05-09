from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # League
    path('league/create/', views.create_league, name='create_league'),
    path('league/<slug:slug>/', views.league_detail, name='league_detail'),
    path('league/<slug:slug>/delete/', views.delete_league, name='delete_league'),

    # Teams
    path('league/<slug:slug>/teams/', views.add_teams, name='add_teams'),
    path('league/<slug:slug>/teams/<int:team_id>/delete/', views.delete_team, name='delete_team'),

    # Fixtures
    path('league/<slug:slug>/fixtures/generate/', views.generate_fixtures, name='generate_fixtures'),
    path('league/<slug:slug>/fixture/<int:fixture_id>/result/', views.enter_result, name='enter_result'),
    path('league/<slug:slug>/fixture/<int:fixture_id>/reset/', views.reset_result, name='reset_result'),
    path('league/<slug:slug>/fixtures/', views.fixtures_view, name='fixtures')
]