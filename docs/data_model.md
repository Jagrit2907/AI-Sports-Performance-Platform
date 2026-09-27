# Version 1 Data Model

## Raw entities

### competitions
- competition_id
- competition_name
- season_id
- season_name
- competition_gender
- competition_youth
- competition_international
- match availability metadata

### matches
- match_id
- competition context
- season context
- match_date
- kick_off
- home team
- away team
- score
- competition_stage
- match_week

### lineups
- team_id
- player_id
- player_name
- country
- jersey_number
- position intervals
- substitution/start/end context

### events
- event_id
- index
- period
- timestamp
- event_type
- possession
- possession_team
- play_pattern
- team
- player
- position
- location
- event-specific attributes (pass, shot, carry, duel, pressure, etc.)

### optional 360
- event_uuid
- visible_area
- freeze_frame player locations

## Derived analytical tables

### player_match
One row per player-match observation.

### player_match_stats
One row per player-match with engineered event counts/rates.

### player_profile
One row per player for the chosen aggregation window.

### peer_baseline
Position/context-specific distributions used for percentile or standardized comparisons.

### player_similarity
Pairwise similarity results from the scaled feature representation.

### player_clusters
Cluster assignment plus diagnostics and cluster summaries.

### talent_shortlist
Transparent statistical shortlist with evidence fields.

### recommendations
Rule-based development suggestions linked to supporting metrics.
