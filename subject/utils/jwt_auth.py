import jwt
import time


def create_jitsi_token(user, room_name, is_moderator=False):
    payload = {
        'aud': 'jitsi',
        'iss': 'educhat',
        'sub': 'educhat.uz',
        'room': room_name,
        'exp': int(time.time()) + 3600,
        'context': {
            'user': {
                'name': user.username(),
                'moderator': str(is_moderator).lower()
            }
        }
    }

    secret = 'supersecret'
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token
