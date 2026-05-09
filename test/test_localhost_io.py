import socket
import sys
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from network.tcp_client import TCPClient
from network.tcp_server import TCPServer
from network.udp_handler import UDPFrameReceiver, UDPFrameSender


def _free_port(protocol: str = "tcp") -> int:
    sock_type = socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM
    with socket.socket(socket.AF_INET, sock_type) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def test_tcp_client_server_roundtrip():
    port = _free_port("tcp")

    def handler(request):
        return {"ok": True, "echo": request}

    server = TCPServer("127.0.0.1", port, handler)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.2)

    client = TCPClient("127.0.0.1", port, timeout=3.0)
    response = client.send_request({"type": "ping", "payload": {"n": 1}})

    assert response == {"ok": True, "echo": {"type": "ping", "payload": {"n": 1}}}


def test_udp_chunk_reassembly_roundtrip():
    port = _free_port("udp")
    receiver = UDPFrameReceiver("127.0.0.1", port)
    sender = UDPFrameSender("127.0.0.1", port)
    payload = b"fake-jpeg-frame" * 5000
    received = []

    def receive_once():
        for data in receiver.receive_packets():
            received.append(data)
            break

    thread = threading.Thread(target=receive_once, daemon=True)
    thread.start()
    time.sleep(0.1)
    sender.send_frame_raw(payload)
    thread.join(timeout=3.0)

    assert received == [payload]
