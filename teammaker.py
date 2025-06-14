from typing import List, Dict
from collections import defaultdict
import heapq

class Player:
    def __init__(self, name: str, primary_skill: str, secondary_skills: List[str], skill_point: int):
        self.name = name
        self.primary_skill = primary_skill
        self.secondary_skills = secondary_skills
        self.skill_point = skill_point

    def __repr__(self):
        return f"{self.name} ({self.primary_skill}, {self.skill_point})"


def balance_teams(players: List[Player]) -> Dict[str, List[Player]]:
    roles = ['gk', 'defender', 'striker']
    role_buckets = {role: [] for role in roles}
    fallback_bucket = []

    # Step 1: Categorize players by primary skill
    for player in players:
        if player.primary_skill in roles:
            role_buckets[player.primary_skill].append(player)
        else:
            fallback_bucket.append(player)

    # Step 2: Fill missing roles using secondary skills
    for role in roles:
        if not role_buckets[role]:
            for p in fallback_bucket:
                if role in p.secondary_skills:
                    role_buckets[role].append(p)
                    fallback_bucket.remove(p)
                    break

    # Step 3: Sort all players by skill points descending
    sorted_players = sorted(players, key=lambda p: p.skill_point, reverse=True)

    team_a = []
    team_b = []

    # Step 4: Assign key roles evenly first
    for role in roles:
        candidates = sorted(role_buckets[role], key=lambda p: p.skill_point, reverse=True)
        for i, p in enumerate(candidates[:2]):
            if i % 2 == 0:
                team_a.append(p)
            else:
                team_b.append(p)

    assigned_names = set(p.name for p in team_a + team_b)
    remaining_players = [p for p in sorted_players if p.name not in assigned_names]

    # Step 5: Distribute remaining players alternately
    for i, p in enumerate(remaining_players):
        if len(team_a) <= len(team_b):
            team_a.append(p)
        else:
            team_b.append(p)

    extra_player = None
    if len(players) % 2 != 0:
        if len(team_a) > len(team_b):
            extra_player = team_a.pop()
        else:
            extra_player = team_b.pop()

    return {
        'team_a': team_a,
        'team_b': team_b,
        'extra_player': extra_player
    }

# Example usage
if __name__ == "__main__":
    players = [
        Player("Alice", "gk", ["defender"], 80),
        Player("Bob", "striker", ["defender"], 85),
        Player("Charlie", "defender", ["gk"], 75),
        Player("Diana", "striker", ["gk"], 70),
        Player("Ethan", "defender", ["striker"], 90),
        Player("Fiona", "gk", ["striker"], 65),
        Player("George", "striker", ["defender"], 60),
    ]

    result = balance_teams(players)
    print("Team A:", result['team_a'])
    print("Team B:", result['team_b'])
    if result['extra_player']:
        print("Extra player (plays one half for each team):", result['extra_player'])
