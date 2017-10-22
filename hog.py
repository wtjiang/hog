"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled (capped at 11 - NUM_ROLLS).
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    score = 0
    pigout = 0
    for x in range(num_rolls):
        roll = dice()
        if roll == 1:
            pigout += 1
        else:
            score += roll
    if pigout > 0:
        return min(pigout,11-num_rolls)
    return score

    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    return max(opponent_score%10, opponent_score//10) + 1
    # END PROBLEM 2


# Write your prime functions here!
def is_prime(n): #Checks if a number is prime
    if n < 2:
        return False
    else:
        for x in range(2,n):
            if n%x == 0:
                return False
        return True

def next_prime(n): #Returns the next prime number if a number is prime
    if is_prime(n):
        n += 1
        while not is_prime(n):
            n += 1
        return n

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    score = 0
    if num_rolls == 0: #Implements Free Bacon
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls,dice)
    if is_prime(score): #Implements Hogtimus Prime
          return next_prime(score)
    else:
          return score

    # END PROBLEM 2

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    total = score + opponent_score
    sevens = 0
    while sevens <= total:
        sevens += 7        
        if total % sevens == 0:
            return four_sided
    return six_sided
    # END PROBLEM 3

def is_swap(score0, score1):
    """Returns whether one of the scores is double the other.
    """
    # BEGIN PROBLEM 4
    return max(score0,score1) == 2*min(score0,score1)
    # END PROBLEM 4

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    while score0 < goal and score1 < goal:
        if player == 0:
            dicetype = select_dice(score0,score1)
            num_rolls0 = strategy0(score0, score1)
            score0 = score0 + take_turn(num_rolls0, score1, dicetype)
            player = other(player)
        elif player == 1:
            dicetype = select_dice(score1,score0)
            num_rolls1 = strategy1(score1, score0)
            score1 = score1 + take_turn(num_rolls1, score0, dicetype)
            player = other(player)
        if is_swap(score0,score1): #Implements Swine Swap
            temp = score0
            score0 = score1
            score1 = temp
    return score0, score1

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'

def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    for i in range(goal): #Nested for loop to check all possible input values
        for j in range(goal):
            check_strategy_roll(i, j, strategy(i, j))
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75

    >>> from hog import *
    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_roll_dice = make_averaged(roll_dice, 1000)
    >>> # Average of calling roll_dice 1000 times
    >>> # Enter a float (e.g. 1.0) instead of an integer
    >>> averaged_roll_dice(2, dice)
    = 6.0
    """
    # BEGIN PROBLEM 7
    def make_avg(*args):
        total = 0
        for x in range(num_samples):
            total += fn(*args)
        return total/num_samples
    return make_avg
    # END PROBLEM 7

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    maxscore = 0
    average = 0
    for numdice in range(1,11):
        avg = make_averaged(roll_dice,num_samples)(numdice, dice) 
        if avg > average:
            average = avg
            maxscore = numdice
    return maxscore


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(10)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: 
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    baconscore = take_turn(0, opponent_score, dice=six_sided)
    if baconscore >= margin and baconscore + score != 2*opponent_score:
        return 0
    return num_rolls
    # END PROBLEM 9
check_strategy(bacon_strategy)

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    baconscore = take_turn(0, opponent_score, dice=six_sided) 
    total = baconscore + opponent_score
    if is_swap(score, total) and score!=2*opponent_score and baconscore >= margin:
        return 0
    return bacon_strategy(score, opponent_score, margin, num_rolls)

    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    Check "#" comments for a breakdown of each conditional statement.

    """
    # BEGIN PROBLEM 11
    if select_dice(score, opponent_score) == six_sided: #Set margins if dice is six sided 
        margin, num_rolls = 11, 6
    else: #Set margins if dice is four sided
        margin, num_rolls = 5,4
    baconscore = take_turn(0, opponent_score, dice=six_sided) #Score from free bacon
    total = baconscore + score #Total score

    if select_dice(total, opponent_score) == four_sided and baconscore >=6 and total!=2*opponent_score: #Force opponent to use four-sided dice 
        return 0
    elif opponent_score == score + 40: #Roll more dice if behind in score
        return swap_strategy(score, opponent_score, margin+7, num_rolls+3)
    elif score == opponent_score + 40: #Roll less dice if ahead in score
        return swap_strategy(score, opponent_score, margin-5, num_rolls-2)
    elif total == 2*opponent_score: #Prevent disadvantageous pigout swap
        return 5
    elif total >= GOAL_SCORE and not is_swap(total, opponent_score): #Roll 0 dice if can win by free bacon
        return 0
    elif score + 1 == 2 * opponent_score: #Roll 10 dice if 1 away from beneficial pigout swap
        return 10
    return swap_strategy(score, opponent_score, margin, num_rolls) #Use swap strategy
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()