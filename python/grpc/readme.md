- [grpc/examples/python/](https://github.com/grpc/grpc/tree/master/examples/python)
- [Python gRPC 入门](https://juejin.im/post/5b19590b6fb9a01e4b062391)


1. 安装 gRPC
python -m pip install grpcio
# 或者
sudo python -m pip install grpcio

# 在 El Capitan OSX 系统下可能会看到以下报错
$ OSError: [Errno 1] Operation not permitted: '/tmp/pip-qwTLbI-uninstall/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/six-1.4.1-py2.7.egg-info'

# 可以使用以下命令
python -m pip install grpcio --ignore-installed

2. 安装 gRPC tools
Python gPRC tools 包含 protocol buffer 编译器和用于从 .proto 文件生成服务端和客户端代码的插件
python -m pip install grpcio-tools


3. Python gRPC 示例
这里我们用Python 编译一下，看得到什么：
```
// 文件名 hello.proto
syntax = "proto3";

package hello;

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```
使用以下命令编译:
python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./hello.proto

生成了两个文件：
hello_pb2.py 此文件包含生成的 request(HelloRequest) 和 response(HelloReply) 类。
hello_pb2_grpc.py 此文件包含生成的 客户端(GreeterStub)和服务端(GreeterServicer)的类。

虽然现在已经生成了服务端和客户端代码，但是我们还需要手动实现以及调用的方法。


4. 创建服务端代码
创建和运行 Greeter 服务可以分为两个部分：
实现我们服务定义的生成的服务接口：做我们的服务的实际的“工作”的函数。
运行一个 gRPC 服务器，监听来自客户端的请求并传输服务的响应。
在当前目录，打开文件 greeter_server.py，实现一个新的函数：
```
from concurrent import futures
import time

import grpc

import hello_pb2
import hello_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(hello_pb2_grpc.GreeterServicer):
	# 工作函数
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    # gRPC 服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()  # start() 不会阻塞，如果运行时你的代码没有其它的事情可做，你可能需要循环等待。
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
```

5. 更新客户端代码
在当前目录，打开文件 greeter_client.py，实现一个新的函数：
```
from __future__ import print_function

import grpc

import hello_pb2
import hello_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = hello_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(hello_pb2.HelloRequest(name='goodspeed'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
```

对于返回单个应答的 RPC 方法（"response-unary" 方法），gRPC Python 同时支持同步（阻塞）和异步（非阻塞）的控制流语义。
对于应答流式 RPC 方法，调用会立即返回一个应答值的迭代器。调用迭代器的 next() 方法会阻塞，直到从迭代器产生的应答变得可用。

首先运行服务端代码
python greeter_server.py

然后运行客户端代码
python greeter_client.py

# output
Greeter client received: Hello, goodspeed!
