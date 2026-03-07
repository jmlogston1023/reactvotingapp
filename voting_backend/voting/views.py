from django.shortcuts import render

# Create your views here.

import random
from rest_framework import status
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, LoginCode, LoginToken, Ballot, Candidate, Vote, VoteSelection, VoteRecord
from django.http import JsonResponse
from .serializers import VoterActivitySerializer
#from django.contrib.auth.models import User


@api_view(['POST'])
def request_login(request):
    email = request.data.get("email")

    user, _ = User.objects.get_or_create(email=email)

    token = LoginToken.objects.create(
        user=user,
        expires_at=timezone.now() + timedelta(minutes=15)
    )

    login_link = f"http://localhost:3000/verify/{token.token}"

    send_mail(
        "Login to Vote",
        f"Click this link to login: {login_link}",
        "noreply@votingapp.com",
        [email],
    )

    return Response({"message": "Login link sent"})


@api_view(['POST'])
def login_user(request):
    email = request.data.get("email")

    try:
        user = User.objects.get(email=email)
        return Response({"user_id": user.id})
    except User.DoesNotExist:
        return Response({"error": "Email not registered"}, status=400)

@api_view(['GET'])
def get_ballot(request):
    ballot = Ballot.objects.filter(is_active=True).first()
    candidates = Candidate.objects.filter(ballot=ballot)

    return Response({
        "ballot_id": ballot.id,
        "title": ballot.title,
        "description": ballot.description,
        "max_selections": ballot.max_selections,
        "candidates": [
            {"id": c.id, "name": c.name}
            for c in candidates
        ]
    })


"""
@api_view(['POST'])
def submit_vote(request):
    user_id = request.data.get("user_id")
    ballot_id = request.data.get("ballot_id")
    candidate_ids = request.data.get("candidate_ids")

    if Vote.objects.filter(user_id=user_id, ballot_id=ballot_id).exists():
        return Response({"error": "Already voted"}, status=400)

    ballot = Ballot.objects.get(id=ballot_id)

    if len(candidate_ids) > ballot.max_selections:
        return Response({"error": "Too many selections"}, status=400)

    vote = Vote.objects.create(user_id=user_id, ballot_id=ballot_id)

    for cid in candidate_ids:
        VoteSelection.objects.create(vote=vote, candidate_id=cid)

    return Response({"message": "Vote recorded"})
"""

@api_view(['POST'])
def submit_vote(request):
    user_id = request.data.get("user_id")
    ballot_id = request.data.get("ballot_id")
    candidate_ids = request.data.get("candidate_ids")

    if not user_id or not ballot_id or not candidate_ids:
        return Response({"error": "Missing required fields"}, status=400)

    # Prevent duplicate voting using VoteRecord
    if VoteRecord.objects.filter(user_id=user_id, ballot_id=ballot_id).exists():
        return Response({"error": "Already voted"}, status=400)

    try:
        ballot = Ballot.objects.get(id=ballot_id)
    except Ballot.DoesNotExist:
        return Response({"error": "Ballot not found"}, status=404)

    # Check selection limit
    if len(candidate_ids) > ballot.max_selections:
        return Response({"error": "Too many selections"}, status=400)

    # Create Vote row
    vote = Vote.objects.create(user_id=user_id, ballot_id=ballot_id)

    # Create VoteSelection rows
    for cid in candidate_ids:
        VoteSelection.objects.create(
            vote=vote,
            candidate_id=cid
        )

    # Create VoteRecord row (tracks voting activity)
    vote_record = VoteRecord.objects.create(
        user_id=user_id,
        ballot_id=ballot_id
    )

    return Response({
        "message": "Vote recorded",
        "vote_id": vote.id,
        "record_id": vote_record.id,
        "voted_at": vote_record.voted_at
    })

@api_view(['POST'])
def request_code(request):
    email = request.data.get("email")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Email not registered"}, status=400)

    code = str(random.randint(100000, 999999))

    LoginCode.objects.create(user=user, code=code)

    send_mail(
        "Your Voting Login Code",
        f"Your login code is: {code}",
        None,
        [email],
    )

    return Response({"message": "Code sent"})

@api_view(['POST'])
def verify_code(request):
    email = request.data.get("email")
    code = request.data.get("code")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email"}, status=400)

    login_code = LoginCode.objects.filter(
        user=user,
        code=code,
        used=False,
        expires_at__gt=timezone.now()
    ).first()

    if not login_code:
        return Response({"error": "Invalid or expired code"}, status=400)

    login_code.used = True
    login_code.save()

    return Response({"user_id": user.id})

@api_view(['GET'])
def ballot_results(request, ballot_id):

    ballot = Ballot.objects.get(id=ballot_id)

    candidates = Candidate.objects.filter(ballot=ballot)

    results = []

    for c in candidates:
        votes = VoteSelection.objects.filter(candidate=c).count()

        results.append({
            "candidate": c.name,
            "votes": votes
        })

    total_votes = VoteSelection.objects.filter(
        candidate__ballot=ballot
    ).count()

    return Response({
        "ballot": ballot.title,
        "total_votes": total_votes,
        "results": results
    })


@api_view(['GET'])
def ballot_results(request, ballot_id):

    ballot = Ballot.objects.get(id=ballot_id)

    candidates = Candidate.objects.filter(ballot=ballot)

    results = []

    for candidate in candidates:

        vote_count = VoteSelection.objects.filter(
            candidate=candidate
        ).count()

        results.append({
            "candidate": candidate.name,
            "votes": vote_count
        })

    return Response({
        "ballot_title": ballot.title,
        "results": results
    })


@api_view(['GET'])
def voters_list(request):
    # Pull votes with related user and ballot info
    votes = VoteRecord.objects.select_related('user', 'ballot').all()

    data = []
    for vote in votes:
        # Make sure user has an email
        user_email = vote.user.email if vote.user and vote.user.email else "N/A"
        ballot_title = vote.ballot.title if vote.ballot else "N/A"

        data.append({
            "user_email": user_email,
            "ballot_title": ballot_title,
            "voted_at": vote.voted_at,
        })

    return Response(data)



@api_view(['GET'])
def voters_list(request):
    votes = VoteRecord.objects.select_related('user', 'ballot').all()
    serializer = VoterListSerializer(votes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ballot_voters(request, ballot_id):

    votes = VoteRecord.objects.filter(ballot_id=ballot_id).values(
        'user__email',
        'ballot__title',
        'voted_at'
    )

    return Response({
        "ballot_id": ballot_id,
        "total_votes": len(votes),
        "voters": list(votes)
    })


@api_view(['GET'])
def voter_activity(request):
    # load votes with related user and ballot to avoid extra queries
    votes = VoteRecord.objects.select_related('user', 'ballot').all()

    serializer = VoterActivitySerializer(votes, many=True)
    return Response(serializer.data)
