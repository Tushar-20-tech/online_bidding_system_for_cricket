from email.mime import image

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Player, UserProfile ,Auction, Team,BidHistory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import random
from django.db.models import Q


def index(request):
    return render(request, 'index.html')

def register(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        date_of_birth = request.POST.get('date_of_birth')

        profile_pic = request.FILES.get('profile_pic')  # ✅ safer

        # PASSWORD CHECK
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # USERNAME CHECK
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # IMAGE CHECK
        if profile_pic and not profile_pic.name.endswith('.jpg'):
            messages.error(request, "Upload JPG image only")
            return redirect('register')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # CREATE PROFILE
        UserProfile.objects.create(
            user=user,
            profile_pic=profile_pic,
            full_name=full_name,
            mobile_number=mobile_number,
            date_of_birth=date_of_birth
        )

        messages.success(request, "Registration successful")

        return redirect('login')

    return render(request, 'register.html')


def register_success(request):

    return render(request,'register_success.html')


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        # ✅ Check if user exists
        if not User.objects.filter(username=username).exists():

            messages.error(request, "User not registered")
            return redirect('login')

        # ✅ Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect('dashboard')

        else:

            messages.error(request, "Incorrect password")

    return render(request, 'login.html')



def dashboard(request):

    auctions = Auction.objects.filter(user=request.user).order_by('-id')
    latest_auction = auctions.first()

    chart_data = []

    if latest_auction:
        raw_data = Player.objects.filter(
            auction=latest_auction
        ).values('category').annotate(count=Count('id'))

        # Convert category codes to readable names
        category_map = dict(Player.CATEGORY_CHOICES)

        chart_data = [
            {
                "category": category_map.get(item['category'], item['category']),
                "count": item['count']
            }
            for item in raw_data
        ]

    return render(request, 'dashboard.html', {
        'auctions': auctions,
        'chart_data': chart_data
    })

@login_required
def profile(request):
    profile = request.user.userprofile   # ✅ get profile
    return render(request, 'profile.html', {'profile': profile})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')
    

@login_required
def create_auction(request):

    if request.method == "POST":

        auction_logo = request.FILES.get('auction_logo')

        if auction_logo and not auction_logo.name.endswith('.jpg'):
            messages.error(request, "Only JPG images allowed")
            return redirect('create_auction')

        Auction.objects.create(

            user=request.user,

            auction_logo=auction_logo,
            auction_name=request.POST['auction_name'],
            auction_date=request.POST['auction_date'],
            points_per_team=request.POST['points_per_team'],
            minimum_bid=request.POST['minimum_bid'],
            bid_increase_by=request.POST['bid_increase_by'],
            players_per_team=request.POST['players_per_team']

        )

        messages.success(request, "Auction Created Successfully")
        return redirect('dashboard')

    return render(request, 'create_auction.html')


@login_required
def my_auctions(request):

    auctions = Auction.objects.filter(user=request.user).order_by('-id')

    return render(request, 'my_auctions.html', {'auctions': auctions})

@login_required
def edit_auction(request, id):

    auction = get_object_or_404(Auction, id=id, user=request.user)

    if request.method == "POST":

        auction.auction_name = request.POST['auction_name']
        auction.auction_date = request.POST['auction_date']
        auction.points_per_team = request.POST['points_per_team']
        auction.minimum_bid = request.POST['minimum_bid']
        auction.bid_increase_by = request.POST['bid_increase_by']
        auction.players_per_team = request.POST['players_per_team']

        # update image only if new uploaded
        if request.FILES.get('auction_logo'):
            auction.auction_logo = request.FILES['auction_logo']

        auction.save()

        return redirect('my_auctions')

    return render(request, 'edit_auction.html', {'auction': auction})

@login_required
def delete_auction(request, id):

    auction = get_object_or_404(Auction, id=id, user=request.user)

    if request.method == "POST":
        auction.delete()
        return redirect('my_auctions')

    return redirect('my_auctions')


def players(request, auction_id):

    auction = get_object_or_404(Auction, id=auction_id)

    if request.method == "POST":

        Player.objects.create(
        user=request.user,
        auction=auction,
        player_image=request.FILES.get('player_image'),
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        category=request.POST.get('category'),
        mobile=request.POST.get('mobile'),
        email=request.POST.get('email'),
        dob=request.POST.get('dob'),
        tshirt_size=request.POST.get('tshirt_size'),
        trouser_size=request.POST.get('trouser_size'),
        notes=request.POST.get('notes')
)

        return redirect('players', auction_id=auction.id)

    players = Player.objects.filter(auction=auction)

    return render(request, 'players.html', {
        'auction': auction,
        'players': players,
        'categories': Player.CATEGORY_CHOICES   # 🔥 FIX
    })


@login_required
def edit_player(request, id):

    player = get_object_or_404(Player, id=id, user=request.user)

    if request.method == "POST":

        image = request.FILES.get('player_image')

        if image and not image.name.endswith('.jpg'):
            messages.error(request, "Only JPG allowed")
            return redirect('edit_player', id=id)

        if image:
            player.player_image = image

        player.first_name = request.POST.get('first_name')
        player.last_name = request.POST.get('last_name')
        player.category = request.POST.get('category')
        player.mobile = request.POST.get('mobile')
        player.email = request.POST.get('email')
        player.dob = request.POST.get('dob')
        player.tshirt_size = request.POST.get('tshirt_size')
        player.trouser_size = request.POST.get('trouser_size')
        player.notes = request.POST.get('notes')

        player.save()

        return redirect('players', auction_id=player.auction.id)

    return render(request, 'edit_player.html', {
        'player': player
    })


@login_required
def delete_player(request, id):
    player = get_object_or_404(Player, id=id, user=request.user)

    if request.method == "POST":
        auction_id = player.auction.id
        player.delete()
        return redirect('players', auction_id=auction_id)
    


def teams(request, auction_id):

    auction = Auction.objects.get(id=auction_id, user=request.user)
    teams = Team.objects.filter(auction=auction)

    if request.method == 'POST':

        logo = request.FILES.get('team_logo')

        if logo and not logo.name.endswith('.jpg'):
            messages.error(request, "Only JPG images allowed")
            return redirect('teams', auction_id=auction.id)

        Team.objects.create(
            user=request.user,
            auction=auction,
            team_logo=logo,
            team_name=request.POST.get('team_name')
        )

        messages.success(request, "Team added successfully")
        return redirect('teams', auction_id=auction.id)

    return render(request, 'teams.html', {
        'auction': auction,
        'teams': teams
    })


def delete_team(request, id):
    team = get_object_or_404(Team, id=id, user=request.user)

    auction_id = team.auction.id
    team.delete()

    return redirect('teams', auction_id=auction_id)


@login_required
def auction_dashboard(request, auction_id):

    auction = get_object_or_404(
        Auction,
        id=auction_id,
        user=request.user
    )

    teams = Team.objects.filter(
        auction=auction
    )

    sold_players = Player.objects.filter(
        auction=auction,
        status='SOLD'
    ).order_by('-id')[:8]

    current_player = Player.objects.filter(
        auction=auction,
        status='PENDING'
    ).first()

    if current_player:

        # SET BASE PRICE AUTOMATICALLY
        if current_player.base_price == 0:
            current_player.base_price = auction.minimum_bid
            current_player.save()

    return render(request, 'auction_dashboard.html', {
        'auction': auction,
        'teams': teams,
        'current_player': current_player,
        'sold_players': sold_players,
    })


@login_required
def place_bid(request, player_id, team_id):

    player = get_object_or_404(
        Player,
        id=player_id,
        user=request.user
    )

    team = get_object_or_404(
        Team,
        id=team_id,
        user=request.user
    )

    auction = player.auction

    # FIRST BID
    if not player.sold_price:
        player.sold_price = player.base_price

    # INCREASE BID
    else:
        player.sold_price += auction.bid_increase_by

    player.team = team
    player.save()

    # SAVE HISTORY
    BidHistory.objects.create(
        auction=auction,
        player=player,
        team=team,
        amount=player.sold_price
    )

    return redirect('auction_dashboard', auction.id)

@login_required
def sold_player(request, player_id):

    player = get_object_or_404(
        Player,
        id=player_id,
        user=request.user
    )

    # VALIDATION
    if not player.team:

        messages.error(
            request,
            "No team selected for bidding."
        )

        return redirect(
            'auction_dashboard',
            auction_id=player.auction.id
        )

    # SOLD STATUS
    player.status = 'SOLD'
    player.save()

    # TEAM SPENDING
    if player.sold_price:

        player.team.total_spent += player.sold_price
        player.team.save()

    # 🔥 GRAND SUCCESS MESSAGE
    messages.success(
        request,
        f"🏏 {player.first_name} {player.last_name} SOLD to {player.team.team_name} for ₹{player.sold_price}"
    )

    return redirect(
        'auction_dashboard',
        auction_id=player.auction.id
    )
@login_required
def unsold_player(request, player_id):

    player = get_object_or_404(
        Player,
        id=player_id,
        user=request.user
    )

    player.status = 'UNSOLD'
    player.save()

    return redirect('auction_dashboard', player.auction.id)

@login_required
def random_player(request, auction_id):

    auction = get_object_or_404(
        Auction,
        id=auction_id,
        user=request.user
    )

    # GET ONLY PENDING PLAYERS
    pending_players = Player.objects.filter(
        auction=auction,
        status='PENDING'
    )

    # IF NO PLAYERS
    if not pending_players.exists():

        messages.warning(
            request,
            "No pending players remaining."
        )

        return redirect(
            'auction_dashboard',
            auction_id=auction.id
        )

    # RANDOM PLAYER
    selected_player = random.choice(
        list(pending_players)
    )

    # STORE CURRENT PLAYER IN SESSION
    request.session[
        f'current_player_{auction.id}'
    ] = selected_player.id

    return redirect(
        'auction_dashboard',
        auction_id=auction.id
    )


@login_required
def undo_last_bid(request, auction_id):

    auction = get_object_or_404(
        Auction,
        id=auction_id,
        user=request.user
    )

    last_bid = BidHistory.objects.filter(
        auction=auction
    ).order_by('-id').first()

    if last_bid:

        player = last_bid.player

        # RESET PLAYER
        player.sold_price = None
        player.team = None
        player.status = 'PENDING'
        player.save()

        # DELETE LAST HISTORY
        last_bid.delete()

    return redirect(
        'auction_dashboard',
        auction_id=auction.id
    )


@login_required
def auction_summary(request, auction_id):

    auction = get_object_or_404(
        Auction,
        id=auction_id,
        user=request.user
    )

    teams = Team.objects.filter(
        auction=auction
    )

    sold_players = Player.objects.filter(
        auction=auction,
        status='SOLD'
    ).order_by('-sold_price')

    unsold_players = Player.objects.filter(
        auction=auction,
        status='UNSOLD'
    )

    return render(
        request,
        'auction_summary.html',
        {
            'auction': auction,
            'teams': teams,
            'sold_players': sold_players,
            'unsold_players': unsold_players,
        }
    )