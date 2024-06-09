# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 02:33:02 2024

@author: alexh
"""
from random import shuffle, choice
from time import sleep
from collections import Counter


def string2list(string):
    lines = string.split('\n')
    nested_list = [line.split('\t') for line in lines]
    # print(nested_list)
    nested_nested_list = [[grid.split(', ') for grid in line] for line in nested_list] # dealing with "ʙ, ⱱ̟" and "ɾ, r"
    return [list(filter(None, line)) for line in nested_nested_list]

def flatten(nested_list): # and remove all empty str at the same time
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    flat_list_cleaned = [i for i in flat_list if i != ""]
    return flat_list_cleaned

def drawFromDeck(curPlayer):
    playersCards[curPlayer].append(cardDeck.pop(0))

def hasSameRowCol(curPlayer, topCardInfo):
    # topCardInfo = consInfo[topCard]
    # playerCardInfo = []
    hasSameRowCol = False
    for card in playersCards[curPlayer]:
        if card in consInfo.keys():
            # playerCardInfo.append(consInfo[card])
            if (consInfo[card][0] == topCardInfo[0]) or (consInfo[card][1] == topCardInfo[1]):
                # return True
                hasSameRowCol = True   
                break
    return hasSameRowCol

def playRegularCombo(curPlayer, topCardInfo):
    # topCardInfo = consInfo[topCard]
    playerCardInfo = []
    for card in playersCards[curPlayer]:
        if card in consInfo.keys():
            if (consInfo[card][0] == topCardInfo[0]) or (consInfo[card][1] == topCardInfo[1]):
                playerCardInfo.append(card)
    toPlay = choice(playerCardInfo)
    return toPlay

def hasSpecialVowel(curPlayer):
    for card in playersCards[curPlayer]:
        if card in specialList or card in vowelList:
            return True
    return False

def chooseSpecialVowel(curPlayer): # Select a card that is special or vowel (but won't be played, just to select special or vowel)
    playerCardInfo = []
    for card in playersCards[curPlayer]:
        if card in specialList or card in vowelList:
            playerCardInfo.append(card)
    toPlay = choice(playerCardInfo)
    return toPlay

def findMaxCategory(curPlayer): # Find the player has more same place or more same manner, select that one
    place_counter = Counter()
    manner_counter = Counter()
    for item in playersCards[curPlayer]:
        if item in consInfo:
            place, manner = consInfo[item]
            place_counter[place] += 1
            manner_counter[manner] += 1
    print(f"Player {curPlayer}: Place of articulation counts: {place_counter}")
    print(f"Player {curPlayer}: Manner of articulation counts: {manner_counter}")
    max_place = max(place_counter.values(), default=0)
    max_place_key = max(place_counter, key=place_counter.get, default=None)
    max_manner = max(manner_counter.values(), default=0)
    max_manner_key = max(manner_counter, key=manner_counter.get, default=None)
    # Compare and select based on the larger count
    if max_place > max_manner:
        relevant_list = specialList[0:7] + specialList[14:]
        isManner = False # is place: 0, is manner: 1
        key = max_place_key
        print('place is larger')
    else:
        relevant_list = specialList[7:14] + specialList[14:]
        isManner = True
        key = max_manner_key
        print('manner is larger')
    
    final_filtered_list = [item for item in playersCards[curPlayer] if item in relevant_list]
    print(final_filtered_list)
    if len(final_filtered_list) != 0: 
        toPlay = choice(final_filtered_list)
    else: 
        final_filtered_list = [item for item in playersCards[curPlayer] if item in specialList]
        toPlay = choice(final_filtered_list)
        isManner = toPlay in specialList[7:14]
        if isManner == 0: # is place
            key = max_place_key
        else:
            key = max_manner_key
    # return toPlay, isManner, key, specialList.index(toPlay)
    return toPlay, isManner, key

regularComboTable_string = """m̥	m	ɱ̊	ɱ			n̥	n			ɳ̊	ɳ			ɲ̊	ɲ	ŋ̊	ŋ	ɴ̥	ɴ				
p	b	p̪	b̪			t	d			ʈ	ɖ			c	ɟ	k	ɡ	q	ɢ	ʡ		ʔ	
pɸ	bβ	p̪f	b̪v			ts	dz	t̠ʃ	d̠ʒ	tʂ	dʐ	tɕ	dʑ	cç	ɟʝ	kx	ɡɣ	qχ	ɢʁ				
ɸ	β	f	v	θ	ð	s	z	ʃ	ʒ	ʂ	ʐ	ɕ	ʑ	ç	ʝ	x	ɣ	χ	ʁ	ħ	ʕ	h	ɦ
ʙ̥	ʙ, ⱱ̟		ⱱ			r̥	ɾ, r				ɽ							ʀ̥	ʀ	ʜ	ʢ		
ʘ		ɓ			ǀ		ǃ	ɗ				ᶑ	ǁ		ǂ	ʄ		ɠ		ʛ				
""" + """pʼ						tʼ				ʈʼ				cʼ		kʼ		qʼ		ʡʼ			
		p̪fʼ				tsʼ		t̠ʃʼ		tʂʼ		tɕʼ				kxʼ		qχʼ					
