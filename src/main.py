"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:  # running as `python src/main.py`
    from recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    # Adversarial / edge cases
    "Conflicting (sad but energetic)": {"genre": "lofi", "mood": "sad", "energy": 0.9},
    "Unknown genre (bossa nova)": {"genre": "bossa nova", "mood": "relaxed", "energy": 0.4},
}


def print_recommendations(name: str, prefs: dict, songs: list, k: int = 5) -> None:
    """Print a profile and its top k recommendations."""
    print("=" * 64)
    print(f"Profile: {name}  {prefs}")
    print("=" * 64)
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k), 1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}/{song['mood']}]")
        print(f"   Score: {score:.2f} / 4.00")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
