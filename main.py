from howlongtobeatpy import HowLongToBeat as hltb
from dataclasses import dataclass
import datetime
from backlog import BACKLOG


@dataclass
class Game:
    name: str
    main_story: float
    review_score: float
    score_per_hour: float

def main() -> None:
    games = []
    failed = []


    for i, name in enumerate(BACKLOG):
        results = hltb().search(name)
        if len(results) > 0:
            first = results[0]
            # print(f"{name}: {first.review_score / first.main_story}")
            print(f"loading... ({i+1}/{len(BACKLOG)})")
            if first.main_story == 0 or first.main_story == 0.0:
                game = Game(name, first.main_story, first.review_score, -1)
            else:
                game = Game(name, first.main_story, first.review_score, first.review_score / first.main_story)
                
        else:
            game = f"FAILED SEARCH FOR {name}!"
        games.append(game)


    valid_games = []
    for game in games:
        if isinstance(game, str):
            failed.append(game)
        else:
            valid_games.append(game)
    games = valid_games
    
    sorted_games_by_score_per_hour = sorted(games, key=lambda x: x.score_per_hour)
    sorted_games_by_score_itself   = sorted(games, key=lambda x: x.review_score)
    sorted_games_by_howlongtobeat  = sorted(games, key=lambda x: x.main_story)


    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"{time_string}-output-score_per_hour.txt"
    with open(filename, "w") as file:
        print(f"\nGAMES SORTED BY SCORE PER HOUR\n", file=file)
        for game in sorted_games_by_score_per_hour:
            print(f"{game.name}: {game.score_per_hour}", file=file)

    filename = f"{time_string}-output-score_itself.txt"
    with open(filename, "w") as file:
        print(f"\nGAMES SORTED BY REVIEW SCORE ITSELF\n", file=file)
        for game in sorted_games_by_score_itself:
            print(f"{game.name}: {game.review_score}", file=file)

    filename = f"{time_string}-output-how_long_to_beat.txt"
    with open(filename, "w") as file:
        print(f"\nGAMES SORTED BY HOW LONG TO BEAT\n", file=file)
        for game in sorted_games_by_howlongtobeat:
            print(f"{game.name}: {game.main_story}", file=file)

    filename = f"{time_string}-output-failed.txt"
    with open(filename, "w") as file:
        if len(failed) > 0:
            print("FAILED TO FIND:", file=file)
            for f in failed:
                print(f, file=file)

    # print(first.gameplay_main)

if __name__ == "__main__":
    main()
