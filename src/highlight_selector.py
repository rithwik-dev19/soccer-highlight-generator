def calculate_excitement_score(match):
    """
    Scores a match based on how exciting it is.
    Higher score = better highlight candidate.
    """
    score = 0
    home = match["home_score"]
    away = match["away_score"]
    total = match["total_goals"]
    diff = abs(home - away)

    # More goals = more exciting
    score += total * 10

    # Big upsets (underdog winning away) = exciting
    if away > home:
        score += 15

    # Thrashings (5+ goal difference) = very highlight worthy
    if diff >= 5:
        score += 30

    # Close high scoring games = exciting
    if total >= 4 and diff <= 1:
        score += 20

    return score

def pick_best_match(matches):
    """
    Picks the single most highlight-worthy match
    """
    if not matches:
        print("❌ No matches to pick from")
        return None

    # Score every match
    for match in matches:
        match["excitement_score"] = calculate_excitement_score(match)

    # Pick the highest scored match
    best = max(matches, key=lambda x: x["excitement_score"])

    return best

def describe_match(match):
    """
    Generates a human readable description of why this match is exciting
    """
    home = match["home_score"]
    away = match["away_score"]
    diff = abs(home - away)
    total = match["total_goals"]
    winner = match["home_team"] if home > away else match["away_team"]
    loser = match["away_team"] if home > away else match["home_team"]

    reasons = []

    if diff >= 5:
        reasons.append(f"massive {diff}-goal thrashing")
    if total >= 6:
        reasons.append(f"goal fest with {total} goals")
    if away > home:
        reasons.append("away team dominated")
    if diff <= 1 and total >= 4:
        reasons.append("thrilling close contest")

    reason_str = " + ".join(reasons) if reasons else "solid performance"

    return {
        "headline": f"{winner} destroy {loser} {match['score_str']}",
        "reason": reason_str,
        "league": match["league"],
        "country": match["country"],
        "excitement_score": match["excitement_score"]
    }

# Test it
if __name__ == "__main__":
    # Import and use real data
    from data_fetcher import get_matches_by_date

    matches = get_matches_by_date("2026-06-15")

    if matches:
        best_match = pick_best_match(matches)
        description = describe_match(best_match)

        print("\n🏆 TODAY'S HIGHLIGHT MATCH:")
        print(f"  Headline : {description['headline']}")
        print(f"  Reason   : {description['reason']}")
        print(f"  League   : {description['league']} ({description['country']})")
        print(f"  Excitement Score: {description['excitement_score']}")
        