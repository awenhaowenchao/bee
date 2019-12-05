from gevent import monkey;monkey.patch_all()
from gevent import socket

from bee.data.option import Option
from bee.data.map import Map
from bee.net.rpc.channel import Channel
from bee.net.rpc.codec import RequestHead, Request, ResponseHead, Result
from bee.net.rpc.codecs.proto.proto import Builder

id = 1

sock = socket.create_connection(address=("127.0.0.1", 8080));
print(sock.closed)
while id<5:

    rh = RequestHead()
    rh.id = id
    rh.service = "Test"
    rh.method = "hello"
    rh.labels = [Option(name="test", value="test")]

    r = Request(head=rh, args=["Mr. " + str(id)])
    cc = Builder().new_client_codec(s=Channel(id="", sock=sock), opts=Map())
    cc.encode(req=r)

    rh = ResponseHead()
    cc.decode_head(rh)
    rt = Result()
    cc.decode_result(rt)
    print(rt.value)

    # length_data = sock.recv(4)
    # length = int.from_bytes(length_data, byteorder="little")
    # if length > 0:
    #     data = sock.recv(length)
    #     print(data)

    id +=1


