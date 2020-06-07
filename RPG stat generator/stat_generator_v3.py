# This is a learning program that generates statistic values for D&D
# based on the roll 4 drop 1 method.

import random, yes_no

def display_intro():
    '''Shows the intro text.'''
    print()
    print('''''Please provide priorities for the following ability scores: \n
    Strength - Melee and thrown weapons, athletics, durability, carry capacity, etc.
    Dexterity - Ranged/finesse weapons, acrobatics, stealth, initiative, etc.
    Constitution - Hit points, resistance to poisons, etc.
    Intelligence - Knowledge checks, investigation, etc.
    Wisdom - Insight, perception, etc.
    Charisma - Persuasion, deception, intimidation, etc.
    ''')


def pick_a_stat(placement,stats_left):
    '''Gather/display priorities.'''
    stat_loop = True
    while stat_loop:
        if len(placement) < 2:
            print('Please type at least 2 letters of the stat.')
            placement = input().lower().strip()
        else: stat_loop = False
    already_used = True
    while already_used:
        for i in stats_left:
            if placement[:2].lower().strip() in i[:2].lower() and \
            len(placement) >= 2:
                placement = i
        if placement not in stats_left:
            placement = input(
                f'Please enter one of the following: \n{", ".join(stats_left)}'
                '\n'
                )
        else: already_used = False
    return placement


def gather_stats():
    '''Prompt the user for the priority of their stats.'''
    while True:
        print(
            'Choose the priority of your stats.  Type at least 2 letters, i.e.'
            ' "st", "in", etc.')

        statsdict = {}
        statslist = ['Highest','Second','Third','Fourth','Fifth','Sixth']
        stats_left = [
            'Strength','Dexterity','Constitution','Intelligence','Wisdom',
            'Charisma'
            ]
        for s in statslist[:-1]:
            statsdict[s] = choose_priorities(s, stats_left)
        statsdict['Sixth'] = str(stats_left[0])
        print()

        print('You chose the ability scores with the following priorities:\n')
        for s in statslist:
            print (f'{s} = {statsdict[s]}')
        print()

        if yes_no.prompt_yn(
                'Is this correct? Defaults to "y". (y/n)', 'y'
                ).startswith('y'):
            break

    return [statsdict[x] for x in statslist]


def choose_priorities(priority, stats_left):
    '''
    Assign the input priority of the stat and remove it from the list.
    '''
    priority = input(
        f'\nWhat is your {priority} priority? Choose between the following:\
            \n{", ".join(stats_left)}\n'
        )
    priority = pick_a_stat(priority.strip(),stats_left)
    stats_left.remove(priority)
    return priority


