from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView   # ✅ ADD THIS LINE

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('register-success/', views.register_success, name='register_success'),
    path('login/', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),

    path('create-auction/', views.create_auction, name='create_auction'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),

    path('edit-auction/<int:id>/', views.edit_auction, name='edit_auction'),
    path('delete-auction/<int:id>/', views.delete_auction, name='delete_auction'),

    path('players/<int:auction_id>/', views.players, name='players'),
    path('player/edit/<int:id>/', views.edit_player, name='edit_player'),
    path('player/delete/<int:id>/', views.delete_player, name='delete_player'),

    # ✅ LOGOUT FIXED
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('teams/<int:auction_id>/', views.teams, name='teams'),
    path('team/delete/<int:id>/', views.delete_team, name='delete_team'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('auction-dashboard/<int:auction_id>/',views.auction_dashboard,name='auction_dashboard'),

    path('place-bid/<int:player_id>/<int:team_id>/',views.place_bid,name='place_bid'),
    path('sold-player/<int:player_id>/',views.sold_player,name='sold_player'),
    path('unsold-player/<int:player_id>/',views.unsold_player,name='unsold_player'),
    path('random-player/<int:auction_id>/',views.random_player,name='random_player'),
    path('undo-last-bid/<int:auction_id>/',views.undo_last_bid,name='undo_last_bid'),
    path('auction-summary/<int:auction_id>/',views.auction_summary,name='auction_summary'),

]