from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import random
import string


class League(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leagues')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    season = models.CharField(max_length=20, default='2024/25')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            while League.objects.filter(slug=slug).exists():
                slug = base_slug + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

    def get_standings(self):
        teams = self.teams.all()
        standings = []
        for team in teams:
            home_fixtures = self.fixtures.filter(home_team=team, is_played=True)
            away_fixtures = self.fixtures.filter(away_team=team, is_played=True)

            played = home_fixtures.count() + away_fixtures.count()
            wins = draws = losses = gf = ga = 0

            for f in home_fixtures:
                gf += f.home_score
                ga += f.away_score
                if f.home_score > f.away_score:
                    wins += 1
                elif f.home_score == f.away_score:
                    draws += 1
                else:
                    losses += 1

            for f in away_fixtures:
                gf += f.away_score
                ga += f.home_score
                if f.away_score > f.home_score:
                    wins += 1
                elif f.away_score == f.home_score:
                    draws += 1
                else:
                    losses += 1

            points = (wins * 3) + draws
            gd = gf - ga

            standings.append({
                'team': team,
                'played': played,
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'gf': gf,
                'ga': ga,
                'gd': gd,
                'points': points,
            })

        standings.sort(key=lambda x: (-x['points'], -x['gd'], -x['gf']))
        return standings


class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('league', 'name')

    def __str__(self):
        return self.name


class Fixture(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='fixtures')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_fixtures')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_fixtures')
    matchweek = models.PositiveIntegerField(default=1)
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)
    is_played = models.BooleanField(default=False)
    played_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['matchweek', 'id']

    def __str__(self):
        return f"MW{self.matchweek}: {self.home_team} vs {self.away_team}"

    def result_display(self):
        if self.is_played:
            return f"{self.home_score} - {self.away_score}"
        return "vs"