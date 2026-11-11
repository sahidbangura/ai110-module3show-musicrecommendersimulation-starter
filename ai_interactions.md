# AI Interactions Log

All AI work for this project was done in one Claude Code session in VS Code (not separate chat windows). The prompt for each phase was the assignment text for that step. Below is what the AI was asked to do, what it produced, and what was checked by running the code.

---

## Phase 1: Understanding the problem

**Ask:** Summarize how Spotify/YouTube-style systems predict what users will like, separating collaborative filtering from content-based filtering, and name the data types involved.

**Result:** Collaborative filtering uses other users' behavior (likes, skips, playlists, listening time). Content-based filtering uses song attributes (genre, mood, tempo, energy). Real platforms combine both. With no other users in this project, only content-based filtering is possible. This is summarized in the README.

**Ask:** Which columns in `songs.csv` work best for a simple content-based recommender?

**Result:** Genre and mood are strong categorical signals; energy, valence, danceability and acousticness are good numeric ones. Tempo needs scaling because it runs from 60 to 168 BPM, not 0 to 1. I chose genre, mood and energy as the first version because they are easy to explain.

**Ask:** How should a numeric feature reward closeness, and why have both a scoring rule and a ranking rule?

**Result:** Use `1 - |song - target|` so the closest value scores highest, instead of "higher is better." The scoring rule judges one song; the ranking rule sorts all the scores. A score means nothing until songs are compared.

## Phase 2: Design

**Ask:** Generate 8 more songs in the same CSV format with genres and moods not already present.

**Result:** Songs 11 to 18 (country, EDM, R&B, hip hop, classical, folk, metal, sad lofi). **Checked:** headers and value ranges match the starter file, and the loader reads all 18 rows.

**Ask:** Critique the weights (genre +2.0, mood +1.0, energy up to +1.0) and whether the profile can tell "intense rock" from "chill lofi."

**Result:** Energy plus genre separates those two well. Risk: genre dominates, and mood and energy can't override it.

## Phase 3: Implementation

**Ask:** Implement `load_songs` with the csv module and numeric conversion; `score_song` returning `(score, reasons)`; `recommend_songs` with `sorted()`; and a readable CLI layout.

**Result:** Code in `src/recommender.py` and `src/main.py`. `sorted()` returns a new list and keeps the catalog unchanged, while `.sort()` reorders in place and returns None; I used `sorted()`.

**Fixed manually:** the starter's `from recommender import ...` fails with `python -m src.main`, so I added an import fallback. **Verified:** printed "Loaded songs: 18", and the top result for each normal profile matched what I expected. The two starter tests pass.

## Phase 4: Evaluation

**Ask:** Suggest adversarial profiles.

**Result:** "Sad but energetic" (lofi/sad/0.9) and an unknown genre ("bossa nova"), both added to `main.py`. The first showed genre and mood overpowering energy; the second showed a silent fallback to mood and energy only.

**Ask:** Explain why Gym Hero ranks second for happy pop. **Result:** genre match (+2.0) plus close energy (+0.87), with no penalty for the intense mood.

**Experiment (genre 2.0 to 1.0, energy 1.0 to 2.0).** Max score becomes 5.0 so the math stays valid. Ranks 2 and 3 swapped for the pop profile. **Verified** by running both versions and comparing the printed scores.

**Bias check on `recommender.py` and `songs.csv`:** 12 of the 14 genres appear only once, lofi is 4 of 18 songs, and exact-match strings mean "pop" and "indie pop" never match. These findings are in the model card.

## What I double-checked and what I would not trust blindly

- Scores in the README were pasted from real runs, not written by hand.
- Claims about the experiment come from actually running the changed weights.
- The AI's suggested prose (reflections) is a draft and should be read and edited before submission.
