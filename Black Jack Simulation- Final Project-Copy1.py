#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import multiprocessing
import math
import time
import matplotlib.pyplot as plt
import statistics
random.seed(1234)


# In[2]:


num_decks = 4

def total(hand):
    total=0   
    for i, card in enumerate(hand):
        if card != "A":
            total+= card
        if card=="A":
            if total>= 11: 
                total += 1
                hand[i] = 1
            else: 
                total+=11
                hand[i]=11
    
    return total
#Creation of one deck, with traditional 52 card deck. Face cards are added as "10" values.
def new_deck():
    
    std_deck = [
          # 2  3  4  5  6  7  8  9  10  J   Q   K   A
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A",
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A",
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A",
            2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, "A"]


        # add more decks
    std_deck = std_deck * num_decks

    random.shuffle(std_deck)

    return std_deck[:]


# In[3]:


#Implements standard blackjack rules logic for player's hand
def player_h(p_hand,cards,i,p_stand,soft):
    ncards = len(cards)
    stand = False
    while stand != True:
        #Total the current hand
        current = total(p_hand)
        
        #Stop if card index is equal to num of card in deck (when deck runs out)
        if i == ncards:
            stand = True
        if soft == "N":    
            if current < p_stand:
                i += 1
                p_hand.append(cards[i])
            else:
                stand = True
        elif soft =="Y":    
            #Checking for a soft hand, when Ace is counted as 11
            if "A" in p_hand and current == p_stand and current > 11:
                p_hand.append(cards[i])
            elif current < p_stand:
                i += 1
                p_hand.append(cards[i])
            else:
                stand = True
    x = [current,i]
    return x
    


# In[4]:



def dealer_h(d_hand,cards,i):
    ncards = len(cards)
    stand = False
    while (stand != True):
        current = total(d_hand)
        if i == ncards:
            stand = True
        elif current <= 16:
            i += 1
            d_hand.append(cards[i])
        
        else:
            stand = True
    x = [current,i]
    return x


# In[5]:



def play_bj(cards,bet,p_stand,soft):
    ncards = len(cards)
    i = -1
    cwinnings = 0
    mwinnings = 0
    won = 0
    lost = 0
    draw = 0
    bet = bet
    unit = bet/2
    global prev_result
    global maxm
    prev_result = 0
    maxm = 0
    while i < ncards-20:
        
        if prev_result == 0:
            cbet = bet
            mbet = bet
        elif prev_result == -1:
            mbet = 2*mbet
        elif prev_result ==1:
            cbet = cbet+unit
        #make sure at least 4 cards left in deck
        if i <= (ncards-8):
            ## Initial deals
            i += 2
            p_hand = [cards[i-1],cards[i]]
            i += 2
            d_hand = [cards[i-1],cards[i]]
            
        else: #when deck is near empty
            return [won,lost,draw,winnings]
        
        p_res = player_h(p_hand,cards,i,p_stand,soft)
        
        i = p_res[1]
        d_res = dealer_h(d_hand,cards,i)
        
        if mbet > maxm:
            maxm = mbet
        
        #if player didn't go over 21, then move on to dealer
        if p_res[0] < 22 :
            d_res = dealer_h(d_hand,cards,i)
            i = d_res[1]
        if p_res[0] == d_res[0]:
            draw += 1
            prev_result = 0
        elif p_res == [10,"A"] or p_res== ["A",10]: #If blackjack
            cwinnings += 3*(cbet/2)
            mwinnings += 3*(mbet/2)
            won += 1
            prev_result = 1
        elif p_res[0] > 21:
            cwinnings -= cbet
            mwinnings -= mbet
            lost +=1
            prev_result = -1
        elif d_res[0] > 21:
            cwinnings += cbet
            mwinnings += mbet
            won += 1
            prev_result = 1
        elif p_res[0] > d_res[0]:
            cwinnings += cbet
            mwinnings += mbet
            won += 1
            prev_result = 1
        elif p_res[0] < d_res[0]:
            cwinnings -= cbet
            mwinnings -= mbet
            lost +=1
            prev_result = -1
    return [won,lost,draw,cwinnings,mwinnings,maxm]
            
            


# In[6]:



def softplays():
    test = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    resy = [0]*len(test)
    for k,j in enumerate(test):
        p_stand = j
        wins = [0]*N
        losses = [0]*N
        draws = [0]*N
        cwinnings = [0]*N
        mwinnings = [0]*N
        results = [0]*N
        maxbet = [0]*N
        bet = 10
        for i in range(0,N):
            total_decks = new_deck()
            results[i] = play_bj(total_decks,bet,p_stand,"Y")
            wins[i] = results[i][0]
            losses[i] = results[i][1]
            draws[i] = results[i][2]
            cwinnings[i] = results[i][3]
            mwinnings[i] = results[i][4]
            maxbet[i] = results[i][5]
            total = sum(wins)+sum(losses)+sum(draws)
            
        resy[k] = [j,round(sum(wins)/total,5), round(sum(losses)/total,5), round(sum(draws)/total,5), 
                   round(sum(cwinnings)/len(cwinnings),2),round(sum(mwinnings)/len(mwinnings),2),round(sum(maxbet)/len(maxbet),2)]
    return resy
    


