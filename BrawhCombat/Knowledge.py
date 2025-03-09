from utilities import *

pygame.init()

started = False
winner = False
restarted = False


def main():
    global started, winner, restarted, player1, player2, players
    while not started:
        started = main_menu()

    winner = game()
    restarted = game_over(winner)
    if restarted:
        restarted = False
        started, winner, player1, player2, players = restart()
        main()


if __name__ == "__main__":
    main()
