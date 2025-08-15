import re
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from openid.consumer.consumer import Consumer, SUCCESS
from openid.store.memstore import MemoryStore
from django.shortcuts import redirect
from core.constants import FRONTEND_URL, SERVER_DOMAIN, STEAM_OPENID_URL, STEAM_GET_USER_INFO_URL
from .services import get_steam_user_summary
from .models import User
from urllib.parse import urlencode, urljoin


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    try:
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'steam_profile_url': user.steam_profile_url,
            'steam_id': user.steam_id,
            'balance': str(user.balance),
            'trade_url': user.trade_url,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
def redirect_to_steam(request):
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': f'{SERVER_DOMAIN}/api/v1/auth/steam/callback/',
        'openid.realm': SERVER_DOMAIN,
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
    }
    steam_url = f"{STEAM_OPENID_URL}?{urlencode(params)}"
    print('Redirecting to:', steam_url)
    return redirect(steam_url)


@api_view(['GET'])
def steam_callback(request):
    claimed_id = request.GET.get('openid.claimed_id')
    if not claimed_id:
        return Response({'error': 'Missing claimed_id'}, status=400)

    # Попытка извлечь SteamID из claimed_id
    match = re.search(r'/id/(\d+)|/profiles/(\d+)|/openid/id/(\d+)', claimed_id)
    if not match:
        return Response({'error': 'Invalid Steam ID'}, status=400)

    steam_id = match.group(1) or match.group(2) or match.group(3)

    steam_user_summary = get_steam_user_summary(steam_id)
    if not steam_user_summary:
        return Response({'error': 'Ошибка при запросе данных о пользователе'}, status=500)

    user, _ = User.objects.update_or_create(
        steam_id=steam_id,
        defaults={
            'username': steam_user_summary.get('personaname'),
            'avatar': steam_user_summary.get('avatarfull'),
            'steam_profile_url': steam_user_summary.get("profileurl"),
        }
    )

    refresh = RefreshToken.for_user(user)
    print(refresh.access_token)
    redirect_url = urljoin(FRONTEND_URL, 'steam-callback') + f'?access={refresh.access_token}&refresh={str(refresh)}'
    return redirect(redirect_url)