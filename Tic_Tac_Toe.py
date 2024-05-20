import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self) -> None:
        self.name = ""
        self.symbol = ""

    def choose_symbol(self, chosen_symbol):
        self.symbol = chosen_symbol

    def choose_name(self, taken_names): #argument name 
        while True:
            name = input("enter your name: ").capitalize()
            valid = self.valid_name(name, taken_names)
            if valid is None:
                self.name = name
                break
            print(valid)

    def valid_name(self, name, taken_names):
        if not name.isalpha():
            return "name should consist of only alphabetic letters"
        if not (3 <= len(name) <= 8):
            return "Invalid lenght"
        if name in taken_names:
            return "this name is already exist"
        return None


class Board:
    def __init__(self):
        self.cells = [' ' for _ in range(1,10)]

    def display_board(self):
        for i in range(0,9,3):
            print("%s │ %s │ %s" % tuple(self.cells[i:i+3]))
            if i < 6:
                print("──┼───┼──")

    def reset_board(self):
        self.cells = [' ' for _ in range(1,10)]

    def update_board(self, choice, symbol): #parametres
        if self.invalid_move(choice): 
            return False      
        self.cells[choice - 1] = symbol 
        return True #don't forgot

    def invalid_move(self, choice): #choice
        return self.cells[choice - 1] != ' '


class Menu:
    @staticmethod
    def display_main_menu():
        print("Welcome to tic-tac-toe\n")
        choices = {
            "1": "Start Game", 
            "2": "Read Instructions",
            "3": "Quit Game"
        }
        for key, value in choices.items(): #loop to print dict
            print(f"{key}: {value}")
        choice = input("Enter your choice: ")
        if choice in choices:
            return choice #not true
        else:
            clear_screen()
            print("Please enter a valid option.\n")

    @staticmethod
    def display_endgame_menu():
        choices = {
            "1": "Restart Game", 
            "2": "Start New Game", 
            "3": "Quit Game"
        }
        for key, value in choices.items(): 
            print(f"{key}: {value}")
        choice = input("Enter your choice: ")
        if choice in choices:
            return choice
        else:
            print("Please enter a valid option.\n")

    instructions = """
    1-
    2-
    3-
    ...
""" #i have to write instructions

    @staticmethod
    def display_instructions():
        print(Menu.instructions)
        input("Press Enter to return to the main menu...")
        clear_screen()
        return Menu.display_main_menu() 


class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def setup_players(self):
        available_symbols = ['X', 'O']
        taken_names = []
        for number, player in enumerate(self.players, start = 1):
            clear_screen()
            print(f"Player {number} enter your details..")
            player.choose_name(taken_names)
            taken_names.append(player.name)
            if number == 1:
                clear_screen()
                chosen_symbol = input(f"{player.name} choose your symbol X or O: ").upper()
                while chosen_symbol not in available_symbols: 
                    print(f"invalid symbol, {player.name} please choose either X or O")
                    chosen_symbol = input(f"{player.name} choose your symbol X or O: ").upper()
                    #break!
            else:
                chosen_symbol = 'X' if self.players[0].symbol == 'O' else 'O'
            player.choose_symbol(chosen_symbol)
            print(f"{player.name} {player.symbol}")

    def start_game(self):
        clear_screen()
        choice = self.menu.display_main_menu()
        if choice == '1':
            self.setup_players()
            self.play_game()
        if choice == '2':
            self.menu.display_instructions()
        if choice == '3':
            self.quit()
        else:
            self.menu.display_main_menu()
        

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win():
                clear_screen()
                self.board.display_board()
                winner = self.players[self.current_player_index]
                print(f"\n{winner.name} wins!\n")
                self.handle_endgame_choice()
                break
            elif self.check_draw():
                print("it's a draw!\n")
                self.handle_endgame_choice()
                break

    def quit(self):
        print("Good bye!\n")
        sys.exit()

    def play_turn(self):
        player = self.players[self.current_player_index]
        clear_screen()
        self.board.display_board()
        while True:
            try:
                cell_choice = int(input(f"\n{player.name} ({player.symbol}) choose a valid cell: "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    clear_screen()
                    self.board.display_board()
                    print("\nInvalid move, try again")
            except ValueError:
                clear_screen()
                self.board.display_board()
                print("\nPlease enter a number between 1 and 9.")

        if not self.check_win() or self.check_draw():
            self.switch_player()    

    def check_win(self):
        symbol = self.players[self.current_player_index].symbol
        combo = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Rows
            [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Columns
            [1, 5, 9], [3, 5, 7]  # Diagonal
        ]
        for combination in combo:
            if all(self.board.cells[cell_no - 1] == symbol for cell_no in combination):
                return True
        return False 

    def handle_endgame_choice(self):
        choice = self.menu.display_endgame_menu()
        if choice == '1':
            self.restart_game()  
        elif choice == '2':
            self.setup_new_game()  
        elif choice == '3':
            self.quit()  
        else:
            choice = self.menu.display_endgame_menu()


    def check_draw(self):
        if not self.check_win() and ' ' not in self.board.cells[1:]:
            return True
        return False


    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def restart_game(self):
        self.current_player_index = 0
        self.board.reset_board()
        self.play_game()

    def setup_new_game(self):
        self.setup_players()
        self.restart_game()



if __name__ == "__main__":
    game = Game() 
    game.start_game()  