ɸʼ		fʼ		θʼ		sʼ		ʃʼ		ʂʼ		ɕʼ				xʼ		χʼ					""" 

specialTable_string = """			ʋ				ɹ				ɻ				j		ɰ						
						ɬʼ	ɺ																
						ɬ	ɮ			ꞎ													
							l				ɭ				ʎ		ʟ						
															ɥ		w						
"""
vowelTable_string = """a	e	i	o	u	ɛ	ɔ	ə	y	ɨ	ɯ	ʌ
ø	ɵ	œ	ɶ								
ʉ	ɜ	ɤ	ɞ								
æ	ɐ	ɑ	ɒ								
ɘ	ɪ	ʏ	ʊ								"""

cardTable_string = regularComboTable_string + "\n" + specialTable_string + vowelTable_string



regularComboTable = string2list(regularComboTable_string)
specialList = flatten(string2list(specialTable_string))
vowelList = flatten(string2list(vowelTable_string))
cardTable = string2list(cardTable_string)

# create a dictionary so that we can look up a consonant's info (place and manner)
consInfo = dict()
for i, manner in enumerate(regularComboTable):
    for j, grid in enumerate(manner):
        for ipa in grid:
            consInfo[ipa] = (i, j)


playersNum = 4 # number of players

playersCards = [[] for _ in range(playersNum)] # create empty lists for all players that contains the cards they currently have

cardDeck = flatten(cardTable) # card deck placed in the middle
shuffle(cardDeck)
print(f"The card deck has been shuffled, distributing the cards to the players... ({13-playersNum} cards initally for each player)")
for i in range(playersNum):
    for j in range(13-playersNum):
        playersCards[i].append(cardDeck.pop(0))

# STRATEGY:
    # if player have eligible cards from Regular/Combo -> play the card -> can play with a combo?
    # elif vowels/special random
    # else draw from card deck


print(f"First 5 cards from the deck: {cardDeck[:5]}")
# Draw the first card out of the deck
topCard = cardDeck.pop(0)
while topCard not in consInfo.keys():
    topCard = cardDeck.pop(0)
topCardInfo = consInfo[topCard]
print(f"First card: {topCard}. Game start.")

# curPlayer = 0
cntRound = 0
drawCards = 0
direction = 1
hasToSkip = False
sayVowel = (0, "")
while all(len(player) != 0 for player in playersCards): # until anyone has 0 cards
    cntRound += 1 # count how many rounds; a round is when everyone has played once
    
    for curPlayer in range(playersNum): # iterate every person
        if not hasToSkip:
            cntDraws = 0
            for __ in range(2):
                for _ in range(drawCards): playersCards[curPlayer].append(cardDeck.pop(0)) # cards that this player has to draw from the prev player
                if drawCards: print(f"player {curPlayer} has drawn {drawCards} cards!")
                print(f"Top card: {topCard}; info: {topCardInfo}")
                drawCards = 0 # reset
                
                if hasSameRowCol(curPlayer, topCardInfo): # if player have eligible cards from Regular/Combo 
                    toPlay = playRegularCombo(curPlayer, topCardInfo)
                    playersCards[curPlayer].remove(toPlay)
                    if sayVowel[1] != "":
                        if sayVowel[0] != curPlayer: print(f"player {curPlayer} has said /{toPlay}{sayVowel[1]}/")
                        else: sayVowel = (curPlayer, "")
                    print(f"player {curPlayer} has played {toPlay}; info: {consInfo[toPlay]}; cur. # of cards: {len(playersCards[curPlayer])}")
                    topCard = toPlay
                    topCardInfo = consInfo[topCard]
                    break
                    
                elif hasSpecialVowel(curPlayer):
                    toPlay = chooseSpecialVowel(curPlayer)
                    if toPlay in specialList: # if it is special, not vowel
                        toPlay, isManner, key = findMaxCategory(curPlayer)
                        playersCards[curPlayer].remove(toPlay)
                        if sayVowel[1] != "":
                            if sayVowel[0] != curPlayer: print(f"player {curPlayer} has said /{toPlay}{sayVowel[1]}/")
                            else: sayVowel = (curPlayer, "")
                        print(f"player {curPlayer} has played special {toPlay}; cur. # of cards: {len(playersCards[curPlayer])}")
                        if not isManner: 
                            topCardInfo = (key, topCardInfo[1])
                            print(f"player {curPlayer} has change place to {key}; now: {topCardInfo}")
                        else: 
                            topCardInfo = (topCardInfo[0], key)
                            print(f"player {curPlayer} has change manner to {key}; now: {topCardInfo}")
                        # specialList[0:7]: place of articulation
                        # specialList[7:14]: manner of articulation
                        # specialList[14:]: either
                    else: # is vowel
                        playersCards[curPlayer].remove(toPlay)
                        sayVowel = (curPlayer, toPlay) # from whom, say what vowel
                        print(f"player {curPlayer} has played vowel {toPlay}; cur. # of cards: {len(playersCards[curPlayer])}")
                        if toPlay in vowelList[12:16]: # skip next player
                            print(f"player {curPlayer} has played skipped; now player {(curPlayer + 1 * direction) % playersNum} is skipped")
                            hasToSkip = True 
                        elif toPlay in vowelList[12:16]: # reverse
                            direction *= -1
                            print(f"player {curPlayer} has played reverse")
                        elif toPlay in vowelList[12:16]: # +2
                            drawCards = 2
                            print(f"player {curPlayer} has played +2; now player {(curPlayer + 1 * direction) % playersNum} has to draw 2 cards")
                        elif toPlay in vowelList[12:16]: # +4
                            drawCards = 4
                            print(f"player {curPlayer} has played +4; now player {(curPlayer + 1 * direction) % playersNum} has to draw 4 cards")
                    # Add special function / Add vowel counts / Add vowel function
                    break
                
                    
                else: # draw from card deck
                    if cntDraws == 0:
                        playersCards[curPlayer].append(cardDeck.pop(0))
                        print(f"player {curPlayer} has drawn a card from the deck")
                        cntDraws += 1
                        # And repeat the previous step once
                        
                if len(playersCards[curPlayer]) == 1: print(f"player {curPlayer} has said '[ɪ̀.pʰá]'!")
        else: 
            print(f"player {curPlayer} is skipped")
            hasToSkip = False
        curPlayer = (curPlayer + 1 * direction) % playersNum
        sleep(3)
        
#drawFromDeck(curPlayer)

print("Game ends.")



# TO-DO:
    # if player have eligible cards from Regular -> can play with a combo?
    # # Add special function / Add vowel counts
    # And repeat the previous step once after drawing a card
    