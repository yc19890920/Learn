from sanic_jwt import initialize, exceptions, protected, scoped
# from apps.utils.redis_pool import redis
# from sanic_jwt.utils import generate_token
from .models import username_table

async def authenticate(request, *args, **kwargs):
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return exceptions.AuthenticationFailed("Missing username or password")
    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')
    if not user.check_password(password.encode("utf-8")):
        raise exceptions.AuthenticationFailed("Password is incorrect")
    return user

# async def store_refresh_token(user_id, refresh_token, *args, **kwargs):
#     key = 'refresh_token_{user_id}'.format(user_id=user_id)
#     await redis.set(key, refresh_token)
#
# async def retrieve_refresh_token(user_id, *args, **kwargs):
#     key = 'refresh_token_{user_id}'.format(user_id=user_id)
#     return await redis.get(key)


# from sanic_jwt import BaseEndpoint
# class Register(BaseEndpoint):
#     async def post(self, request, *args, **kwargs):
#         username = request.json.get('username', None)
#         email = request.json.get('email', None)
#
#         helper = MyCustomUserAuthHelper()
#         user = helper.register_new_user(username, email)
#
#         access_token, output = await self.responses.get_access_token_output(
#             request,
#             user,
#             self.config,
#             self.instance)
#
#         refresh_token = await self.instance.auth.get_refresh_token(request, user)
#         output.update({
#             self.config.refresh_token_name(): refresh_token
#         })
#
#         response = self.responses.get_token_reponse(
#             request,
#             access_token,
#             output,
#             refresh_token=refresh_token,
#             config=self.config)
#         return response

