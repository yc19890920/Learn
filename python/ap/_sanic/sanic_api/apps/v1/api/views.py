try:
    import ujson
except:
    import json as ujson
from sanic.response import json
from playhouse.shortcuts import model_to_dict
from .models import ShanghaiPersonInfo
from apps.utils.helper import list_remove_repeat
from apps.utils.drf import order_list_api
from sanic_jwt import protected, scoped
from sanic import Blueprint
from sanic_openapi import doc
"""
@user_bp.post('/')
@doc.summary('create user')
@doc.description('create user info')
@doc.consumes(Users)
@doc.produces({'id': int})
async def create_user(request):
    data = request['data']
    async with request.app.db.transaction(request) as cur:
        record = await cur.fetchrow(
            \""" INSERT INTO users(name, age, city_id, role_id)
                VALUES($1, $2, $3, $4, $5)
                RETURNING id
            \""", data['name'], data['age'], data['city_id'], data['role_id']
        )
        return {'id': record['id']}

summary: api概要
description: 详细描述
consumes: request的body数据
produces: response的返回数据
tag: API标签
在consumes和produces中传入的参数可以是peewee的model,会解析model生成API数据, 在field字段的help_text参数来表示引用对象
http://host:ip/openapi/spec.json 获取生成的json数据

"""

crud_bp = Blueprint('crud', url_prefix='/api/v1/persons')

@crud_bp.route('/', methods=['GET', 'POST'])
@protected()
@doc.summary("Fetches persons")
@doc.consumes(ShanghaiPersonInfo)
# @doc.produces({ "user": { "name": str, "id": int } })
async def persons(request):
    if request.method == "POST":
        j = request.json
        if j:
            obj = ShanghaiPersonInfo.create(**j[0])
            return json(obj.model_to_dict())
        return json({})

    page = int(request.args.get('page', 1))
    max_per_page = request.app.config['MAX_PER_PAGE']
    sex, email, username = request.args.get('sex'), request.args.get('email'), request.args.get('username')
    qs = ShanghaiPersonInfo.filters(
        sex=sex, email=email, username=username, page_number=page, items_per_page=max_per_page)
    result = [model_to_dict(row) for row in qs.result.iterator()]
    total = ShanghaiPersonInfo.filters(sex=sex, email=email, username=username).counts()
    data = order_list_api(request, result, page, max_per_page, total)
    return json(data)

@crud_bp.route('/detail/<item_id:int>', methods=['GET', 'PUT'])
@protected()
async def person_detail(request, item_id):
    if request.method == "PUT":
        update_data = eval(request.body.decode())
        qs = ShanghaiPersonInfo.update(**update_data).where(ShanghaiPersonInfo.id == item_id)
        qs.execute()
        new_data = ShanghaiPersonInfo.get(id=item_id)
        return json(model_to_dict(new_data))

    data = ShanghaiPersonInfo.get(id=item_id)
    return json(model_to_dict(data))


@crud_bp.route('/sex', methods=['GET'])
@protected()
async def person_detail(request):
    unique_list = list_remove_repeat(ShanghaiPersonInfo.values_list('sex'))
    result = [dict(label=i, value=i) for i in unique_list]
    return json(result)

