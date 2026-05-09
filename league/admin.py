from django.contrib import admin
from .models import League, Team, Fixture

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'season', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'league']

@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'matchweek', 'is_played', 'home_score', 'away_score']