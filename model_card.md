# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Intended Use

VibeFinder suggests up to 5 songs from a small catalog that match a user's favorite genre, favorite mood and target energy level. It is for classroom exploration, not real users.

**Not intended for:** real streaming products, judging artists, or making decisions about people. It assumes one fixed taste per user and has no listening history.

---

## 3. How the Model Works

Every song gets a score out of 4 points:

- **Genre:** 2 points if the genre is the one the user likes.
- **Mood:** 1 point if the mood is the one the user likes.
- **Energy:** up to 1 point. The closer the song's energy is to the user's target, the more points. A song exactly on target gets 1; a song at the opposite end gets 0.

The program scores every song, sorts them from highest to lowest, and shows the top 5. Each result lists the reasons for its points, so the user can see why it was picked.

---

## 4. Data

- 18 songs in `data/songs.csv`: the 10 starter songs plus 8 I added (country, EDM, R&B, hip hop, classical, folk, metal, and a sad lofi track).
- Features per song: genre, mood, energy, tempo, valence, danceability, acousticness. Only genre, mood and energy are scored.
- Many genres have just one song, and lofi has four. Real taste (language, lyrics, era, artist) is missing.

---

## 5. Strengths

- Clear, normal profiles work well. "Chill Lofi" returns the two lofi/chill songs first, and "Deep Intense Rock" returns Storm Runner first, as I expected.
- Every result is explainable because it lists its reasons.
- The energy rule rewards closeness, so a low-energy user gets calm songs and not just "low numbers."

---

## 6. Limitations and Bias

Genre is worth twice as much as mood and exact-match only, so the system over-rewards genre. In the "sad but energetic" test (lofi, sad, energy 0.9), the top four results were all slow lofi songs with energy between 0.30 and 0.42. The user asked for high energy, but the genre and mood points (3.0 total) outweighed the energy gap. Meanwhile, Storm Runner (rock, energy 0.91), which matched the energy, ranked 5th. Because "pop" and "indie pop" count as different genres, a pop fan only sees indie pop through its mood match. Genres with one song (jazz, metal, folk) can never fill a top-5 list with on-genre results, so fans of small genres get filler songs after the first result.

---

## 7. Evaluation

**Profiles tested:** High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases (Conflicting: sad but energetic; Unknown genre: bossa nova). Outputs are in the README.

**What I checked:** whether the top result matched my own sense of the profile, and whether the reasons made sense.

**Pair comparisons:**

- *Pop vs. Chill Lofi:* pop returns bright, fast songs (Sunrise City, Rooftop Lights); lofi switches to slow, acoustic songs (Library Rain, Midnight Coding). That makes sense because the energy targets are 0.8 and 0.35.
- *Pop vs. Rock:* both like high energy, so Gym Hero shows up in both lists. For pop it matches on genre; for rock it matches on mood ("intense") and energy.
- *Chill Lofi vs. Conflicting:* both pick lofi, but with a high energy target the list loses its confident top and every score drops (4.00 to 3.40). It still shows slow songs, which exposes the genre weight.
- *Rock vs. Unknown genre:* with a real genre the top song scores about 4.0; with a missing genre nobody gets genre points, and the best score is just 1.97.

**Surprise, in plain language:** "Gym Hero" keeps showing up for happy-pop fans. It is a pop song, so it gets the big genre bonus, and its energy is close to what a high-energy user wants. The system never checks that the mood is "intense," not "happy." It only awards points when moods match and never subtracts for a mismatch, so a workout song looks like a fine happy song.

**Experiment:** I halved genre (2.0 to 1.0) and doubled energy (1.0 to 2.0). Rankings barely moved. Rooftop Lights (happy) moved above Gym Hero (intense) for the pop profile, which feels more right. The change made results a bit more accurate for that profile, but mostly just different.

---

## 8. Future Work

- Treat related genres and moods as partly similar (indie pop is close to pop) instead of all-or-nothing.
- Use valence, danceability and acousticness (the `likes_acoustic` field is currently unused).
- Add a diversity rule so the top 5 can't all come from one genre or artist, and grow the catalog.

---

## 9. Personal Reflection

**Biggest learning moment.** A recommender can be very simple and still feel smart. Three additions (genre, mood, energy closeness) produced lists I agreed with for the normal profiles. The weirdness only showed up in the edge cases, which is where the real design problems live.

**How AI helped, and where I double-checked it.** I used an AI assistant to research how real systems work, write the first version of the code, expand the dataset and suggest edge-case profiles. I did not accept anything unchecked: I ran the program, compared the printed scores with the numbers in my write-up, fixed an import error from the starter code, and re-ran the weight experiment myself to confirm the rank change was real. The AI is fast at drafts but can state things confidently without testing them, so the run-and-compare step mattered most.

**What surprised me.** The "Gym Hero for happy pop" result. Nothing is broken: the rules are just blind to the difference between intense and happy because a mood mismatch costs nothing. The explanations made that bug easy to see, which is why I would keep them in any real system.

**What I would try next.** Give related genres and moods partial credit, use valence and acousticness, add a diversity rule for the top 5, and test with a much bigger catalog to see whether the genre bias gets better or just moves.
