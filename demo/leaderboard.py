import sys
import os

# Add parent directory to path to import easy_redis
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from easy_redis import EasyRedis


def main():
    print("--- Game Leaderboard Demo ---")
    print("Tracking high scores using Redis dictionaries\n")

    # Initialize EasyRedis and connect to "leaderboard_app" namespace
    redis = EasyRedis()
    app = redis.app("leaderboard_app")

    leaderboard_key = "high_scores"

    # Add initial scores
    print("1. Adding initial high scores:")
    scores = {"Alice": "1500", "Bob": "2300", "Charlie": "1800", "Diana": "2100"}

    app.save_dict(leaderboard_key, scores)
    print("   Scores added!\n")

    # Display leaderboard
    print("2. Current Leaderboard:")
    all_scores = app.load_dict(leaderboard_key)

    # Sort by score (descending)
    sorted_scores = sorted(all_scores.items(), key=lambda x: int(x[1]), reverse=True)

    for rank, (player, score) in enumerate(sorted_scores, 1):
        print(f"   #{rank} {player}: {score} points")

    # Add a new high score
    print("\n3. Charlie just beat his high score!")
    new_scores = app.load_dict(leaderboard_key)
    new_scores["Charlie"] = "2500"
    app.save_dict(leaderboard_key, new_scores)

    print("   Updated score saved!\n")

    # Display updated leaderboard
    print("4. Updated Leaderboard:")
    all_scores = app.load_dict(leaderboard_key)
    sorted_scores = sorted(all_scores.items(), key=lambda x: int(x[1]), reverse=True)

    for rank, (player, score) in enumerate(sorted_scores, 1):
        medal = (
            "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
        )
        print(f"   {medal} #{rank} {player}: {score} points")

    # Add new player
    print("\n5. New player 'Eve' joins with score 1900:")
    new_scores = app.load_dict(leaderboard_key)
    new_scores["Eve"] = "1900"
    app.save_dict(leaderboard_key, new_scores)

    # Final leaderboard
    print("\n6. Final Leaderboard:")
    all_scores = app.load_dict(leaderboard_key)
    sorted_scores = sorted(all_scores.items(), key=lambda x: int(x[1]), reverse=True)

    for rank, (player, score) in enumerate(sorted_scores, 1):
        medal = (
            "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
        )
        print(f"   {medal} #{rank} {player}: {score} points")

    # Cleanup
    print("\n7. Demo complete. Clearing leaderboard...")
    app.delete(leaderboard_key)


if __name__ == "__main__":
    main()
