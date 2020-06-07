#Dice roller
import random
roll = True #this allows to loop to play again

while roll:

    def choose_sides(): #this allows player to choose which sided die to roll
        print('Hello!')
        while True:
            sides=(input('How many sides are the dice you would you like to roll?' ))
            if sides.isdigit(): break
            print('Choose a proper number of sides.')
        return sides

    def choose_dice_number():  #choose how many dice to roll
        while True:
            num_dice=input('How many of these dice would you like to roll?')
            if num_dice.isdigit(): break
            print('No, you must enter a whole number.')
        num_dice=int(num_dice)
        while num_dice <=0:
            print('Enter a valid number: ')
            num_dice=int(input())
        return num_dice

    sides=choose_sides()
    num_dice=choose_dice_number()
    subtotal=0
    for n in range(num_dice):
        result=random.randint(1, int(sides))
        result=int(result)
        print (result)
        subtotal=result+subtotal

    #choose a modifier
    while True:
        print('What is the modifier?')
        modifier=input()
        if modifier.lstrip('-').isdigit(): break # lstrip for neg number
        if modifier.lstrip('+').isdigit(): break
        print('No, you must enter a whole number.')
    modifier=int(modifier)
    resultmod=subtotal+modifier

    #creates plus_or_minus variable to properly display the modifier in the results
    if modifier >= 0:
        plus_or_minus='+'
    else:
        plus_or_minus='-'

    #show results
    modifier=str(abs(modifier)) #sets modifier string with an absolute value (no negative)
    result=str(result)
    resultmod=str(resultmod)
    num_dice=str(num_dice)
    sides=str(sides)
    subtotal=str(subtotal)
    #explain what user has rolled
    print('You rolled ' + num_dice + 'd' + sides + plus_or_minus + modifier +'.')
    print('You rolled ' + subtotal + ' with a ' + plus_or_minus + modifier + ' modifier resulting in a ' + resultmod + '.')

    while True:
        again=str(input('Do you want to play again? y/n? ')).lower()
        if again.startswith('n'):
            roll = False
            break
        elif again.startswith('y'):
            roll = True
            break
        else:
            print('Enter "y" or "n".')
