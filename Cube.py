class Cube:
    def __init__(self):
        self.U = [['⬜', '⬜', '⬜'], ['⬜', '⬜', '⬜'], ['⬜', '⬜', '⬜']] # up
        self.L = [['🟧', '🟧', '🟧'], ['🟧', '🟧', '🟧'], ['🟧', '🟧', '🟧']] # left
        self.F = [['🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩'], ['🟩', '🟩', '🟩']] # front
        self.R = [['🟥', '🟥', '🟥'], ['🟥', '🟥', '🟥'], ['🟥', '🟥', '🟥']] # right
        self.B = [['🟦', '🟦', '🟦'], ['🟦', '🟦', '🟦'], ['🟦', '🟦', '🟦']] # back
        self.D = [['🟨', '🟨', '🟨'], ['🟨', '🟨', '🟨'], ['🟨', '🟨', '🟨']] # down
        self.sides = [self.U, self.L, self.F, self.R, self.B, self.D]
        self.neighbors = {
            'U': {
                'F': [[0, 2],[0, 1],[0, 0]],
                'L': [[0, 2],[0, 1],[0, 0]],
                'B': [[0, 2],[0, 1],[0, 0]],
                'R': [[0, 2],[0, 1],[0, 0]],
            },
            'L': {
                'F': [[0,0],[1,0],[2,0]],
                'D': [[0,0],[1,0],[2,0]],
                'B': [[2,2],[1,2],[0,2]],
                'U': [[0,0],[1,0],[2,0]],
            },
            'F': {
                'L': [[0,2],[1,2],[2,2]],
                'U': [[2,0],[2,1],[2,2]],
                'R': [[0,0],[1,0],[2,0]],
                'D': [[0,2],[0,1],[0,0]],
            },
            'R': {
                'F': [[2,2],[1,2],[0,2]],
                'U': [[2,2],[1,2],[0,2]],
                'B': [[0,0],[1,0],[2,0]],
                'D': [[2,2],[1,2],[0,2]],
            },
            'B': {
                'R': [[0,2],[1,2],[2,2]],
                'U': [[0,2],[0,1],[0,0]],
                'L': [[0,0],[1,0],[2,0]],
                'D': [[2,0],[2,1],[2,2]],
            },
            'D': {
                'F': [[2,0],[2,1],[2,2]],
                'R': [[2,0],[2,1],[2,2]],
                'B': [[2,0],[2,1],[2,2]],
                'L': [[2,0],[2,1],[2,2]],
            },
            
        }

    def showCube(self):
        ghost = [["  ", "  ", "   "]]
        for side in self.sides:
            if getattr(self, 'U') == side:
                for row in side:
                    for color in ghost[0]:
                        print(color, end='')
                    for color in row:
                        print(color, end='')
                    print('')
            elif getattr(self, 'L') == side:
                print('')
                order = ['F', 'R', 'B']
                for row in range(len(side)):
                    for color in side[row]:
                        print(color, end='')
                    print(' ', end='')
                    for sideInOrder in order:
                        for color in getattr(self, sideInOrder)[row]:
                            print(color, end='')
                        print(' ', end='')

                    print('')  
            elif getattr(self, 'D') == side:
                print('')
                for row in side:
                    for color in ghost[0]:
                        print(color, end='')
                    for color in row:
                        print(color, end='')
                    print('')

    def showSide(self, sideName):
        side = getattr(self, sideName)
        for row in side:
            for color in row:
                print(color, end='')
            print('')
        
    def cycle(self, side_name, prime=False):
        side = getattr(self, side_name)
        all_colors = [] # список в который с помощью цикла добавляются все ячейки одной стороны кроме центра
        last_color = ''
        for row in range(len(side)):
            correctRow = list(reversed(side[row])) if row == 2 else side[row]
            for color in range(len(correctRow)):
                if row == 1 :
                    if color == 0:
                        last_color = correctRow[color]
                    elif color == 2:
                        all_colors.append(correctRow[color])
                else:
                    all_colors.append(correctRow[color])
        all_colors.append(last_color)

        # поворот внутри списка с ячейками стороны на 90 deg
        temp_el = 0
        safe_el = 0
        for _ in range(6 if prime else 2):
            for i in range(len(all_colors)):
                temp_el = all_colors[i + 1]
                all_colors[i+1] = safe_el if i > 0 else all_colors[i]
                safe_el = temp_el
                if i == 6:
                    all_colors[0] = safe_el
                    break

        # Изменение ячеек на самом кубе
        for row in range(len(side)):
            for color in range(3):
                match row:
                    case 0:
                        side[row][color] = all_colors[color]
                    case 1:
                        side[row][0] = all_colors[-1]
                        side[row][-1] = all_colors[3]
                    case 2:
                        rightLayerColors = list(reversed(all_colors[-4:-1]))
                        side[row][color] = rightLayerColors[color]

        # Поворот ячеек на других сторонах
        all_other_colors = []
        for sideStr, elOrder in self.neighbors[side_name].items():
            side = getattr(self, sideStr)
            for row, color in elOrder:
                all_other_colors.append(side[row][color])
        
        # поворот внутри списка с ячейками других сторон на 90 deg
        for _ in range(9 if prime else 3):
            for i in range(len(all_other_colors)):
                temp_el = all_other_colors[i + 1]
                all_other_colors[i+1] = safe_el if i > 0 else all_other_colors[i]
                safe_el = temp_el
                if i == 10:
                    all_other_colors[0] = safe_el
                    break
        
        # Изменение ячеек на самом кубе
        neighbors = self.neighbors[side_name]
        for neighborIndex in range(len(neighbors.items())):
            sideStr, elOrder = list(neighbors.items())[neighborIndex]
            side = getattr(self, sideStr)
            
            for orderElementindex in range(len(elOrder)):
                row, color = elOrder[orderElementindex]
                side[row][color] = all_other_colors[(3 * neighborIndex) + orderElementindex]

cube = Cube()
# cube.cycle('F')
# cube.cycle('F')

# cube.cycle('U')
# cube.cycle('U')

# cube.cycle('F')
# cube.cycle('F')

# cube.cycle('D')
# cube.cycle('D')

# cube.cycle('L')

# cube.cycle('R')
# cube.cycle('R')

# cube.cycle('U')
# cube.cycle('U')

# cube.cycle('L')
# cube.cycle('L')

# cube.cycle('F')
# cube.cycle('F')

# cube.cycle('U')
# cube.cycle('U')

# cube.cycle('F')
# cube.cycle('F')

# cube.cycle('U', prime=True)

# cube.cycle('R')
# cube.cycle('R')

# cube.cycle('B')

# cube.cycle('D', prime=True)

# cube.cycle('L')

# cube.cycle('R')

# cube.cycle('B')
# cube.cycle('B')

# cube.cycle('D')
# cube.cycle('D')

# cube.cycle('B')
# cube.cycle('B')



cube.showCube()