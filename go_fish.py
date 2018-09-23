import random

class Card(object):
    suit_names = ["Diamonds", "Clubs", "Hearts", "Spades"]
    rank_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    faces = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

    def __init__(self, suit=0, rank=2):
        self.suit = self.suit_names[suit]
        if rank in self.faces:  # self.rank handles printed representation
            self.rank = self.faces[rank]
        else:
            self.rank = rank
        self.rank_num = rank  # To handle winning comparison

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck(object):
    def __init__(self):  # Don't need any input to create a deck of cards
        # This working depends on Card class existing above
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)  # appends in a sorted order

    def __str__(self):
        total = []
        for card in self.cards:
            total.append(card.__str__())
        # shows up in whatever order the cards are in
        return "\n".join(total)  # returns a multi-line string listing each card

    def pop_card(self, i=-1):
        # removes and returns a card from the Deck
        # default is the last card in the Deck
        return self.cards.pop(i)  # this card is no longer in the deck -- taken off

    def shuffle(self):
        random.shuffle(self.cards)

    def replace_card(self, card):
        card_strs = []  # forming an empty list
        for c in self.cards:  # each card in self.cards (the initial list)
            card_strs.append(c.__str__())  # appends the string that represents that card to the empty list
        if card.__str__() not in card_strs:  # if the string representing this card is not in the list already
            self.cards.append(card)  # append it to the list

    def sort_cards(self):
        # Basically, remake the deck in a sorted way
        # This is assuming you cannot have more than the normal 52 cars in a deck
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    # Add a function “deal” to Deck that takes two parameters representing the number of hands and the number
    # of cards per hand and returns a list of Hands. If the number of cards per hand is set to -1, all of the
    # cards should be dealt, even if this results in an uneven number of cards per hand. Write tests to verify
    # that this works.
    def deal(self, num_hand, card_per_hand):

        round = 0
        hands = []

        for i in range(0, num_hand):
            hands.append(Hand([]))

        while (card_per_hand == -1 or round < card_per_hand) and len(self.cards):
            for i in range(0, num_hand):
                if len(self.cards):
                    card = self.pop_card()
                    hands[i].add_card(card)
            round += 1

        return hands


class Hand:
    # create the Hand with an initial set of cards
    # param: a list of cards -- init_cards
    def __init__(self, init_cards):
        self.cards = init_cards.copy()

    def __str__(self):
        total = []
        for card in self.cards:
            total.append(card.__str__())
        # shows up in whatever order the cards are in
        return ", ".join(total)  # returns a multi-line string listing each card

    # add a card to the hand
    # silently fails if the card is already in the hand
    # param: the card to add
    # returns: nothing
    def add_card(self, card):
        card_strs = []
        for c in self.cards:
            card_strs.append(c.__str__())
        if card.__str__() not in card_strs:
            self.cards.append(card)

    # remove a card from the hand
    # param: the card to remove
    # returns: the card, or None if the card was not in the Hand
    def remove_card(self, card):
        card_str = card.__str__()
        for existing_card in self.cards:
            if existing_card.__str__() == card_str:
                self.cards.remove(existing_card)
                return existing_card
        return None

    # draw a card from a deck and add it to the hand
    # side effect: the deck will be depleted by one card
    # param: the deck from which to draw
    # returns: the card drawed
    def draw(self, deck):
        drawed_card = deck.pop_card()
        self.cards.append(drawed_card)
        return drawed_card

    # Add a function “remove_pairs” to Hand that looks for pairs of cards in a hand and removes them.
    # Note that if there are three of a kind, only two should be removed (it doesn’t matter which two).
    # Write tests to verify that this works.
    def remove_pairs(self):

        rank_dic = {}
        cards_to_remove = []

        for card in self.cards:
            rank = card.rank
            if rank in rank_dic.keys():
                cards_to_remove.append(card)
                cards_to_remove.append(rank_dic.pop(rank))
            else:
                rank_dic[rank] = card

        for card in cards_to_remove:
            self.cards.remove(card)


def play_go_fish_human():
    play_go_fish(2)

