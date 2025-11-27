# tests/test_chatbot.py
import re
from datetime import datetime, timezone

from chatBot import detect_intent, echo_response, handle_intent


def test_detect_intent_greet():
    assert detect_intent("Hallo") == "greet"
    assert detect_intent("guten Morgen") == "greet"


def test_detect_intent_time():
    assert detect_intent("Wie spät ist es?") == "time"
    assert detect_intent("uhr") == "time"


def test_detect_intent_unknown():
    assert detect_intent("das ist etwas anderes") == "unknown"


def test_echo_response():
    resp = echo_response("  test  ")
    assert "test" in resp
    assert "Länge: 4" in resp


def test_handle_intent_time_format():
    resp = handle_intent("time", "")
    # Expect prefix and an ISO-ish datetime string portion (YYYY-)
    assert resp.startswith("Aktuelle Uhrzeit (UTC): ")
    ts = resp.split(": ", 1)[1]
    # basic check for valid formatting
    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", ts)
