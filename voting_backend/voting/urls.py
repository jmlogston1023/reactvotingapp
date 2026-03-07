from django.urls import path
from . import views
from .views import voters_list, ballot_voters, voter_activity


urlpatterns = [
    path('auth/request-code/', views.request_code),
    path('auth/verify-code/', views.verify_code),
    path('login/', views.login_user),
    path('ballot/', views.get_ballot),
    path('vote/', views.submit_vote),
    path("results/<int:ballot_id>/", views.ballot_results),
    path("voters/", voters_list),
    path('api/voters/', voters_list, name='voters-list'),
    path('ballot/<int:ballot_id>/voters/', ballot_voters),
    #path('recordvote/', record_vote, name='record-vote'),
    path('admin/voter-activity/', voter_activity, name='voter-activity'),
    #path("admin/voter-activity/", views.voter_activity),
    #path("api/admin/voter-activity/", views.voter_activity),
]
