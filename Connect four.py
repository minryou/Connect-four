""" 
Name : Min Ryou
ID : 720682435
Username : mryo272
This program is a game that is similar to connect 4. Each player will consecutively place an 'x' or an 'o' until the whole board is full, in which the player with the most connect fours will be the winner.
"""
class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
    
    
    def num_free_positions_in_column(self, column):
        return self.size - self.num_entries[column]
        
    def game_over(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.items[i][j] == 0:
                    return False
        return True
    
    def display(self):
        for i in range(self.size -1, -1,-1):
            for j in range(self.size):
                if self.items[j][i] == 0:
                    print(" ", end=" ")
                elif self.items[j][i] == 1:
                    print("o", end = " ")
                elif self.items[j][i] == 2:
                    print("x", end =" ")
            print()
        print("-" * (self.size * 2 - 1))
        
        for k in range(self.size):
            print(k, end = " ")
        print()
        print("Points player 1:", self.points[0])
        print("Points player 2:", self.points[1])
        
    
    def num_new_points(self,column,row,player):
        count = 0
        for i in range(column - 3, column + 1):
            if i >= 0:
                try:
                    if self.items[i][row] == player and self.items[i+1][row] == player and self.items[i+2][row] == player and self.items[i+3][row] == player:
                        count += 1
                except:
                    pass

        for i in range(-3, 1):
            if column + i >= 0 and row + i >= 0:
                try:
                    if self.items[column + i][row + i] == player and self.items[column + i + 1][row + i + 1] == player and self.items[column + i + 2][row + i + 2] == player and self.items[column + i + 3][row + i + 3] == player:
                        count += 1
                except:
                    pass

        for i in range(row - 3, row + 1):
            if i >= 0:
                try:
                    if self.items[column][i] == player and self.items[column][i + 1] == player and self.items[column][i + 2] == player and self.items[column][i + 3] == player:
                        count += 1
                except:
                    pass

        for i in range(-3, 1):
            if column + i >= 0 and row - i - 3 >= 0:
                try:
                    if self.items[column + i][row - i] == player and self.items[column + i + 1][row - i - 1] == player and self.items[column + i + 2][row - i - 2] == player and self.items[column + i + 3][row - i - 3] == player:
                        count += 1
                except:
                    pass

        return count
            
    def add(self, column, player):
        if column < 0 or column >= self.size or self.num_free_positions_in_column(column) == 0:
            return False

        row = self.num_entries[column]
        self.items[column][row] = player
        self.num_entries[column] +=  1
        self.num_new_points(row, column, player)
        self.points[player - 1] += self.num_new_points(column, row, player)
        return True      

    def free_slots_as_close_to_middle_as_possible(self): 
        my_list = []
        x = self.size
        if x % 2 == 0:
            middle = x // 2
            for i in range(middle):
                calc1 = (x - 1) // 2 - i
                calc2 = (x - 1) // 2 + i + 1
                my_list.append(calc1)
                my_list.append(calc2)
        else:
            middle = x // 2
            my_list.append(middle)
            for i in range(1, middle + 1):
                calc1 = (x - 1) // 2 - i
                calc2 = (x - 1) // 2 + i
                my_list.append(calc1)
                my_list.append(calc2)

        for i in range(len(my_list)-1,-1,-1):
            if self.num_free_positions_in_column(my_list[i]) == 0:
                my_list.pop(i)
        return my_list
        
        
    def column_resulting_in_max_points(self, player):
        list_of_possible_points = []
        for i in range(self.size):
            if self.num_entries[i] < self.size:
                row = self.num_entries[i]
                self.items[i][row] = player
                list_of_possible_points.append([i,self.num_new_points(i,row,player)])
                self.items[i][row] = 0

        max_list = []
        max_value = 0
        for i,j in enumerate(list_of_possible_points):
            possible_points = list_of_possible_points[i][1]
            if possible_points > max_value:
                max_value = possible_points

        for i,j in enumerate(list_of_possible_points):
            possible_points = list_of_possible_points[i][1]
            if possible_points == max_value:
                max_list.append(list_of_possible_points[i])
                
        middle_list = self.free_slots_as_close_to_middle_as_possible()
        if len(middle_list) > 0:
            for i in range(len(middle_list)):
                for j in range(len(max_list)):
                    if middle_list[i] == max_list[j][0]:
                        return tuple(max_list[j])
        else:
            return [],
class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            else:
                                print("Column ", column, "is alrady full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(6)
game.play()      