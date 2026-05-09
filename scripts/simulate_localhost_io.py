"""Run local TCP/UDP simulation without cameras, DB, or a physical cart.

The script validates:
1. Length-prefixed TCP JSON request/response path.
2. UDP chunking and reassembly path using synthetic JPEG-like bytes.

Usage:
    python scripts/simulate_localhost_io.py
"""

from __future__ import annotations

import json
import socket
import sys
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from network.tcp_client import TCPClient  # noqa: E402
from network.tcp_server import TCPServer  # noqa: E402
from network.udp_handler import UDPFrameReceiver, UDPFrameSender  # noqa: E402


def get_free_port(protocol: str = "tcp") -> int:
    sock_type = socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM
    with socket.socket(socket.AF_INET, sock_type) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def run_tcp_check() -> dict:
    port = get_free_port("tcp")

    def handler(request: dict) -> dict:
        return {
            "ok": True,
            "received_type": request.get("type"),
            "payload": request.get("payload", {}),
        }

    server = TCPServer("127.0.0.1", port, handler)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.2)

    client = TCPClient("127.0.0.1", port, timeout=3.0)
    response = client.send_request({"type": "AI_EVT", "payload": {"level": "CAUTION"}})
    return {"response": response}


def run_udp_check() -> dict:
    port = get_free_port("udp")
    receiver = UDPFrameReceiver("127.0.0.1", port)
    sender = UDPFrameSender("127.0.0.1", port)

    payload = b"fake-jpeg-frame" * 5000
    received: list[bytes] = []

    def receive_once():
        for data in receiver.receive_packets():
            received.append(data)
            break

    thread = threading.Thread(target=receive_once, daemon=True)
    thread.start()
    time.sleep(0.1)
    sender.send_frame_raw(payload)
    thread.join(timeout=3.0)

    return {
        "sent_bytes": len(payload),
        "received_bytes": len(received[0]) if received else 0,
        "matched": bool(received and received[0] == payload),
    }


def main() -> int:
    tcp_result = run_tcp_check()
    udp_result = run_udp_check()
    result = {"tcp": tcp_result, "udp": udp_result}
    print(json.dumps(result, ensure_ascii=False, indent=2))

    ok = tcp_result["response"] and tcp_result["response"].get("ok") and udp_result["matched"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
