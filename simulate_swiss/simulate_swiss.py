import random

N = 24  # 16  # 24  # nr teams
W = 5  # 4  # nr wins
R = 10000  # nr repetitions
P = 8  # nr teams required to go through playoffs


win_probs = "fixed_perc"  # TODO: one of "highest", "equal", "fixed_perc", "rankdiff"
fixed_perc = 0.9


class Team:
    # TODO: implement support for this being sortable on scoreline and then rank
    def __init__(self, rank):
        self.wins = 0
        self.losses = 0
        self.rank = rank
        self.opponents = set()

    def get_scoreline(self):
        return self.wins - self.losses


class ByeOpponent(Team):
    def __init__(self):
        super().__init__(rank=100000000000000)


def get_rank(team):
    return team.rank


results = []
stats = []
decider_types = set()
for r in range(R):

    # Create teams and their current results (which are empty or 0-0 or whatev')
    teams = [Team(i+1) for i in range(N)]
    curr_round = 1
    stop = False
    last_n_through = 0
    n_through = 0
    active_teams = teams.copy()

    while not stop:

        teams_per_scoreline = [[x for x in active_teams if x.losses == j] for j in range(curr_round)]
        nr_teams_per_scoreline = [len(x) for x in teams_per_scoreline]
        matchups = []

        for i, teams_this_score in enumerate(teams_per_scoreline):
            teams_this_score = sorted(teams_this_score, key=get_rank)
            if len(teams_this_score) % 2 != 0:
                # If odd number of teams: add lowest rank team of next score that has not faced top rank of this score
                highest_this_score = teams_this_score[0]
                teams_next_score = sorted(teams_per_scoreline[i+1], key=get_rank)
                valid_teams_next_score = [x for x in teams_next_score if x not in highest_this_score.opponents]
                lowest_ranked_valid = valid_teams_next_score[-1] if len(valid_teams_next_score) > 0 \
                    else teams_next_score[-1] if len(teams_next_score) > 0 else ByeOpponent()
                teams_this_score.append(lowest_ranked_valid)
                teams_per_scoreline[i+1].remove(lowest_ranked_valid) \
                    if lowest_ranked_valid in teams_per_scoreline[i+1] else None

            while len(teams_this_score) > 0:
                highest = teams_this_score.pop(0)
                valid_teams = [x for x in teams_this_score if x in highest.opponents]
                if len(valid_teams) > 0:
                    opponent = valid_teams[-1]
                else:
                    opponent = teams_this_score[-1]
                teams_this_score.remove(opponent)
                matchups.append((highest, opponent))

        for matchup in matchups:
            if isinstance(matchup[1], ByeOpponent):
                matchup[0].wins += 1
            else:
                if win_probs == "highest":
                    matchup[0].wins += 1
                    matchup[1].losses += 1
                elif win_probs == 'equal':
                    if random.random() < 0.5:
                        matchup[0].wins += 1
                        matchup[1].losses += 1
                    else:
                        matchup[1].wins += 1
                        matchup[0].losses += 1
                elif win_probs == 'fixed_perc':
                    if random.random() < fixed_perc:
                        matchup[0].wins += 1
                        matchup[1].losses += 1
                    else:
                        matchup[1].wins += 1
                        matchup[0].losses += 1
                else:
                    raise NotImplementedError(f"Not yet implemented: {win_probs}")
                matchup[0].opponents.add(matchup[1])
                matchup[1].opponents.add(matchup[0])

        last_n_through = n_through
        n_through = sum(x.wins >= W for x in teams)
        n_new_through = n_through - last_n_through

        if n_through >= P:

            through = [x for x in teams if x not in active_teams and x.wins >= W]
            new_through = [x for x in active_teams if x.wins >= W]
            decider_size = P - last_n_through

            if n_new_through > decider_size:
                decider_types.add((n_new_through, decider_size))

                if win_probs == 'equal':
                    # Not really true, depends on decider bracket -- to do accurate, you have to simulate full decider bracket of each type that can exist
                    through.extend(random.sample(new_through, k=decider_size))
                elif win_probs == 'highest':
                    through.extend(sorted(new_through, key=get_rank)[:decider_size])
                elif win_probs == 'fixed_perc':
                    # Not really true, depends on decider bracket -- to do accurate, you have to simulate full decider bracket of each type that can exist
                    through.extend(sorted(new_through, key=get_rank)[:decider_size])
                else:
                    raise NotImplementedError(f"Not yet implemented: {win_probs}")
            else:
                through.extend(new_through)

            stop = True
            results.append([curr_round, n_through, n_new_through, decider_size])

            nr_top8 = sum([x.rank <= 8 for x in through])
            nr_top3 = sum([x.rank <= 3 for x in through])
            stats.append([nr_top8 == 8, nr_top8 >= 4, nr_top3 == 3])
        else:
            curr_round += 1
            active_teams = [x for x in teams if x.wins < W and x.losses < W]


print(f'Rounds needed min/max: {min([x[0] for x in results])}, {max([x[0] for x in results])}')
print(f'Number through min/max: {min([x[1] for x in results])}, {max([x[1] for x in results])}')
print(f'Last round number through min/max: {min([x[2] for x in results])}, {max([x[2] for x in results])}')
print(f'Decider size min/max: {min([x[3] for x in results])}, {max([x[3] for x in results])}')

print(f'How often is top 8 fully through to playoffs: {sum([x[0] for x in stats]) / R}')
print(f'How often is majority of top 8 through to playoffs: {sum([x[1] for x in stats]) / R}')
print(f'How often is top 3 fully through to playoffs: {sum([x[2] for x in stats]) / R}')

print(f'Types of decider brackets: {decider_types}')
1+1

