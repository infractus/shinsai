"""Lists for Connect 4."""

def win_combos():
	"""This creates a list of winning combinations."""
	sets = []
	for x in range(0, 7):
		sets.append([f'{x}0', f'{x}1', f'{x}2', f'{x}3'])
		sets.append([f'{x}1', f'{x}2', f'{x}3', f'{x}4'])
		sets.append([f'{x}2', f'{x}3', f'{x}4', f'{x}5'])
	for y in range(0, 6):
		sets.append([f'0{y}', f'1{y}', f'2{y}', f'3{y}'])
		sets.append([f'1{y}', f'2{y}', f'3{y}', f'4{y}'])
		sets.append([f'2{y}', f'3{y}', f'4{y}', f'5{y}'])
		sets.append([f'3{y}', f'4{y}', f'5{y}', f'6{y}'])
	sets.append(['02', '13', '24', '35'])
	sets.append(['01', '12', '23', '34'])
	sets.append(['00', '11', '22', '33'])
	sets.append(['11', '22', '33', '44'])
	sets.append(['22', '33', '44', '55'])
	sets.append(['12', '23', '34', '45'])
	sets.append(['10', '21', '32', '43'])
	sets.append(['21', '32', '43', '54'])
	sets.append(['32', '43', '54', '65'])
	sets.append(['20', '31', '42', '53'])
	sets.append(['31', '42', '53', '64'])
	sets.append(['30', '41', '52', '63'])
	sets.append(['03', '12', '21', '30'])
	sets.append(['04', '13', '22', '31'])
	sets.append(['13', '22', '31', '40'])
	sets.append(['05', '14', '23', '32'])
	sets.append(['14', '23', '32', '41'])
	sets.append(['23', '32', '41', '50'])
	sets.append(['15', '24', '33', '42'])
	sets.append(['24', '33', '42', '51'])
	sets.append(['33', '42', '51', '60'])
	sets.append(['25', '34', '43', '52'])
	sets.append(['34', '43', '52', '61'])
	sets.append(['35', '44', '53', '62'])

	return sets

def column_lists():
	"""This creates a list of slots in each column."""
	columns = []
	
	for x in range(0,7):
		coord_list = []
		for y in range(0, 6):
			coord_list.append(f'{x}{y}')
		columns.append(coord_list)
	return columns



		
