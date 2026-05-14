from user_app.models import Friendship

def add_friend_request(user, other_user):
    Friendship.objects.get_or_create(from_user = user, to_user = other_user)
    return {'text': 'Очікування'}

def accept_friend_request(user, other_user):
    friendship = Friendship.objects.filter(from_user = other_user, to_user = user).first()
    friendship.status = 'accepted'
    friendship.save()
    return {}

def delete_friendship(user, other_user):
    friendship = Friendship.objects.filter(from_user = other_user, to_user = user).first()
    if not friendship:
        friendship = Friendship.objects.filter(from_user = user, to_user = other_user).first()
    if friendship:
        friendship.delete()
    return {}

def ignore_friendship(user, other_user):
    friendship = Friendship.objects.get_or_create(from_user = user, to_user = other_user, defaults= {'status':'ignored'})
    return {}
