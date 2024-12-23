import random
import time
import sys

# increase recursion limit
sys.setrecursionlimit(10000)


class Match:
    def __init__(self, player_rating, opponent_rating, result):
        self.player_rating = player_rating
        self.opponent_rating = opponent_rating
        self.result = result


class Player:
    # Constructor
    def __init__(self, id, name, initial_rating, k_factor=32):
        self.id = id
        self.name = name
        self.initial_rating = initial_rating
        self.current_rating = initial_rating
        self.k_factor = k_factor
        self.matches = []

    # Method to add a match to the player's history
    def add_match(self, match):
        self.matches.append(match)


def generate_players(n, max_rating, min_rating):
    player_list = []

    for i in range(n):
        player_id = i + 1
        player_name = f"Player {player_id}"
        player_rating = random.randint(min_rating, max_rating)
        player_k_factor = random.randint(15, 40)

        player = Player(player_id, player_name, player_rating, player_k_factor)
        player_list.append(player)

    return player_list


def playmatch(player1, player2):
    # Get player Elo ratings
    p1_elo = player1.current_rating
    p2_elo = player2.current_rating

    # Calculate initial win probabilities using the Elo formula
    p1_win_prob = 1 / (1 + 10 ** ((p2_elo - p1_elo) / 400))
    p2_win_prob = 1 / (1 + 10 ** ((p1_elo - p2_elo) / 400))

    # Calculate Elo difference
    elo_difference = abs(p1_elo - p2_elo)

    # Calculate draw probability
    draw_prob = max(0, 0.333 - elo_difference / 1200)

    # Adjust win probabilities
    total_win_prob = p1_win_prob + p2_win_prob
    p1_win_prob = p1_win_prob * (1 - draw_prob) / total_win_prob
    p2_win_prob = p2_win_prob * (1 - draw_prob) / total_win_prob

    # Simulate match result
    result = random.choices(
        [1, 0, 0.5],  # 1 for Player 1 win, 0 for Player 2 win, 0.5 for draw
        [p1_win_prob, p2_win_prob, draw_prob],
    )[0]

    # # print table with player, elos, and initial win probabilities
    # print(f"match between {player1.name} and {player2.name}")
    # print(f"Player 1: {player1.name}, Elo: {p1_elo}, Win Probability: {p1_win_prob}")
    # print(f"Player 2: {player2.name}, Elo: {p2_elo}, Win Probability: {p2_win_prob}")
    # print(f"Result: {result}\n")

    return result


def scores(matches):
    score = 0
    for match in matches:
        score += match.result
    return score


def calculate_elo(player):
    matches = player.matches
    total_matches = len(matches)
    total_score = scores(matches)

    if total_matches == 0:
        raise ValueError("Player has no matches.")

    # Calculate expected score
    expected_score = sum(
        1 / (1 + 10 ** ((match.opponent_rating - player.current_rating) / 400))
        for match in matches
    )

    # Update the player's rating
    new_rating = player.current_rating + player.k_factor * (
        total_score - expected_score
    )

    print(
        f"Player: {player.name}, Total Score: {total_score}, Expected Score: {expected_score}, "
        f"Initial Rating: {player.current_rating}, New Rating: {new_rating}"
    )

    return round(new_rating)


def calculate_elo_recursive(player, index=0, total_score=0.0, expected_score=0.0):
    if index == len(player.matches):
        new_rating = player.current_rating + player.k_factor * (
            total_score - expected_score
        )
        return round(new_rating)

    match = player.matches[index]
    total_score += match.result
    expected_score += 1 / (
        1 + 10 ** ((match.opponent_rating - player.current_rating) / 400)
    )

    return calculate_elo_recursive(player, index + 1, total_score, expected_score)


# round robin
def round_robin(players):
    n = len(players)
    for i in range(n):
        for j in range(i + 1, n):
            player1 = players[i]
            player2 = players[j]
            result = playmatch(player1, player2)
            match1 = Match(player1.current_rating, player2.current_rating, result)
            match2 = Match(player2.current_rating, player1.current_rating, 1 - result)
            player1.add_match(match1)
            player2.add_match(match2)

    for player in players:
        print(
            f"{player.name}, Wins: {scores(player.matches)}, Losses: {len(player.matches) - scores(player.matches)}"
        )
        for match in player.matches:
            print(f"Opponent: {match.opponent_rating}, Result: {match.result}")
        player.current_rating = calculate_elo(player)
        # list matches and opponent ratings

    return players


def round_robin_recursive(players, i=0, j=1):
    n = len(players)
    if i >= n:
        return players
    if j >= n:
        return round_robin_recursive(players, i + 1, i + 2)

    player1 = players[i]
    player2 = players[j]
    result = playmatch(player1, player2)
    match1 = Match(player1.current_rating, player2.current_rating, result)
    match2 = Match(player2.current_rating, player1.current_rating, 1 - result)
    player1.add_match(match1)
    player2.add_match(match2)

    return round_robin_recursive(players, i, j + 1)


# Main function to run the simulation
def process(n):

    players = generate_players(n, 2000, 800)
    for player in players:
        print(f"{player.name}, Rating: {player.current_rating}")

    players = round_robin(players)

    for player in players:
        # print player, initial rating, and final rating
        print(
            f"{player.name}, Initial Rating: {player.initial_rating}, Final Rating: {player.current_rating}"
        )

    # find player that lost the most rating
    print("\nPlayer with the most rating loss:")
    player = max(players, key=lambda x: x.initial_rating - x.current_rating)
    print(
        f"{player.name}, Initial Rating: {player.initial_rating}, Final Rating: {player.current_rating}"
    )


def process_recursive(n):
    players = generate_players(n, 2000, 800)
    for player in players:
        print(f"{player.name}, Rating: {player.current_rating}")

    players = round_robin_recursive(players)

    for player in players:
        # print player, initial rating, and final rating
        print(
            f"{player.name}, Initial Rating: {player.initial_rating}, Final Rating: {player.current_rating}"
        )

    # find player that lost the most rating
    print("\nPlayer with the most rating loss:")
    player = max(players, key=lambda x: x.initial_rating - x.current_rating)
    print(
        f"{player.name}, Initial Rating: {player.initial_rating}, Final Rating: {player.current_rating}"
    )


def main():
    # inputs to test
    test = [8, 16, 32, 64, 128]
    iterative_times = []
    recursive_times = []

    # run the simulation for each test case 10 times and take average time of runs
    print("Iterative:")
    for n in test:
        t = 0
        count = 10
        for i in range(10):
            start = time.time()
            process(n)
            end = time.time()
            t += end - start
        print(f"Time for {n} players: {t / count}")
        iterative_times.append(t / count)

    print("\nRecursive:")
    for n in test:
        t = 0
        count = 10
        for i in range(10):
            start = time.time()
            process_recursive(n)
            end = time.time()
            t += end - start
        print(f"Time for {n} players: {t / count}")
        recursive_times.append(t / count)

    print("Comparison:")
    for i in range(len(test)):
        # print rounded to 4 decimal places
        print(
            f"{test[i]} players: {round(iterative_times[i] / recursive_times[i], 4)} times faster. Iterative: {round(iterative_times[i], 4)}, Recursive: {round(recursive_times[i], 4)}"
        )


main()
