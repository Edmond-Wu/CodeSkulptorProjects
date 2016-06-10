"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    score_table = []
    for die in hand:
        value = hand.count(die) * die
        score_table.append(value)
    if not score_table:
        return 0
    else:
        return max(score_table)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = []
    for side in range(num_die_sides):
        val = side + 1
        outcomes.append(val)
    all_seq = gen_all_sequences(outcomes, num_free_dice)
    total_score = 0.0
    for seq in all_seq:
        possible_hand = list(held_dice)
        for die in seq:
            possible_hand.append(die)
        value = score(tuple(possible_hand))
        total_score += value
    
    return total_score / len(all_seq)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    keeper_set = set([()])
    outcomes = [0, 1]
    masks = list(gen_all_sequences(outcomes, len(hand)))
        
    for outcome in masks:
        hold = []
        for idx in range(len(hand)):
            if outcome[idx] != 0:
                hold.append(hand[idx])
        keeper_set.add(tuple(hold))
        #print hold
    #print masks
    #print keeper_set
    return keeper_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    best_value = 0.0
    best_hold = ()
    for hold in all_holds:
        expected_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if expected_val > best_value:
            best_value = expected_val
            best_hold = hold
    return (best_value, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