def select_race():
    '''Prompts user to select a race and returns it.'''
    print('''
    1: Dragonborn: Str+2, Cha+1
    2: Hill Dwarf: Con+2, Wis+1
    3: High Elf: Dex+2, Int+1
    4: Rock Gnome: Int+2, Con+1
    5: Half-Elf: Cha+2, two others +1
    6: Half-Orc: Str+2, Con+1
    7: Lightfoot Halfling: Dex+2, Cha+1
    8: Human: Str+1, Dex+1, Con+1, Int+1, Wis+1, Cha+1
    9: Tiefling: Int+1, Cha+2
    ''')

    while True:
        racenum = input('Select your race: (1-9) ')
        if racenum.isdigit() and int(racenum) == 1:
            race = 'Dragonborn'
            bonuses = {'Strength' : 2, 'Charisma' : 1}
            break
        elif racenum.isdigit() and int(racenum) == 2:
            race = 'Hill Dwarf'
            bonuses = {'Constitution' : 2, 'Intelligence' : 1}
            break
        elif racenum.isdigit() and int(racenum) == 3:
            race = 'High Elf'
            bonuses = {'Dexterity' : 2, 'Intelligence' : 1}
            break
        elif racenum.isdigit() and int(racenum) == 4:
            race = 'Rock Gnome'
            bonuses = {'Intelligence' : 2, 'Constitution' : 1}
            break
        elif racenum.isdigit() and int(racenum) == 5:
            # If the user is a Half-Elf, prompt for which stats they
            # would like to increase.
            stats_choice = [
                'Strength','Dexterity','Constitution',
                'Intelligence','Wisdom'
                ]
            priority = input(f'Choose two stats to gain a +1 bonus. Choose '
                    'between the following:\n{", ".join(stats_choice)}\n')
            half_elf_stats = pick_a_stat(priority, stats_choice)
            stats_choice.remove(half_elf_stats)
            bonuses = {'Charisma' : 2}
            bonuses.update( {half_elf_stats : 1} )
            half_elf_stats = pick_a_stat(priority, stats_choice)
            bonuses.update( {half_elf_stats : 1} )
            race = 'Half-Elf'
            break
        elif racenum.isdigit() and int(racenum) == 6:
            race = 'Half-Orc'
            bonuses = {'Strength' : 2, 'Constitution' : 1}
            break
        elif racenum.isdigit() and int(racenum) == 7:
            race = 'Lightfoot Halfling'
            bonuses = {'Dexterity' : 2, 'Charisma' : 1}
            break
        elif racenum.isdigit() and int(racenum) == 8:
            race = 'Human'
            bonuses = {
                'Strength' : 1, 'Dexterity' : 1, 'Constitution' : 1,
                'Intelligence' : 1, 'Wisdom' : 1, 'Charisma' : 1
                }
            break
        elif racenum.isdigit() and int(racenum) == 9:
            race = 'Tiefling'
            bonuses = {'Intelligence' : 1, 'Charisma' : 2}
            break

    print()
    return race, bonuses


def results(race, bonuses, stats):
    '''Rolls the dice, then calculates and prints the results.'''
    results = [roll_dice(s) for s in (
                'first', 'second', 'third', 'fourth', 'fifth', 'sixth'
                )]
    print()
    print(f'Your results are: {results}')
    results.sort(reverse = True)
    print(f'Your results sorted highest to lowest are: {results}')
    print()
    print(f'Assigned stats (Taking into account the {race} bonuses):')
    print()
    stats_dict = {}
    for i,s in enumerate((stats)):
        stats_dict[s] = results[i]
    for s in bonuses:
        if s in stats_dict:
            stats_dict[s] = stats_dict[s] + bonuses[s]
        else:
            pass
    for s in (
            'Strength', 'Dexterity', 'Constitution',
            'Intelligence', 'Wisdom', 'Charisma'
            ):
        print(f'{s}:{stats_dict[s]}')


def roll_dice(ordinal):
    '''Roll dem bones.'''
    roll = [random.randint(1,6) for x in range(4)]
    print(f'Your {ordinal} roll is: {roll} which sorts to ', end = '')
    roll.sort(reverse = True)
    roll_result = sum(roll[:3])
    print(
        f'{roll}; dropping the lowest, this becomes {roll[:3]} adding up to '
        f'{roll_result}.')
    return roll_result


def main():
    '''Runs the program.'''
    main_loop = True
    while main_loop:
        # This loop is in place for the "play again?" functionality at
        # the bottom.
        display_intro()
        stats = gather_stats()
        race, bonuses = select_race()
        results(race, bonuses, stats)
        while True:
            if yes_no.prompt_yn(
                    '\nDo you want to roll again? Defaults to "y". (y/n) ', 'y'
                    ).startswith('n'):
                print()
                print('Thanks for playing!')
                main_loop = False
                break
            if yes_no.prompt_yn(
                '\nDo you want to keep the stat priorities you selected? '
                'Defaults to "y". (y/n) ', 'y').startswith('y'):
                if yes_no.prompt_yn(
                        f'\nDo you want to keep the race you\'ve selected'
                        f' ({race})? Defaults to "y". (y/n) ', 'y'
                        ).startswith('n'):
                    race, bonuses = select_race()
                results(race, bonuses, stats)
            else:
                break


main()
