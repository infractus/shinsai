def prompt_yn(prompt, default): 
    '''This prompts the user for a yes/no response based on the input'''
    while True:
        yesno=str(input(prompt)).lower().strip()
        if len(yesno) == 0:
            yesno = default
            break
        if yesno[0] in 'yn:':
            break
        print('Enter "y" or "n".')
    return yesno