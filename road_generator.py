import random
import time
from termcolor import cprint, colored

TYPES = {
	"NONE": 0,
	"RESIDENTIAL": 1,
	"COMMERCIAL": 2,
	"INDUSTRIAL": 3,
	"DECORATION": 4,
	"BUILDING": 5,
	"ROAD": 7
}

SIZES = {
	0: { "min_size": 0, "max_size": 0 },
	1: { "min_size": 2, "max_size": 4 },
	2: { "min_size": 3, "max_size": 6 },
	3: { "min_size": 4, "max_size": 6 },
}

building_ids = [-1, -2, -3, -4]


class Cell():
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.type = TYPES["NONE"]
		self.id = -1


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
				cell.type = TYPES["BUILDING"]
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


class CityGenerator():
	def __init__(self, map_size):
		self.map_size = map_size
		self.grid = []
		self.explored = []


	def shuffle(self, array):
		copy = []
		n = len(array)
		
		# While there remain elements to shuffle...
		while n:
			# Pick a remaining element
			i = random.randint(0, len(array)-1)

			# If not already shuffled, move it to the new array
			if i < len(array):
				copy.append(array[i])
				del array[i]
				n -= 1
		
		return copy


	# Get all cells as a 1-dimensional array
	def get_all_cells(self):
		cells = []

		for i in range(0, self.map_size, 2):
			for j in range(0, self.map_size, 2):
				cells.append(self.grid[i][j])

		return cells


	def is_in_bounds(self, i, j, map):
		if not (i < 0 or i >= len(map)):
			return not (j < 0 or j >= len(map[i]))
		return False


	# Check if the neighbor to the right or below is a road and if so replace self as a road cell
	def check_if_road(self, i, j):
		if self.is_in_bounds(i+1, j, self.grid) and self.grid[i+1][j].id != self.grid[i][j].id:
			self.grid[i][j].type = TYPES["ROAD"]

		if self.is_in_bounds(i, j+1, self.grid) and self.grid[i][j+1].id != self.grid[i][j].id:
			self.grid[i][j].type = TYPES["ROAD"]


	def generate_empty_grid(self):
		for i in range(self.map_size):
			self.grid.append([])
			for j in range(self.map_size):
				self.grid[i].append(Cell(i, j))


	def get_random_section_type(self):
		rand_num = random.randint(1,20)
		zone_type = TYPES["NONE"]

		if 1 <= rand_num <= 13:
			zone_type = TYPES["RESIDENTIAL"]
		elif 13 < rand_num <= 19:
			zone_type = TYPES["COMMERCIAL"]
		elif 19 < rand_num <= 20:
			zone_type = TYPES["INDUSTRIAL"]
		
		min_size = SIZES[zone_type]["min_size"]
		max_size = SIZES[zone_type]["max_size"]

		direction = 1 if random.random() > 0.5 else 0
		square_width = random.randint(min_size, max_size if direction else min_size)
		square_height = random.randint(min_size, min_size if direction else max_size)

		# square_width = random.randint(min_size, max_size)
		# square_height = random.randint(min_size, max_size)

		return zone_type, square_height, square_width

	
	def populate_grid(self):

		# Get a random order to loop through the cells
		check_order = self.shuffle(self.get_all_cells())

		for id in range(1, len(check_order)):
			curTile = check_order[id]

			if curTile.type == TYPES["NONE"]:
				zone, square_height, square_width = self.get_random_section_type()

				for i in range(0, square_width, 2):
					for j in range(0, square_height, 2):
						if self.is_in_bounds(curTile.i + i+1, curTile.j + j+1, self.grid):
							self.grid[curTile.i + i][curTile.j + j].id = id
							self.grid[curTile.i + i][curTile.j + j].type = zone

							self.grid[curTile.i + i+1][curTile.j + j].id = id
							self.grid[curTile.i + i+1][curTile.j + j].type = zone

							self.grid[curTile.i + i][curTile.j + j+1].id = id
							self.grid[curTile.i + i][curTile.j + j+1].type = zone

							self.grid[curTile.i + i+1][curTile.j + j+1].id = id
							self.grid[curTile.i + i+1][curTile.j + j+1].type = zone


		for i in range(self.map_size):
			for j in range(self.map_size):
				self.check_if_road(i,j)

		return self.grid


	def get_color(self, zone):
		if zone == TYPES["RESIDENTIAL"]:
			return "green"
		elif zone == TYPES["COMMERCIAL"]:
			return "blue"
		elif zone == TYPES["INDUSTRIAL"]:
			return "red"
		elif zone == TYPES["DECORATION"]:
			return "yellow"
		elif zone == TYPES["BUILDING"]:
			return "grey"
		elif zone == TYPES["ROAD"]:
			return "light_grey"
		else:
			return "white"
		

	def get_building_color(self, id):
		if id == -1:
			return "cyan"
		elif id == -2:
			return "magenta"
		elif id == -3:
			return "light_green"
		elif id == -4:
			return "light_red"
		else:
			return "white"


	def print_map(self, map):
		for i in range(len(map)):
			for j in range(len(map[i])):
				color = self.get_color(map[i][j].type)
				cprint(" ■ ", color, f"on_{color}", end="")
			print()


	def print_colored_id(self, map):
		for i in range(len(map)):
			for j in range(len(map[i])):
				color = self.get_color(map[i][j].type)
				id = map[i][j].id
				if id in building_ids:
					color = self.get_building_color(id)
					cprint(f" {abs(id)} ", color, f"on_{color}", end="")
				else:
					cprint(" ■ ", color, f"on_{color}", end="")
				# cprint(f" {id} ", color, f"on_{color}", end="")
			print()


	def print_roads(self, map):
		for i in range(len(map)):
			for j in range(len(map[i])):
				if map[i][j].type == TYPES["ROAD"]:
					color = self.get_color(map[i][j])
					road_type = self.find_road_neighbors(i, j)
					# cprint(" ■ ", color, f"on_{color}", end="")
					cprint(f" {road_type} ", color, f"on_{color}", end="")
				else:
					print("   ", end="")
			print()

	
	def find_road_neighbors(self, i, j):
		neighbor_roads = {
			"up": None,
			"down": None,
			"left": None,
			"right": None
		}

		intersections = 0

		# find up neighbor
		if self.is_in_bounds(i-1,j,self.grid):
			if self.grid[i-1][j].type == TYPES["ROAD"]:
				neighbor_roads["up"] = self.grid[i-1][j]
				intersections += 1
		# find down neighbor
		if self.is_in_bounds(i+1,j,self.grid):
			if self.grid[i+1][j].type == TYPES["ROAD"]:
				neighbor_roads["down"] = self.grid[i+1][j]
				intersections += 1
		# find left neighbor
		if self.is_in_bounds(i,j-1,self.grid):
			if self.grid[i][j-1].type == TYPES["ROAD"]:
				neighbor_roads["left"] = self.grid[i][j-1]
				intersections += 1
		# find right neighbor
		if self.is_in_bounds(i,j+1,self.grid):
			if self.grid[i][j+1].type == TYPES["ROAD"]:
				neighbor_roads["right"] = self.grid[i][j+1]
				intersections += 1

		return intersections


	def find_shape(self, starting_cell):
		shape = [[starting_cell]]
		pos = {"i": 0, "j": 0}

		current_cell = starting_cell
		self.explored.append(starting_cell)

		found = False

		
		while not found:
			changed = current_cell

			# check left
			if self.is_in_bounds(current_cell.i, current_cell.j-1,self.grid):
				left = self.grid[current_cell.i][current_cell.j-1]
				if left.type == current_cell.type and left not in self.explored:
					self.explored.append(left)
					if pos["j"] != 0:
						pos["j"] -= 1
					# else:
						# for i in range(pos["i"]):
						# 	shape[i] = [Cell(0,0)] + shape[i]
					
					try:
						shape[pos["i"]][pos["j"]] = left
					except IndexError:
						# shape[pos["i"]] = shape[pos["i"]][:pos["i"]] + [left] + shape[pos["i"]:]
						shape[pos["i"]].insert(0, left)
						
					current_cell = left
					continue
			
			# check right
			if self.is_in_bounds(current_cell.i, current_cell.j+1,self.grid):
				right = self.grid[current_cell.i][current_cell.j+1]
				if right.type == current_cell.type and right not in self.explored:
					self.explored.append(right)
					pos["j"] += 1
					try:
						shape[pos["i"]][pos["j"]] = right
					except IndexError:
						# shape[pos["i"]] = shape[pos["i"]][:pos["j"]+1] + [right] + shape[pos["i"]][pos["j"]+1:]
						# for i in range(pos["i"]):
						# 	shape[i] = shape[i].append(Cell(0,0))
						shape[pos["i"]] = shape[pos["i"]] + [right]

					
					current_cell = right
					continue

			# check down
			if self.is_in_bounds(current_cell.i+1, current_cell.j,self.grid):
				down = self.grid[current_cell.i+1][current_cell.j]
				if down.type == current_cell.type and down not in self.explored:
					self.explored.append(down)
					pos["i"] += 1
					try:
						shape[pos["i"]][pos["j"]] = down
					except IndexError:
						shape.append([Cell(0,0)] * pos["j"] + [down])
						
					current_cell = down
					continue
			
			if current_cell == changed:
				found = True

			# print_colored(shape)
			# print("--------")

		return shape
	

	def detect_shapes(self):
		shapes = []

		for row in self.grid:
			for i in range(len(row)):
				if row[i].type != TYPES["ROAD"]:
					if row[i] not in self.explored:
						shape = self.find_shape(row[i])
						# if len(shape) == 1 and len(shape[0]) == 1 and random.randint(1,2) == 1:
						# 	cell = shape[0][0]
						# 	self.grid[cell.i][cell.j].type = TYPES["DECORATION"]
						
						# self.print_map(shape)
						# print("-"*len(shape[0]))
						shapes.append(shape)
		
		return shapes


	def check_if_placeable(self, building, plot, building_type):
		for i in range(len(plot)):
			found = False
			for j in range(len(plot[i])):
				build_length = len(building)
				build_width = len(building[0])
				# print(f"{i}, {j}")
				start_pos = [plot[i][j].i, plot[i][j].j]
				place_pos = start_pos

				for a in range(build_length):
					for b in range(build_width):
						if self.is_in_bounds(i+a, j+b, plot):
							cell = plot[i+a][j+b]
							if cell.type != building_type:
								place_pos = []
								break
						else:
							place_pos = []
							break
					if len(place_pos) == 0:
						break
				
				if len(place_pos) == 2:
					found = True
					break
			if found:
				break
		
		return place_pos


	def detect_section_filled(self, section):
		# print("new")
		# self.print_map(section)
		# print("-----")
		for i in range(len(section)):
			for j in range(len(section[i])):
				# print(section[i][j].id)
				# time.sleep(0.1)
				section_cell = section[i][j]
				if section_cell.type != TYPES['NONE']:
					cell = self.grid[section_cell.i][section_cell.j]
					if cell.type != TYPES["BUILDING"] and cell.type != TYPES["NONE"]:
						return False
		return True


	def place_buildings_in_plot(self, buildings, plot):
		building_type = plot[0][0].type
		for x in range(len(plot)):
			for y in range(len(plot[x])):
				if plot[x][y].type != TYPES["NONE"]:
					building_type = plot[x][y].type
					break
		while not self.detect_section_filled(plot):
			random_num = random.randint(0,len(buildings)-1)
			building = buildings[random_num]
			for rotation in building.rotations:
				place_pos = self.check_if_placeable(rotation, plot, building_type)
				# print(place_pos)
				if len(place_pos) != 0:
					build_length = len(rotation)
					build_width = len(rotation[0])
					# print(building.id)

					for i in range(build_length):
						for j in range(build_width):
							self.grid[place_pos[0]+i][place_pos[1]+j].type = TYPES["BUILDING"]
							self.grid[place_pos[0]+i][place_pos[1]+j].id = building.id
					
					break
		
		# self.print_colored_id(plot)
		# print("------")

			# time.sleep(0.01)

	
	def place_buildings_in_map(self, buildings, sections):
		# print(len(sections))
		for section in sections:
			self.place_buildings_in_plot(buildings, section)



# generate buildings to place
buildings = []

onebyone = Building()
onebyone.id = -1
onebyone.build(1,1)

onebytwo = Building()
onebytwo.id = -2
onebytwo.build(1,2)

onebythree = Building()
onebythree.id = -3
onebythree.build(1,3)

twobytwo = Building()
twobytwo.id = -4
twobytwo.build(2,2)

buildings = [onebyone, onebytwo, onebythree, twobytwo]

# generate a city map
city_generator = CityGenerator(30)
city_generator.generate_empty_grid()
city_map = city_generator.populate_grid()
# city_generator.print_roads(city_map)
city_generator.print_map(city_map)

print("-"*len(city_map)*3)

# detect and store sections of city
sections = city_generator.detect_shapes()
# for section in sections:
# 	city_generator.print_map(section)
# 	print("---------")
# city_generator.print_map(city_map)
# print("-"*len(city_map)*3)
city_generator.place_buildings_in_map(buildings, sections)

city_generator.print_colored_id(city_map)
