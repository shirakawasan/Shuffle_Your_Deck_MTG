import random
#from mtgsdk import Card
#import types
import scrython

class Card_Deck:
    def __init__(self):
        self.decklist_string = "null"
        self.decksize = 0
        self.decklist = []
        self.shuffledecklist = []
    
    def deck_import(self,decklist_string):
        self.decklist = []

        #decklist import
        self.decklist_string = decklist_string
        deck_card_order = decklist_string.split("\n")
        for card in deck_card_order:
            if card[1] == " ":
                for i in range(int(card[0])):
                    self.decklist.append(card[2:])
            else:
                for i in range(int(card[:2])):
                    self.decklist.append(card[3:])
        
        #shuffle decklist
        self.decksize = len(self.decklist)
        self.shuffledecklist = [i for i in range(self.decksize)]
        return None
    
    def make_display_string(self):
        output_string = ""
        for i in range(self.decksize):
            output_string += self.decklist[self.shuffledecklist[i]]
            if i != self.decksize-1:
                output_string += "\n"
        return output_string
    
    def reset(self):
        self.shuffledecklist = [i for i in range(self.decksize)]
        output_string = ""
        for i in range(self.decksize):
            output_string += self.decklist[self.shuffledecklist[i]]
            if i != self.decksize-1:
                output_string += "\n"
        return output_string
    
    # nonrandom deal shuffle   
    def shuffle_deal_nonrandom(self, cardnumber_list, num_pile):
        '''
        input
        cardnumber_list : int list whose length is the deck size
        num_pile : int

        chenge parameter
        shuffled_cardnumber_list : int list whose length is the deck size

        output
        msg, TF
        '''

        if num_pile > self.decksize:
            msg, flag = "The number of piles is larger than the deck size.", False
            return msg, flag
        
        # make the first pile
        shuffle_pilelist = [i for i in range(num_pile)]
        pile = [i for i in range(num_pile)]
        
        # Regurarly sort the cards into their respective piles.
        while len(shuffle_pilelist) < self.decksize:
            shuffle_pilelist.extend(pile)
        
        # Cutting off the portion that extends beyond the deck size with shuffle_pilelist
        shuffle_pilelist_cutted = shuffle_pilelist[:self.decksize]
        
        # Make the card number correspond to the pile number.
        shuffled_cardnumber_list = []
        for i in range(num_pile):
            indexes = [j for j, x in enumerate(shuffle_pilelist_cutted) if x == i]
            for k in indexes:
                shuffled_cardnumber_list.append(cardnumber_list[k])
        self.shuffledecklist = shuffled_cardnumber_list
        msg, flag = "Shuffle successed", True
        return msg, flag
    
    # random deal shuffle
    def shuffle_deal_random(self, cardnumber_list, num_pile):
        '''
        input
        cardnumber_list : int list whose length is the deck size
        num_pile : int
        
        chenge parameter
        shuffled_cardnumber_list : int list whose length is the deck size

        output
        msg, TF
        '''
        if num_pile > self.decksize:
            msg, flag = "The number of piles is larger than the deck size.", False
            return msg, flag
        
        # make the first pile
        shuffle_pilelist = [i for i in range(num_pile)]
        pile = [i for i in range(num_pile)]
        
        # Randomly sort the cards into their respective piles.
        while len(shuffle_pilelist) < self.decksize:
            divide_to_pile = random.sample(pile,len(pile))
            shuffle_pilelist.extend(divide_to_pile)
        
        # Cutting off the portion that extends beyond the deck size with shuffle_pilelist
        shuffle_pilelist_cutted = shuffle_pilelist[:self.decksize]
        
        # Make the card number correspond to the pile number.
        shuffled_cardnumber_list = []
        for i in range(num_pile):
            indexes = [j for j, x in enumerate(shuffle_pilelist_cutted) if x == i]
            for k in indexes:
                shuffled_cardnumber_list.append(cardnumber_list[k])

        self.shuffledecklist = shuffled_cardnumber_list
        msg, flag = "Shuffle successed", True
        return msg, flag
        
    # Hindu Shuffle
    def shuffle_Hindu(self, cardnumber_list, time):
        '''
        input
        cardnumber_list : int list whose length is the deck size
        time : the number of shuffle time

        chenge parameter
        shuffled_cardnumber_list : int list whose length is the deck size

        output
        msg, TF
        '''

        shuffled_cardnumber_list = cardnumber_list
        
        for i in range(time):
            # The number of cards in the bucket to be moved is 20%~60% of the number of cards in the deck.
            number_card_bucket = round(self.deck_size * (0.2 + 0.4 * random.random()))
            shuffled_cardnumber_list = shuffled_cardnumber_list[number_card_bucket:] + shuffled_cardnumber_list[:number_card_bucket]
        
        self.shuffledecklist = shuffled_cardnumber_list     
        msg,flag = "Shuffle successed", True
        return msg, True
    
    def make_initialhand_url(self, number_of_initialhand = 7):
        card_image_url_list = []
        for i in range(number_of_initialhand):
            card_name = self.decklist[self.shuffledecklist[i]]
            '''
            cards = Card.where(name=card_name).all()
            index = [j for j, x in enumerate(cards) if type(x.image_url) != types.NoneType]
            print(index)
            card_image_url_list.append(cards[index[0]].image_url)
            '''
            card = scrython.cards.Named(fuzzy=card_name)
            card_image_url_list.append(card.image_uris()['small'])
        return card_image_url_list