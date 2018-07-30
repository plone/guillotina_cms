# -*- encoding: utf-8 -*-
from guillotina.api.service import Service
from datetime import datetime, timedelta
import jwt
from aiohttp.web import Response
from guillotina.api.service import DownloadService
from guillotina import configure
from guillotina.interfaces import IContainer

SECRET = 'secret'


@configure.service(
    context=IContainer, method='POST',
    permission='guillotina.Public', name='@login',
    summary='Components for a resource', allow_access=True)
class Login(Service):

    async def __call__(self):
        ttl = 3660
        token = jwt.encode(
            {
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(seconds=ttl),
                'fullname': 'root',
                'sub': 'root'
            },
            SECRET,
            algorithm='HS256')
        return {
            'token': token.decode('utf-8')
        }


@configure.service(
    context=IContainer, method='POST',
    permission='guillotina.AccessContent', name='@login-renew',
    summary='Components for a resource')
class Refresh(DownloadService):

    async def __call__(self):
        ttl = 3660
        token = jwt.encode(
            {
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(seconds=ttl),
                'token': 'YWRtaW4='
            },
            SECRET,
            algorithm='HS256')
        return Response(body=token)
