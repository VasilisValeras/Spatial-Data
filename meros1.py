#Vasileios Valeras 4031

# Import the csv module
import csv

# Set initial values for minX, maxX, minY, maxY
minX = float('inf')
maxX = float('-inf')
minY = float('inf')
maxY = float('-inf')

f = input("Please provide me the .csv file you want to work with: ")

# Open the CSV file
with open(f) as file:
    reader = csv.reader(file)

    # Read the total number of linestrings
    total_linestrings = next(reader)[0]

    # Create a list to store the linestrings
    linestrings = []
    id = 1

    # Iterate over each row in the CSV file
    for row in reader:

        # Create an empty list to store the coordinates of the current linestring
        linestring = []

        # Split the row string by spaces and convert the first two values to float values
        temp = row[0].split()
        x, y = float(temp[0]), float(temp[1])

        # Set the minimum bounding rectangle (MBR) values for the current linestring to the x and y values
        MBRminX, MBRminY, MBRmaxX, MBRmaxY = x, y, x, y

        # Iterate over the points in the row string and convert them to float values
        for i in range(len(row)):
            points = row[i].split()
            x, y = float(points[0]), float(points[1])

            # Update the MBR values based on the x and y values
            if x <= MBRminX:
                MBRminX = x
            if x >= MBRmaxX:
                MBRmaxX = x
            if y <= MBRminY:
                MBRminY = y
            if y >= MBRmaxY:
                MBRmaxY = y

            # Append the x and y values to the linestring list
            linestring.append([x, y])

        # Update the overall MBR values based on the current linestring
        if MBRminX < minX:
            minX = MBRminX
        if MBRmaxX > maxX:
            maxX = MBRmaxX
        if MBRminY < minY:
            minY = MBRminY
        if MBRmaxY > maxY:
            maxY = MBRmaxY

        # Append the linestring ID, MBR, and coordinates to the linestrings list
        linestrings.append([id, [[MBRminX, MBRminY],[ MBRmaxX, MBRmaxY]], linestring])

        # Increment the linestring ID
        id += 1



# Create a 10x10 grid
x_interval = (maxX - minX) / 10
y_interval = (maxY - minY) / 10
grid = []
for j in range(9, -1, -1):
    y_min = minY + j * y_interval
    y_max = y_min + y_interval
    for i in range(10):
        x_min = minX + i * x_interval
        x_max = x_min + x_interval
        grid.append([(i, j), [x_min, y_min, x_max, y_max]])



#for i in range(len(grid)):
#    if i % 10 == 0:
#        print()
#    print(str(grid[i][0]) + str(grid[i][1]) )

#print("")

# Create a dictionary to store the set of linestring IDs in each cell of the grid
cell_dict = {}

# Initialize the dictionary with an empty set for each cell in the grid
for cell in grid:
    cell_dict[cell[0]] = set()

# Iterate over each linestring and add it to the cell(s) it intersects with
for linestring in linestrings:
    # Find the minimum bounding rectangle (MBR) of the linestring
    min_mbr_cell = None
    max_mbr_cell = None
    for cell in grid:
        # Check if the start point of the linestring is within the current cell
        if cell[1][0] <= linestring[1][0][0] <= cell[1][2] and cell[1][1] <= linestring[1][0][1] <= cell[1][3]:
            cell_dict[cell[0]].add(linestring[0])
            if min_mbr_cell is None:
                min_mbr_cell = cell[0]
        # Check if the end point of the linestring is within the current cell
        if cell[1][0] <= linestring[1][1][0] <= cell[1][2] and cell[1][1] <= linestring[1][1][1] <= cell[1][3]:
            if cell[0] not in cell_dict:
                cell_dict[cell[0]] = set()
            cell_dict[cell[0]].add(linestring[0])
            if max_mbr_cell is None:
                max_mbr_cell = cell[0]

    # If the linestring spans multiple cells, add it to all cells between min_mbr_cell and max_mbr_cell
    if min_mbr_cell != max_mbr_cell:
        for x in range(min_mbr_cell[0], max_mbr_cell[0]+1):
            for y in range(min_mbr_cell[1], max_mbr_cell[1]+1):
                if (x,y) != min_mbr_cell and (x,y) != max_mbr_cell:
                    if (x,y) not in cell_dict:
                        cell_dict[(x,y)] = set()
                    cell_dict[(x,y)].add(linestring[0])

# Create a dictionary to store the minmax MBR and coordinates of each linestring
linestring_dict = {}
for ls in linestrings:
    linestring_dict[ls[0]] = {'minmax_mbr': ls[1], 'coordinates': ls[2]}



# Write the linestrings to the grid file
with open("grid.grd", "w") as f:
    for i in range(10):
        for j in range(10):
            cell_key = (i, j)
            cell_linestrings = cell_dict.get(cell_key, [])
            for linestring in cell_linestrings:
                ls_info = linestring_dict.get(linestring, None)
                if ls_info is not None:
                    f.write(str(linestring) + ", " + str(ls_info['minmax_mbr'][0][0]) + " " + str(ls_info['minmax_mbr'][0][1]) + ", " + str(ls_info['minmax_mbr'][1][0]) + " " + str(ls_info['minmax_mbr'][1][1]) + ", " + ", ".join(str(coord[0]) + " " + str(coord[1]) for coord in ls_info['coordinates']) + "\n")

with open("grid.dir", "w") as f:
    line = 1
    # Write the bounding box
    f.write(f"{line} {minX} {maxX} {minY} {maxY}\n")
    line += 1
    # Write the cell information

    for i in range(10):
        for j in range(10):
            cell_key = (i, j)
            cell_linestrings_number = len(cell_dict.get(cell_key, []))
            f.write(str(line) +" "+str(cell_key[0]) + " " + str(cell_key[1]) + " " + str(cell_linestrings_number) + "\n")
            line+=1





