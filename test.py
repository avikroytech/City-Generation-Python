from road_generator import TYPES, Cell
from termcolor import cprint
from random import randint

BUILDING_TYPES = {
	"NONE": 0,
	"BUILDING": 5
}

explored = []

class Building:
	def __init__(self):
		self.id = -1
		self.width = 0
		self.length = 0
		self.rotations = []

	def build(self, width, length):
		rotation = []
		for i in range(length):
			row = []
			for j in range(width):
				cell = Cell(i, j)
				cell.type = BUILDING_TYPES["BUILDING"]
				cell.id = self.id
				row.append(cell)
			rotation.append(row)
		self.rotations.append(rotation)
		
		if width != length:
			rotation = []
			for i in range(width):
				row = []
				for j in range(length):
					cell = Cell(i,j)
					cell.type = TYPES["BUILDING"]
					cell.id = self.id
					row.append(cell)
				rotation.append(row)
			self.rotations.append(rotation)


def get_color(zone):
	if zone == TYPES["RESIDENTIAL"]:
		return "green"
	elif zone == TYPES["COMMERCIAL"]:
		return "blue"
	elif zone == TYPES["INDUSTRIAL"]:
		return "red"
	elif zone == TYPES["ROAD"]:
		return "light_grey"
	elif zone == TYPES["BUILDING"]:
		return "yellow"
	else:
		return "white"


def is_in_bounds(i, j, map):
	return not (i < 0 or i >= len(map) or j < 0 or j >= len(map[0]))


def print_colored(test_map):
	for i in range(len(test_map)):
		for j in range(len(test_map[i])):
			color = get_color(test_map[i][j].type)
			cprint(" ■ ", color, f"on_{color}", end="")
		print()


def print_colored_id(test_map):
	for i in range(len(test_map)):
		for j in range(len(test_map[i])):
			color = get_color(test_map[i][j].type)
			id = test_map[i][j].id
			if id > 0:
				cprint(f" {id} ", color, f"on_{color}", end="")
			else:
				cprint(" ■ ", color, f"on_{color}", end="")
		print()


def check_if_placeable(building, plot, building_type):
	for i in range(len(plot)):
		found = False
		for j in range(len(plot[0])):
			build_length = len(building)
			build_width = len(building[0])

			start_pos = [plot[i][j].i, plot[i][j].j]
			place_pos = start_pos

			for a in range(build_length):
				for b in range(build_width):
					if is_in_bounds(start_pos[0]+a, start_pos[1]+b, plot):
						cell = plot[start_pos[0]+a][start_pos[1]+b]
						if cell.type != building_type:
							place_pos = []
							break
					else:
						place_pos = []
						break
			
			if len(place_pos) == 2:
				found = True
				break
		if found:
			break
	
	return place_pos


def detect_section_filled(section):
	for i in range(section):
		for j in range(section[i]):
			if section[i][j].type != TYPES["BUILDING"] and section[i][j].type != TYPES["NONE"]:
				return False
	return True


def place_buildings(buildings, plot):
	building_type = plot[0][0].type
	for i in range(5):
		random_num = randint(0,len(buildings)-1)
		building = buildings[random_num]
		for rotation in building.rotations:
			place_pos = check_if_placeable(rotation, plot, building_type)
			if len(place_pos) != 0:
				build_length = len(rotation)
				build_width = len(rotation[0])

				for i in range(build_length):
					for j in range(build_width):
						grid[place_pos[0]+i][place_pos[1]+j].type = TYPES["BUILDING"]
						grid[place_pos[0]+i][place_pos[1]+j].id = building.id

				# print_colored_id(rotation)
				# print("------")


def find_shape(starting_cell):
		shape = [[starting_cell]]
		pos = {"i": 0, "j": 0}

		current_cell = starting_cell
		explored.append(starting_cell)
		unexplored = []

		found = False

		
		while not found:
			changed = current_cell
			action_done = False

			# check left
			if is_in_bounds(current_cell.i, current_cell.j-1,grid):
				left = grid[current_cell.i][current_cell.j-1]
				if left.type == current_cell.type and left not in explored:
					explored.append(left)
					if pos["j"] != 0:
						pos["j"] -= 1
						shape[pos["i"]][pos["j"]] = left
					else:
						for i in range(pos["i"]):
							shape[i].insert(0,Cell(0,0))

						shape[pos["i"]].insert(0, left)
						
					current_cell = left
					action_done = True
			
			# check right
			if is_in_bounds(current_cell.i, current_cell.j+1,grid):
				right = grid[current_cell.i][current_cell.j+1]
				if action_done:
					if right.type == current_cell.type and right not in explored:
					# print("hi")
						unexplored.append([pos["i"], pos["j"], current_cell])
				elif right.type == current_cell.type and right not in explored:
					explored.append(right)
					pos["j"] += 1
					try:
						shape[pos["i"]][pos["j"]] = right
					except IndexError:
						shape[pos["i"]] = shape[pos["i"]] + [right]

					
					current_cell = right
					action_done = True

			# check down
			if is_in_bounds(current_cell.i+1, current_cell.j,grid):
				down = grid[current_cell.i+1][current_cell.j]
				if action_done:
					if down.type == current_cell.type and down not in explored:
						unexplored.append([pos["i"], pos["j"], current_cell])
				elif down.type == current_cell.type and down not in explored:
					explored.append(down)
					pos["i"] += 1
					try:
						shape[pos["i"]][pos["j"]] = down
					except IndexError:
						shape.append([Cell(0,0)] * pos["j"] + [down])
						
					current_cell = down
					action_done = True
			
			if current_cell == changed:
				if len(unexplored) != 0:
					pos["i"] = unexplored[0][0]
					pos["j"] = unexplored[0][1]
					current_cell = unexplored[0][2]
					# print(unexplored[0][0], unexplored[0][1])

					unexplored.pop(0)
					# self.print_map(shape)
					# print("-----")
				else:
					found = True

			print([f"{cell.i}, {cell.j}" for cell in explored])
			print_colored(shape)

			# print_colored(shape)
			# print("--------")

		# print("--------")

		return shape


# buildings = []

# onebyone = Building()
# onebyone.id = 1
# onebyone.build(1,1)

# onebytwo = Building()
# onebytwo.id = 2
# onebytwo.build(1,2)

# onebythree = Building()
# onebythree.id = 3
# onebythree.build(1,3)

# twobytwo = Building()
# twobytwo.id = 4
# twobytwo.build(2,2)

# buildings = [onebyone, onebytwo, onebythree, twobytwo]

grid = []

for i in range(3):
	row = []
	for j in range(5):
		road = Cell(i, j)
		road.type = TYPES["ROAD"]
		row.append(road)

	grid.append(row)

for i in range(2):
	grid[i][2].type = TYPES["RESIDENTIAL"]
	grid[i][3].type = TYPES["RESIDENTIAL"]
	grid[i][4].type = TYPES["RESIDENTIAL"]

for i in range(5):
	grid[2][i].type = TYPES["RESIDENTIAL"]

print_colored(grid)

print("-----"*3)

print_colored(find_shape(grid[0][2]))

# print("-----------")

# place_buildings(buildings, test_shape)

# print_colored_id(test_shape)