def play_go_fish(player_count):
    deck = Deck()
    deck.shuffle()

    initial_card_per_player = 5
    if player_count <= 4:
        initial_card_per_player = 7

    hands = deck.deal(player_count, initial_card_per_player)
    faces = []

    for i in range(player_count):
        faces.append([])

    current_player_index = 0

    should_continue = True
    steps = 0

    while should_continue:
        steps += 1
        if steps > 1000:
            print("It's a draw, too many rounds already.")
            break


        print("")
        for index in range(player_count):
            print("Player " + str(index + 1) + ": " + str(hands[index]))

        next_player_index = (current_player_index + 1) % player_count
        current_player_name = "Player " + str(current_player_index + 1)
        next_player_name = "Player " + str(next_player_index + 1)
        current_player = hands[current_player_index]
        next_player = hands[next_player_index]

        if len(current_player.cards) == 0:
            if len(deck.cards) > 0:
                current_player.draw(deck)
            else:
                print(current_player_name + ": Skip, since I have no cards in my hand")
                current_player_index = next_player_index
                continue
        
        asked_rank = 0

            
        prompt = current_player_name + ": Please choose a card rank you would like to ask the other player if they have (between 1-13):"
        asked_rank = ask_for_rank(prompt, current_player)
        

        print(current_player_name + ": I want " + str(asked_rank))
        next_player_cards = next_player.cards.copy()
        should_go_fish = True
        for card in next_player_cards:
            if card.rank == asked_rank:
                should_go_fish = False
                next_player.remove_card(card)
                current_player.add_card(card)
                print(next_player_name + ": Give you " + str(card))
                dict = {}
                current_player_cards = current_player.cards.copy()
                for card in current_player_cards:
                    if card.rank in dict:
                        dict[card.rank] += 1
                    else:
                        dict[card.rank] = 1

                new_faces = []
                for face, count in dict.items():
                    if count == 4:
                        new_faces.append(face)

                for card in current_player_cards:
                    if card.rank in new_faces:
                        current_player.remove_card(card)

                for face in new_faces:
                    faces[current_player_index].append(face)
        
        deck_has_card = len(deck.cards) != 0
        if should_go_fish and deck_has_card:
            print(next_player_name + ": Go fish.")
            drawed_card = current_player.draw(deck)
            if drawed_card.rank != asked_rank:
                dict = {}
                current_player_cards = current_player.cards.copy()
                for card in current_player_cards:
                    if card.rank in dict:
                        dict[card.rank] += 1
                    else:
                        dict[card.rank] = 1

                new_faces = []
                for face, count in dict.items():
                    if count == 4:
                        new_faces.append(face)

                for card in current_player_cards:
                    if card.rank in new_faces:
                        current_player.remove_card(card)

                for face in new_faces:
                    faces[current_player_index].append(face)
                current_player_index = next_player_index
            else:
                print(current_player_name + ": I got another turn since I drawed " + str(drawed_card))

                dict = {}
                current_player_cards = current_player.cards.copy()
                for card in current_player_cards:
                    if card.rank in dict:
                        dict[card.rank] += 1
                    else:
                        dict[card.rank] = 1

                new_faces = []
                for face, count in dict.items():
                    if count == 4:
                        new_faces.append(face)

                for card in current_player_cards:
                    if card.rank in new_faces:
                        current_player.remove_card(card)

                for face in new_faces:
                    faces[current_player_index].append(face)
        else:
            if not deck_has_card:                
                print("No more card in the deck")
            current_player_index = next_player_index

        should_continue = False

        for index in range(player_count):
            print("Player " + str(index + 1) + ": " + str(hands[index]))
            print("Player " + str(index + 1) + ": " + str(faces[index]))
            if len(hands[index].cards) > 0:
                should_continue = True
            else:
                print("Game ends")
                should_continue = False

    
    winner_index = 0
    for index in range(player_count):
        if len(faces[index]) > len(faces[winner_index]):
            winner_index = index
    print(str(winner_index + 1) + " wins the game!")


# Use this for Extra Credit 1
def ask_for_rank(prompt, hands):
    # repeat until the asked rank is valid
    while True:
        user_input = input(prompt)
        if user_input != "":
            asked_rank = Card(0, int(user_input)).rank
            
            # verify that the rank is valid
            is_asked_valid = False
            for card in hands.cards:
                if card.rank == asked_rank:
                    is_asked_valid = True
                    break

            if is_asked_valid:
                return asked_rank
            else: 
                print("You must have at least one card of the rank you requested.")
        else:
            print("Invalid input! Please input a rank.")
        
        
play_go_fish_human()