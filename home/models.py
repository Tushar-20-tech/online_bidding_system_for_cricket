from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profile_pics/')

    full_name = models.CharField(max_length=150)

    mobile_number = models.CharField(max_length=15)

    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username


class Auction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    auction_logo = models.ImageField(upload_to='auction_logos/')

    auction_name = models.CharField(max_length=200)

    auction_date = models.DateField()

    points_per_team = models.IntegerField()

    minimum_bid = models.IntegerField()

    bid_increase_by = models.IntegerField()

    players_per_team = models.IntegerField()

    def __str__(self):
        return self.auction_name


class Team(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    team_logo = models.ImageField(upload_to='teams/')

    team_name = models.CharField(max_length=150)

    # 🔥 NEW
    total_spent = models.IntegerField(default=0)

    def __str__(self):
        return self.team_name


class Player(models.Model):

    CATEGORY_CHOICES = [
        ('RHB', 'Right Hand Batsman'),
        ('LHB', 'Left Hand Batsman'),
        ('RHB_AR', 'Right Hand All-Rounder'),
        ('LHB_AR', 'Left Hand All-Rounder'),
        ('RBOWLER', 'Right Arm Bowler'),
        ('LBOWLER', 'Left Arm Bowler'),
        ('WICKET_KEEPER', 'Wicket Keeper'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SOLD', 'Sold'),
        ('UNSOLD', 'Unsold'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    player_image = models.ImageField(upload_to='players/')

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    dob = models.DateField()

    tshirt_size = models.CharField(max_length=20)

    trouser_size = models.CharField(max_length=20)

    notes = models.TextField(
        blank=True,
        null=True
    )

    # 🔥 BIDDING SYSTEM
    base_price = models.IntegerField(default=0)

    sold_price = models.IntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_category_display()})"


# 🔥 LIVE BID HISTORY
class BidHistory(models.Model):

    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.player} - {self.team} - ₹{self.amount}"



class BidHistory(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} -> {self.team} ₹{self.amount}"