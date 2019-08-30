import datetime
from sanic import Sanic
from sanic_cors import CORS
from sanic_redis import SanicRedis
from sanic.exceptions import NotFound, InvalidUsage, ServerError
from sanic.response import json
from sanic_jwt import initialize
from sanic_limiter import Limiter, get_remote_address, RateLimitExceeded
from sanic_openapi import swagger_blueprint, openapi_blueprint

from . import settings, import_data, db
from apps.auth.views import authenticate
from apps.v1.api.models import ShanghaiPersonInfo
from apps.v1.api.views import crud_bp

app = Sanic(__name__)
app.config.from_object(settings)
app.config.update(settings.SANIC_REDIS_CONFIG)
app.config.LOGO = settings.LOGO.format(', Y.c')
# app.config.LOGO = None

app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

redis = SanicRedis(app)
CORS(app, automatic_options=True)

app.blueprint(crud_bp)
# 接口访问限制
# app.config.RATELIMIT_STORAGE_URL = 'redis://127.0.0.1:6379'
limiter = Limiter(app,
                  global_limits=['10000 per hour', '100000 per day'],
                  key_func=get_remote_address,
                  # storage_uri='redis://localhost:6379/1'
                  )
limiter.init_app(app)
limiter.limit("1000 per hour")(crud_bp)
# limiter.exempt(crud_bp)


# JWT 配置
# jwt 返回jwt 获取token的键设置，将改变默认键 access_token
app.config.SANIC_JWT_ACCESS_TOKEN_NAME = 'sanic-token'
# app.config.SANIC_JWT_ACCESS_TOKEN_NAME = 'jwt'

# 设置过期时间, 默认30分钟
# app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=60)

initialize(
    app,
    authenticate=authenticate,
    # refresh_token_enabled=True,
    # store_refresh_token=store_refresh_token,
    # retrieve_refresh_token=retrieve_refresh_token,
    url_prefix='/v1/api/authentication',
    secret='fgkjhfkhgkfhkghfjdkgher5545458fjighui',
    # verify_exp = False,

    ## 标头令牌
    authorization_header='Authorization',
    authorization_header_prefix='Bearer',
    # Cookie令牌
    # cookie_domain - 更改与cooke关联的域（默认为''）
    # cookie_httponly - 是否在cookie上设置httponly标志（默认为True） 如果你是使用Cookie来传递JWTs，那么建议您不要不禁用cookie_httponly。这样做意味着客户端上运行的任何javascript都可以访问令牌。
    # cookie_access_token_name - 为访问令牌存储cookie的名称
    # cookie_refresh_token_name - 存储用于刷新令牌的cookie的名称
    cookie_set=True,
    # cookie_domain='mydomain.com',
    cookie_httponly=False,
    cookie_access_token_name='some-token',
    cookie_strict=False,


    # 设置过期时间, 默认30分钟
    # 访问令牌有效的时间长度。由于无法撤销访问令牌，因此建议将此时间段保持为短，并启用刷新令牌（可以撤销）以检索新的访问令牌。
    # 设置为一分钟
    expiration_delta=60,
)

# @app.middleware('response')
# async def response_json(request, response):
#     # if not request.path.startswith("/swagger/"):
#     response.headers["content-type"] = "application/json"

@app.exception(NotFound)
def not_found(request, exception):
    return json({
        'error_code': 'not_found',
        'message': exception.args[0] },
        status=exception.status_code,
    )

@app.exception(InvalidUsage)
def method_not_allow(request, exception):
    return json({
        'error_code': 'method_not_allow',
        'message': exception.args[0]},
        status=exception.status_code,
    )

@app.exception(ServerError)
def server_error(request, exception):
    return json({
        'error_code': 'server_error',
        'message': exception.args[0]},
        status=exception.status_code,
    )

@app.exception(RateLimitExceeded)
def rate_limit_exceeded(request, exception):
    return json({
        'error_code': 'rate_limit_error',
        'message': exception.args[0]},
        status=exception.status_code,
    )

db.db.create_tables([ShanghaiPersonInfo], safe=True)
# import_data.generate_data()






