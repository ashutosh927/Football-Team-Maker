from typing import List, Dict
from collections import defaultdict

# Player class to store player details
class Player:
    def __init__(self, name: str, primary_skill: str, secondary_skills: List[str], skill_point: float):
        self.name = name
        self.primary_skill = primary_skill
        self.secondary_skills = secondary_skills
        self.skill_point = skill_point

    def __repr__(self):
        return f"{self.name} ({self.primary_skill}, {self.skill_point})"

# Function to balance players into two football teams

def balance_teams(players: List[Player]) -> Dict[str, List[Player]]:
    roles = ['gk', 'defender', 'striker']  # Essential roles required in each team
    team_a = []
    team_b = []

    # Step 1: Sort players by skill point in descending order to distribute strongest players first
    sorted_players = sorted(players, key=lambda p: p.skill_point, reverse=True)

    # Step 2: Distribute players alternately to ensure equal number of players in both teams
    for i, player in enumerate(sorted_players):
        if len(team_a) <= len(team_b):
            team_a.append(player)
        else:
            team_b.append(player)

    # Step 3: Ensure each team has at least one player per role (gk, defender, striker)
    def ensure_roles(team: List[Player], fallback_team: List[Player]):
        team_roles = {role: None for role in roles}  # Track if each role is filled

        # Try assigning based on primary skills first
        for player in team:
            if player.primary_skill in roles and not team_roles[player.primary_skill]:
                team_roles[player.primary_skill] = player

        # If a role is still missing, check for players with that role in secondary skills
        for role in roles:
            if not team_roles[role]:
                for player in team:
                    if role in player.secondary_skills:
                        team_roles[role] = player
                        break

        # If still missing, try to take a player from fallback team who fits the role
        for role in roles:
            if not team_roles[role]:
                for player in fallback_team:
                    if player.primary_skill == role or role in player.secondary_skills:
                        team.append(player)
                        fallback_team.remove(player)
                        break

    # Ensure both teams are role-balanced
    ensure_roles(team_a, team_b)
    ensure_roles(team_b, team_a)

    # Step 4: Handle case of odd number of players
    extra_player = None
    if len(players) % 2 != 0:
        # Remove one player from the team that has more to balance
        if len(team_a) > len(team_b):
            extra_player = team_a.pop()
        elif len(team_b) > len(team_a):
            extra_player = team_b.pop()

    return {
        'team_a': team_a,
        'team_b': team_b,
        'extra_player': extra_player  # This player plays half for each team
    }

# List to store all registered players
to_register_players = []

# Add players to the list of registered players
def add_player(name: str, primary: str, secondary: List[str], skill_point: float):
    to_register_players.append(Player(name, primary, secondary, skill_point))

# Function for selecting which players are playing this round
def select_players_for_round() -> List[Player]:
    print("\nRegistered players:")
    for idx, p in enumerate(to_register_players):
        print(f"{idx + 1}. {p.name} (Primary: {p.primary_skill}, Secondary: {p.secondary_skills}, Skill: {p.skill_point})")

    # Ask user for which players to select
    while True:
        selected_indices = input("\nEnter the numbers of the players you want to select for this round (comma separated): ")
        try:
            indices = [int(i.strip()) - 1 for i in selected_indices.split(',')]  # Convert to 0-based index
            selected = [to_register_players[i] for i in indices if 0 <= i < len(to_register_players)]
            if not selected:
                raise ValueError("No valid indices provided.")
            return selected
        except (ValueError, IndexError):
            print("\n❌ Invalid input. Please enter valid player numbers separated by commas.")

# Main execution block
if __name__ == "__main__":
    # Register players manually here
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

    # Allow user to choose players from the list
    current_round_players = select_players_for_round()

    # Divide selected players into balanced teams
    result = balance_teams(current_round_players)

    # Output teams
    print("\n✅ Team A:")
    for player in result['team_a']:
        print(f"- {player.name} ({player.primary_skill})")

    print("\n✅ Team B:")
    for player in result['team_b']:
        print(f"- {player.name} ({player.primary_skill})")

    if result['extra_player']:
        print("\n🧝 Extra player (plays one half for each team):", f"{result['extra_player'].name} ({result['extra_player'].primary_skill})")
