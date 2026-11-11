# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**VibeFinder 1.0** is a command-line, content-based music recommender. It loads an 18-song catalog from `data/songs.csv`, scores every song against a user's taste profile (genre, mood, target energy), and prints the top 5 with a plain-language reason for each score.

---

## How The System Works

**Real-world systems.** Services like Spotify and YouTube mix two ideas. *Collaborative filtering* uses other people's behavior (likes, skips, playlists, listening time): "people like you also played this." *Content-based filtering* uses the song's own attributes (genre, mood, tempo, energy). Real platforms blend both at huge scale. My version is purely content-based: it has no other users, so it can only compare a song's attributes to one profile.

**Features**

- `Song`: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness. Scoring uses genre, mood and energy.
- `UserProfile`: favorite_genre, favorite_mood, target_energy, likes_acoustic (the functional API uses the dict `{"genre", "mood", "energy"}`).

**Algorithm Recipe** (score range 0 to 4)

- +2.0 if the song's genre equals the favorite genre
- +1.0 if the song's mood equals the favorite mood
- 0 to +1.0 for energy: `1.0 * (1 - |song_energy - target_energy|)`, so closer is better (rewards closeness, not just high or low values)

`score_song` judges one song and returns `(score, reasons)`. `recommend_songs` is the ranking rule: it scores every song, sorts high to low with `sorted()`, and returns the top k. Both are needed because a score means nothing until songs are compared against each other.

**Data flow:** user prefs -> loop over every CSV row with `score_song` -> sort -> top-k with reasons.

**Expected biases:** genre is worth twice a mood match, so the system may bury a great mood/energy match in a different genre. Exact string matching means "pop" and "indie pop" are unrelated. Genres with only one song can show at most one strong result.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` (5 profiles; the first three are normal users, the last two are edge cases):

```
Loaded songs: 18