# In[7]:


N = 1000
softplays()


# In[8]:


N = 10000
softplays()


# In[9]:


N = 20000
softplays()


# In[11]:


def hardplays():
    
    test = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    resy = [0]*len(test)
    for k,j in enumerate(test):
        p_stand = j
        wins = [0]*N
        losses = [0]*N
        draws = [0]*N
        cwinnings = [0]*N
        mwinnings = [0]*N
        results = [0]*N
        maxbet = [0]*N
        bet = 10
        for i in range(0,N):
            total_decks = new_deck()
            results[i] = play_bj(total_decks,bet,p_stand,"N")
            wins[i] = results[i][0]
            losses[i] = results[i][1]
            draws[i] = results[i][2]
            cwinnings[i] = results[i][3]
            mwinnings[i] = results[i][4]
            maxbet[i] = results[i][5]
            total = sum(wins)+sum(losses)+sum(draws)
            
        resy[k] = [j,round(sum(wins)/total,5), round(sum(losses)/total,5), round(sum(draws)/total,5), 
                   round(sum(cwinnings)/len(cwinnings),2),round(sum(mwinnings)/len(mwinnings),2),round(sum(maxbet)/len(maxbet),2)]
    return resy


# In[12]:


N = 1000
hardplays()


# In[13]:


N = 10000
hardplays()


# In[14]:


N = 20000
hardplays()


# In[169]:


x = 10000
winnings = [0]*x
results= [0]*x

for i in range(0,x):
    results[i] = play_bj(new_deck(),10,16,"N")
    winnings[i] = results[i][3]


# In[170]:


plt.xlim([min(winnings)-5, max(winnings)+5])

plt.hist(winnings, density=True, bins=50)
plt.title('Winnings Distribution with Hard 16 Strategy and Conservative Betting')
plt.xlabel('Winnings/Profit')
plt.ylabel('Count')

plt.show()


# In[171]:


winnings2 = [0]*10000
results2= [0]*10000

for i in range(0,10000):
    total_decks = new_deck()
    results2[i] = play_bj(total_decks,10,16,"Y")
    winnings2[i] = results2[i][3]


# In[172]:


plt.xlim([min(winnings2)-5, max(winnings2)+5])

plt.hist(winnings2, density=True, bins=50)
plt.title('Winnings Distribution with Soft 16 Strategy and Conservative Betting')
plt.xlabel('Winnings/Profit')
plt.ylabel('Count')

plt.show()


# In[180]:


#Martingale profits at : mean, med, max, min, standard deviation, variance across different iterations
def softsixteen(iterations):
    
    resy = [0]*len(iterations)
    for k,j in enumerate(iterations):
        N = j
        
        p_stand = 16
        cwinnings = [0]*N
        mwinnings = [0]*N
        results = [0]*N
        bet = 10
        
        for i in range(0,N):
            total_decks = new_deck()
            results[i] = play_bj(total_decks,bet,p_stand,"N")
            cwinnings[i] = results[i][3]
            mwinnings[i] = results[i][4]
 
            
        #Create table of mean, med, max, min, standard deviation, variance of winnings
        resy[k] = [j,"c",round(sum(cwinnings)/len(cwinnings),2),
                    statistics.median(cwinnings),
                    max(cwinnings),min(cwinnings),
                    statistics.stdev(cwinnings),statistics.variance(cwinnings),"m",round(sum(mwinnings)/len(mwinnings),2),
                    statistics.median(mwinnings),
                    max(mwinnings),min(mwinnings),
                    statistics.stdev(mwinnings),statistics.variance(mwinnings)]
    return resy
        
        


# In[181]:


softsixteen([1000,10000,20000])


# In[182]:


softsixteen([1000,10000,20000])


# In[183]:


x = 50000
winnings3 = [0]*x
results3= [0]*x

for i in range(0,x):
    total_decks = new_deck()
    results3[i] = play_bj(total_decks,10,16,"N")
    winnings3[i] = results3[i][4]



# In[184]:


plt.hist(winnings3,range=[-16000000, 16000000])
plt.title('Winnings Distribution with Hard 16 Strategy and Conservative Betting')
plt.xlabel('Winnings/Profit')
plt.ylabel('Count')

plt.show()


# In[185]:


softsixteen([10000,50000,100000])


# In[186]:


softsixteen([10000,50000,100000])


# In[ ]:




