from guillotina.auth.extractors import BasePolicy


class CookiePolicy(BasePolicy):
    name = 'cookie'

    async def extract_token(self, value=None):
        if value is None:
            token = self.request.cookies.get('auth_token')
            if token is not None:
                return {
                    'type': 'cookie',
                    'token': token.strip()
                }