================================================================
Profile: High-Energy Pop  {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
================================================================
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 3.98 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.80 (+0.98)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 2.87 / 4.00
     - genre match (+2.0)
     - energy 0.93 vs target 0.80 (+0.87)
3. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 1.96 / 4.00
     - mood match (+1.0)
     - energy 0.76 vs target 0.80 (+0.96)
4. Concrete Gospel by Ruin Verse  [hip hop/aggressive]
   Score: 0.95 / 4.00
     - energy 0.85 vs target 0.80 (+0.95)
5. Night Drive Loop by Neon Echo  [synthwave/moody]
   Score: 0.95 / 4.00
     - energy 0.75 vs target 0.80 (+0.95)

================================================================
Profile: Chill Lofi  {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
================================================================
1. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 4.00 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.35 (+1.00)
2. Midnight Coding by LoRoom  [lofi/chill]
   Score: 3.93 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.35 (+0.93)
3. Focus Flow by LoRoom  [lofi/focused]
   Score: 2.95 / 4.00
     - genre match (+2.0)
     - energy 0.40 vs target 0.35 (+0.95)
4. Rainy Window by Paper Lanterns  [lofi/sad]
   Score: 2.95 / 4.00
     - genre match (+2.0)
     - energy 0.30 vs target 0.35 (+0.95)
5. Spacewalk Thoughts by Orbit Bloom  [ambient/chill]
   Score: 1.93 / 4.00
     - mood match (+1.0)
     - energy 0.28 vs target 0.35 (+0.93)

================================================================
Profile: Deep Intense Rock  {'genre': 'rock', 'mood': 'intense', 'energy': 0.92}
================================================================
1. Storm Runner by Voltline  [rock/intense]
   Score: 3.99 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.91 vs target 0.92 (+0.99)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 1.99 / 4.00
     - mood match (+1.0)
     - energy 0.93 vs target 0.92 (+0.99)
3. Neon Cathedral by Pulse Theory  [edm/euphoric]
   Score: 0.96 / 4.00
     - energy 0.96 vs target 0.92 (+0.96)
4. Ironclad by Black Anvil  [metal/aggressive]
   Score: 0.95 / 4.00
     - energy 0.97 vs target 0.92 (+0.95)
5. Concrete Gospel by Ruin Verse  [hip hop/aggressive]
   Score: 0.93 / 4.00
     - energy 0.85 vs target 0.92 (+0.93)

================================================================
Profile: Conflicting (sad but energetic)  {'genre': 'lofi', 'mood': 'sad', 'energy': 0.9}
================================================================
1. Rainy Window by Paper Lanterns  [lofi/sad]
   Score: 3.40 / 4.00
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.30 vs target 0.90 (+0.40)
2. Midnight Coding by LoRoom  [lofi/chill]
   Score: 2.52 / 4.00
     - genre match (+2.0)
     - energy 0.42 vs target 0.90 (+0.52)
3. Focus Flow by LoRoom  [lofi/focused]
   Score: 2.50 / 4.00
     - genre match (+2.0)
     - energy 0.40 vs target 0.90 (+0.50)
4. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 2.45 / 4.00
     - genre match (+2.0)
     - energy 0.35 vs target 0.90 (+0.45)
5. Storm Runner by Voltline  [rock/intense]
   Score: 0.99 / 4.00
     - energy 0.91 vs target 0.90 (+0.99)

================================================================
Profile: Unknown genre (bossa nova)  {'genre': 'bossa nova', 'mood': 'relaxed', 'energy': 0.4}
================================================================
1. Coffee Shop Stories by Slow Stereo  [jazz/relaxed]
   Score: 1.97 / 4.00
     - mood match (+1.0)
     - energy 0.37 vs target 0.40 (+0.97)
2. Focus Flow by LoRoom  [lofi/focused]
   Score: 1.00 / 4.00
     - energy 0.40 vs target 0.40 (+1.00)
3. Midnight Coding by LoRoom  [lofi/chill]
   Score: 0.98 / 4.00
     - energy 0.42 vs target 0.40 (+0.98)
4. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 0.95 / 4.00
     - energy 0.35 vs target 0.40 (+0.95)
5. Salt & Ember by Harbor Folk  [folk/nostalgic]
   Score: 0.93 / 4.00
     - energy 0.33 vs target 0.40 (+0.93)
```

---

## Experiments You Tried

**Weight shift (genre 2.0 -> 1.0, energy 1.0 -> 2.0).** Top 5 for "High-Energy Pop" before: Sunrise City, Gym Hero, Rooftop Lights, Concrete Gospel, Night Drive Loop. After: Sunrise City, Rooftop Lights, Gym Hero, Concrete Gospel, Night Drive Loop. Max score became 5.0, so the math stays valid, but only the order of ranks 2 and 3 changed. "Chill Lofi" kept the same top 5 but the lofi/ambient gap narrowed. The change made results *different* more than *more accurate*: Rooftop Lights (indie pop, happy) arguably fits a happy-pop fan better than Gym Hero (intense), so this is a small improvement for that profile.

**Edge cases.** "Sad but energetic" (lofi, sad, 0.9) returns slow lofi songs because genre + mood (3.0) outweigh the large energy gap. An unknown genre ("bossa nova") silently falls back to mood + energy only.

---

## Limitations and Risks

- Tiny catalog (18 songs); most genres have one song.
- Genre and mood are exact-match strings, with no notion of similarity ("pop" vs "indie pop", "chill" vs "relaxed").
- Genre dominates, so it can create a filter bubble and hide cross-genre songs.
- Ignores tempo, valence, danceability, acousticness, lyrics and language.
- No listening history, so it cannot learn or adapt.

See [model_card.md](model_card.md) for details.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

*Draft written with AI assistance; edit in your own words.*

Recommenders turn data into predictions by comparing numbers and labels: a few additions and a distance calculation were enough to produce a ranked list that felt like real recommendations. The reasons list made each ranking easy to audit, and that is how I found problems, such as Gym Hero appearing for happy-pop fans.

Bias shows up through weights and data. Genre is worth twice a mood match, so users with mixed tastes get stuck in one genre, and genres with a single song get thin results. Real systems have the same risk at scale: whatever the scoring rule over-values becomes a filter bubble.
