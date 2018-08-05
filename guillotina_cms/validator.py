# -*- coding: utf-8 -*-
from aiohttp.web_exceptions import HTTPUnauthorized
from guillotina import app_settings
from guillotina.auth.users import GuillotinaUser
from guillotina.exceptions import Unauthorized

import jwt
import logging


logger = logging.getLogger('guillotina_cms')


NON_IAT_VERIFY = {
    'verify_iat': False,
}


class CMSJWTValidator(object):

    for_validators = ('bearer', 'wstoken', 'cookie')

    def __init__(self, request):
        self.request = request

    async def validate(self, token):
        """Return the user from the token."""
        if token.get('type') not in ('bearer', 'wstoken', 'cookie'):
            return None

        if '.' not in token.get('token', ''):
            # quick way to check if actually might be jwt
            return None

        try:
            try:
                validated_jwt = jwt.decode(
                    token['token'],
                    app_settings['jwt']['secret'],
                    algorithms=[app_settings['jwt']['algorithm']])
            except jwt.exceptions.ExpiredSignatureError:
                logger.warn("Token Expired")
                raise HTTPUnauthorized()
            except jwt.InvalidIssuedAtError:
                logger.warn("Back to the future")
                validated_jwt = jwt.decode(
                    token['token'],
                    app_settings['jwt']['secret'],
                    algorithms=[app_settings['jwt']['algorithm']],
                    options=NON_IAT_VERIFY)

            user = GuillotinaUser(self.request)
            user.name = validated_jwt['fullname']
            user.id = validated_jwt['sub']
            return user

        except jwt.exceptions.DecodeError:
            pass

        return None

