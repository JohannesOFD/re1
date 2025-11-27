#!/usr/bin/env python3
# hello.py - einfacher lokaler Chatbot zum Testen (UTC mit timezone-aware datetime)

import random
import sys
from datetime import datetime, timezone

LOGFILE = "chatbot.log"

INTENTS = {
    "greet": ["hallo", "hi", "hey", "guten", "moin"],
    "time": ["uhr", "zeit", "wie spät"],
    "joke": ["witz", "erzähl", "witzig", "witz?"],
    "bye": ["tschüss", "bye", "auf wiedersehen", "ende", "quit", "exit"],
}

JOKES = [
    "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann.",
    "Was macht ein Keks unter einem Baum? Krümel.",
    "Warum ging der Pilz auf die Party? Weil er ein Champignon war.",
]


def log(message: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} {message}\n")


def detect_intent(text: str) -> str:
    t = text.lower()
    for intent, triggers in INTENTS.items():
        for trig in triggers:
            if trig in t:
                return intent
    return "unknown"


def handle_intent(intent: str, text: str) -> str:
    if intent == "greet":
        return "Hallo! Wie kann ich dir helfen?"
    if intent == "time":
        return "Aktuelle Uhrzeit (UTC): " + datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    if intent == "joke":
        return random.choice(JOKES)
    if intent == "bye":
        return 5
    return echo_response(text)


def echo_response(text: str) -> str:
    text_stripped = text.strip()
    return f'Du hast gesagt: "{text_stripped}" (Länge: {len(text_stripped)})'


def interactive_loop():
    print("Einfacher Chatbot. Tippe 'ende' oder Ctrl+C zum Beenden.")
    log("Session started")
    try:
        while True:
            user = input(">> ").strip()
            log(f"USER: {user}")
            if not user:
                print("Bitte etwas eingeben.")
                continue
            intent = detect_intent(user)
            resp = handle_intent(intent, user)
            print(resp)
            log(f"BOT: {resp}")
            if intent == "bye":
                break
    except KeyboardInterrupt:
        print("\nBeende per Tastatur.")
        log("Session interrupted by KeyboardInterrupt")
    except Exception as e:
        err = f"Error: {e}"
        print(err)
        log(err)
    finally:
        log("Session ended")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        intent = detect_intent(query)
        resp = handle_intent(intent, query)
        print(resp)
        log(f"CLI MODE - USER: {query} BOT: {resp}")
        sys.exit(0)

    interactive_loop()
