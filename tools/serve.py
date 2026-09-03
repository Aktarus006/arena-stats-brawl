#!/usr/bin/env python3
"""Serve the dashboard locally and accept match reports from the browser."""

from __future__ import annotations

import json
import subprocess
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from web_api import create_game

ROOT = Path(__file__).resolve().parents[1]


class ArenaLabHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/games":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 20_000:
                raise ValueError("Request body must be between 1 and 20,000 bytes")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Request body must be a JSON object")
            game = create_game(ROOT, payload)
            subprocess.run(["python3", str(ROOT / "tools" / "build_data.py")], check=True, capture_output=True, text=True)
        except (ValueError, json.JSONDecodeError) as error:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return
        except subprocess.CalledProcessError as error:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Data rebuild failed: {error.stderr}"})
            return
        self._json(HTTPStatus.CREATED, {"game": game})

    def _json(self, status: HTTPStatus, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 4173), ArenaLabHandler)
    print("Arena Brawl Lab running at http://127.0.0.1:4173/site/")
    server.serve_forever()


if __name__ == "__main__":
    main()
