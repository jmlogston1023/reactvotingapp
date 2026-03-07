import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class LoginToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)


class Ballot(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_selections = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)


class Candidate(models.Model):
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ballot')

class VoteRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ballot')



class VoteSelection(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)


class LoginCode(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)


########### new add

class VoteRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

"""
class VoteSelection(models.Model):
    vote = models.ForeignKey(VoteRecord, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

"""
