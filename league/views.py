from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import IntegrityError
import random
import itertools

from .models import League, Team, Fixture
from .forms import RegisterForm, LeagueForm, TeamForm, ResultForm


# ── Auth ────────────────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'league/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.username}! Create your first league below.")
        return redirect('dashboard')
    return render(request, 'league/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'league/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    leagues = League.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'league/dashboard.html', {'leagues': leagues})


# ── League ────────────────────────────────────────────────────────────────────

@login_required
def create_league(request):
    form = LeagueForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        league = form.save(commit=False)
        league.owner = request.user
        league.save()
        messages.success(request, f'"{league.name}" created! Now add your teams.')
        return redirect('add_teams', slug=league.slug)
    return render(request, 'league/create_league.html', {'form': form})


@login_required
def league_detail(request, slug):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    standings = league.get_standings()
    matchweeks = {}
    for fixture in league.fixtures.all():
        matchweeks.setdefault(fixture.matchweek, []).append(fixture)
    return render(request, 'league/league_detail.html', {
        'league': league,
        'standings': standings,
        'matchweeks': matchweeks,
        'total_teams': league.teams.count(),
        'played': league.fixtures.filter(is_played=True).count(),
        'remaining': league.fixtures.filter(is_played=False).count(),
    })


@login_required
def delete_league(request, slug):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    if request.method == 'POST':
        league.delete()
        messages.success(request, 'League deleted.')
        return redirect('dashboard')
    return render(request, 'league/confirm_delete.html', {'league': league})


# ── Teams ─────────────────────────────────────────────────────────────────────

@login_required
def add_teams(request, slug):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    form = TeamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            team = form.save(commit=False)
            team.league = league
            team.save()
            messages.success(request, f'"{team.name}" added!')
        except IntegrityError:
            messages.error(request, 'That team already exists in this league.')
        return redirect('add_teams', slug=slug)
    teams = league.teams.all()
    return render(request, 'league/add_teams.html', {'league': league, 'teams': teams, 'form': form})


@login_required
def delete_team(request, slug, team_id):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    team = get_object_or_404(Team, id=team_id, league=league)
    team.delete()
    messages.success(request, f'"{team.name}" removed.')
    return redirect('add_teams', slug=slug)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@login_required
def generate_fixtures(request, slug):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    teams = list(league.teams.all())

    if len(teams) < 2:
        messages.error(request, 'You need at least 2 teams to generate fixtures.')
        return redirect('add_teams', slug=slug)

    # Delete existing fixtures before regenerating
    league.fixtures.all().delete()

    random.shuffle(teams)

    # Round-robin algorithm (handles odd number of teams with a BYE)
    if len(teams) % 2 != 0:
        teams.append(None)  # BYE

    n = len(teams)
    rounds = n - 1
    half = n // 2

    all_fixtures = []
    team_list = teams[:]

    for round_num in range(rounds):
        for i in range(half):
            home = team_list[i]
            away = team_list[n - 1 - i]
            if home is not None and away is not None:
                all_fixtures.append((round_num + 1, home, away))
        # Rotate all except first
        team_list = [team_list[0]] + [team_list[-1]] + team_list[1:-1]

    # Second leg (return fixtures)
    first_leg = all_fixtures[:]
    for matchweek, home, away in first_leg:
        all_fixtures.append((matchweek + rounds, away, home))

    for matchweek, home, away in all_fixtures:
        Fixture.objects.create(
            league=league,
            home_team=home,
            away_team=away,
            matchweek=matchweek,
        )

    total = len(all_fixtures)
    messages.success(request, f'✅ {total} fixtures generated across {rounds * 2} matchweeks!')
    return redirect('league_detail', slug=slug)


# ── Results ───────────────────────────────────────────────────────────────────

@login_required
def enter_result(request, slug, fixture_id):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    fixture = get_object_or_404(Fixture, id=fixture_id, league=league)
    form = ResultForm(request.POST or None, instance=fixture)
    if request.method == 'POST' and form.is_valid():
        result = form.save(commit=False)
        result.is_played = True
        result.save()
        messages.success(request, f'Result saved: {fixture.home_team} {result.home_score} - {result.away_score} {fixture.away_team}')
        return redirect('league_detail', slug=slug)
    return render(request, 'league/enter_result.html', {'league': league, 'fixture': fixture, 'form': form})


@login_required
def reset_result(request, slug, fixture_id):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    fixture = get_object_or_404(Fixture, id=fixture_id, league=league)
    fixture.home_score = None
    fixture.away_score = None
    fixture.is_played = False
    fixture.played_on = None
    fixture.save()
    messages.info(request, 'Result cleared.')
    return redirect('league_detail', slug=slug)

@login_required
def fixtures_view(request, slug):
    league = get_object_or_404(League, slug=slug, owner=request.user)
    matchweeks = {}
    for fixture in league.fixtures.all():
        matchweeks.setdefault(fixture.matchweek, []).append(fixture)
    context = {
        'league': league,
        'matchweeks': matchweeks,
        'total_fixtures': league.fixtures.count(),
        'played': league.fixtures.filter(is_played=True).count(),
        'remaining': league.fixtures.filter(is_played=False).count(),
    }
    return render(request, 'league/fixtures.html', context)