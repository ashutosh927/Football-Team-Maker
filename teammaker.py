from typing import List, Dict
from collections import defaultdict

class Player:
    def __init__(self, name: str, primary_skill: str, secondary_skills: List[str], skill_point: float):
        self.name = name
        self.primary_skill = primary_skill
        self.secondary_skills = secondary_skills
        self.skill_point = skill_point

    def __repr__(self):
        return f"{self.name} ({self.primary_skill}, {self.skill_point})"


def balance_teams(players: List[Player]) -> Dict[str, List[Player]]:
    roles = ['gk', 'defender', 'striker']
    team_a = []
    team_b = []

    # Step 1: Sort players by skill point descending
    sorted_players = sorted(players, key=lambda p: p.skill_point, reverse=True)

    # Step 2: Distribute players alternately to balance skill points
    for i, player in enumerate(sorted_players):
        if len(team_a) <= len(team_b):
            team_a.append(player)
        else:
            team_b.append(player)

    # Step 3: Ensure each team has at least one of each role
    def ensure_roles(team: List[Player], fallback_team: List[Player]):
        team_roles = {role: None for role in roles}
        for player in team:
            if player.primary_skill in roles and not team_roles[player.primary_skill]:
                team_roles[player.primary_skill] = player

        for role in roles:
            if not team_roles[role]:
                # Try to find someone in the same team with the secondary skill
                for player in team:
                    if role in player.secondary_skills:
                        team_roles[role] = player
                        break

        for role in roles:
            if not team_roles[role]:
                # Try to borrow from fallback team
                for player in fallback_team:
                    if player.primary_skill == role or role in player.secondary_skills:
                        team.append(player)
                        fallback_team.remove(player)
                        break

    ensure_roles(team_a, team_b)
    ensure_roles(team_b, team_a)

    # Step 4: Handle odd player out
    extra_player = None
    if len(players) % 2 != 0:
        if len(team_a) > len(team_b):
            extra_player = team_a.pop()
        elif len(team_b) > len(team_a):
            extra_player = team_b.pop()

    return {
        'team_a': team_a,
        'team_b': team_b,
        'extra_player': extra_player
    }

# Store all registered players
registered_players = []

def add_player(name: str, primary: str, secondary: List[str], skill_point: float):
    registered_players.append(Player(name, primary, secondary, skill_point))

def select_players_for_round() -> List[Player]:
    print("\nRegistered players:")
    for idx, p in enumerate(registered_players):
        print(f"{idx + 1}. {p.name} (Primary: {p.primary_skill}, Secondary: {p.secondary_skills}, Skill: {p.skill_point})")

    while True:
        selected_indices = input("\nEnter the numbers of the players you want to select for this round (comma separated): ")
        try:
            indices = [int(i.strip()) - 1 for i in selected_indices.split(',')]
            selected = [registered_players[i] for i in indices if 0 <= i < len(registered_players)]
            if not selected:
                raise ValueError("No valid indices provided.")
            return selected
        except (ValueError, IndexError):
            print("\n❌ Invalid input. Please enter valid player numbers separated by commas.")

# Example usage
if __name__ == "__main__":
    # Register players
    add_player("Jai", "defender", [], 4)
    add_player("JaiB", "attacker", [], 4)
    add_player("Yash", "attacker", [], 4.5)
    add_player("YashB", "defender", [], 3.5)
    add_player("Aditya", "attacker", [], 5)
    add_player("Lakshit", "attacker", [], 4)
    add_player("SP", "attacker", [], 3.5)
    add_player("Anshul", "attacker", [], 3)
    add_player("Devi", "attacker", [], 5)
    add_player("Sarthak", "defender", [], 3.5)
    add_player("Ansh", "defender", [], 3)
    add_player("Pratyaksh", "gk", [], 4)
    add_player("Aashu", "gk", [], 3)
    add_player("Satyam", "defender", [], 3.5)
    add_player("Dikshant", "defender", [], 3.5)

    # Choose players for the round interactively
    current_round_players = select_players_for_round()

    result = balance_teams(current_round_players)
    print("\n✅ Team A:", result['team_a'])
    print("✅ Team B:", result['team_b'])
    if result['extra_player']:
        print("🧍 Extra player (plays one half for each team):", result['extra_player'])
