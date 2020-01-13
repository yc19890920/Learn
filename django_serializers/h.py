import uuid
import time
import hashlib

def get_hashID(username, hashMode=64, tablePiece=4):
    """根据 username 确定唯一 hash 值（确定分表）
     # 分组公式：64 = 每组多少个count  * group需要分组的个数
     # 数据所在环的位置（也就是在哪个库中）：value = key mode 64 / count  * count

    hash(key)在0~3之间在第0号表
    hash(key)在4~7之间在第4号表
    hash(key)在8~11之间在第8号表

    hash(key)在0~3之间在第0号库
    hash(key)在4~7之间在第4号库
    hash(key)在8~11之间在第8号库
    """
    # hash = int
    hashID = int(hash(username) % hashMode / tablePiece )
    return hashID
    # # 16进制 -- 900150983cd24fb0d6963f7d28e17f72
    # hash_str = hashlib.md5(username.lower().encode(encoding='UTF-8')).hexdigest()
    # userId = int(hash_str, 16)  # 16进制 --> 10进制
    # # print(hash_str, hash_str[:2], hash_str[-2:], num)
    # # 按hashCount个为一组，分4个表
    # hashID = int(hash(username) % hashMode / tablePiece)
    # # hashID = num % hashNum
    # # print('HashID:', hashID)
    # return hashI

def get_sharding_model(username):
    table_id = get_hashID(username, hashMode=2, tablePiece=1)
    if table_id == 0:
        return 1
    elif table_id == 1:
        return 2

# 4124bc0a9335c27f086f24ba207a4912 41 12 16658
# HashID: 0
# 4124bc0a9335c27f086f24ba207a4912 41 12 16658
# HashID: 0

H = []
count = 0
while count <= 64:
    username = str(uuid.uuid4())
    # username = str(count)
    # hashID = get_hashID(username)
    print(get_sharding_model(username))
    count += 1
    # time.sleep(0.1)
    # if hashID not in H:
    #     H.append(hashID)

H.sort()
print(H)