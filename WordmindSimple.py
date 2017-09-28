import random

again = "Y"
words = ["vaker"]
while again == "Y":                                             # "brommer","fiets","comuter","schade","water","python"] # list of possible words to find
    secretword = list(words[random.randint(0,len(words)-1)])    # randomly selecting one of the possible words and turning it into an array
    wordlen = len(secretword)                                   # lenght of the secret word
    correct = False                                             # user hasn't guessed it right yet
    current = []                                                # for later use
    for i in range(wordlen):
        current.append("-")                                     # adding a dash for each letter of the secret word

    while correct == False:
        print("The secret word: " + "".join(current))
        for i in range(len(current)):
            if current[i] == "?":
                current[i] = "-"
        guess = list(input("Guess the word: ").lower())         # turning the guess the user made into an array

        for i in range(wordlen):
            if (guess[i] == secretword[i]):
                current[i] = guess[i]                           # if a letter is in the right place make it visible in the next round
                if (guess == secretword):
                    correct = True                              # the guess was right
                    break
            elif (guess[i] in secretword and current[i]=="-" and (current[secretword.index(guess[i])] == "-" or current[secretword.index(guess[i])]=="?")):
                current[i] = "?"                                # the letter is in the word, but not in the right place, therefor placing a question mark at its position
        print("\n")                                             # for nicer looks

    print("Word \"" + "".join(secretword) + "\" found!")        # Telling the user their guess was correct
    again = input("Another game? (Y/N)").upper()                # if the user responds with "Y" then the game starts over
    print("\n")                                                 # for nicer looks
