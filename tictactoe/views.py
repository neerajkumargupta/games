from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls  import reverse
import math
import copy

class newGameForm(forms.Form):
    player1 = forms.CharField(label="Player1")
    player2 = forms.CharField(label="Player2")

def load(request):
        request.session["players"] = []
        request.session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        return render(request, "tictactoe/input.html", {
        "form": newGameForm()
    })


def index(request):
    
    if request.method == "POST":
        form = newGameForm(request.POST)
        if form.is_valid():
            player1 = form.cleaned_data["player1"]
            player2 = form.cleaned_data["player2"]
            request.session["player1"] = player1
            request.session["player2"] = player2
            request.session["turn"] = player1
            print(f" value for player1 and 2 {player1}  {player2} ### {request} ### {request.session.items()}")
            return HttpResponseRedirect(reverse("tictactoe:gameboard"))
        else:
             request.session["players"] = []
             request.session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
             request.session["turn"] = None
             return render(request, "tictactoe/input.html", {
            "form": form
            })

    return render(request, "tictactoe/input.html", {
        "form": newGameForm()
    })

def gameboard(request):
        print(f"play current value of in session {request.session.items()}")
        return render(request, "tictactoe/game.html",{
            "game":request.session["board"],
            "turn":request.session["turn"]
        })

def play(request):
        x = int(request.GET.get('x'))
        y = int(request.GET.get('y'))

        print(f"play current value of in session {request.session.items()}")

        board = request.session["board"]
        player1 = request.session["player1"]
        player2 request.session["player2"]

        if terminal(board,player1,player2):
            winner = winnerboard,player1,player2)
            if x == winner or y == winner:
               print(" Winner is " + winner)
               return render(request, "tictactoe/winner.html", {
                    "winner": winner,
                    "game":request.session["board"]
                })


        request.session["board"][x][y] = request.session["turn"]
        print("Player 1  " +  request.session["player1"])
        print("Player 2  " +  request.session["player2"])
        if request.session["turn"] == request.session["player1"]:
            request.session["turn"] = request.session["player2"]
        elif request.session["turn"] == request.session["player2"]:
            request.session["turn"] = request.session["player1"]
       
        print(f"value of x and y in the request {x} :: {y}")
        return render(request, "tictactoe/game.html",{
            "game":request.session["board"],
            "turn":request.session["turn"]
        })

def back(request):
        print(f"back:  current value of session {request.session.items()}")
        request.session.pop("board")
        request.session.pop("turn")
        return HttpResponseRedirect(reverse("tictactoe:load"))

def reset(request):
        print(f"reset:  current value of session {request.session.items()}")
        request.session["board"] = [[None,None,None], [None,None,None], [None,None,None]]
        request.session["turn"] = request.session["player1"]
        return HttpResponseRedirect(reverse("tictactoe:gameboard"))

def winner(board,player1,player2):
    """
    Returns the winner of the game, if there is one.
    """
    columns = []
    # Checks rows
    
    for row in board:
        xcounter = row.count(player1)
        ocounter = row.count(player2)
        if xcounter == 3:
            return player1
        if ocounter == 3:
            return player2

    # Checks columns
    for j in range(len(board)):
        column = [row[j] for row in board]
        columns.append(column)

    for j in columns:
        xcounter = j.count(player1)
        ocounter = j.count(player2)
        if xcounter == 3:
            return player1
        if ocounter == 3:
            return player2

    # Checks diagonals
    if board[0][0] == player2 and board[1][1] == player2 and board[2][2] == player2:
        return player2
    if board[0][0] == player1 and board[1][1] == player1 and board[2][2] == player1:
        return player1
    if board[0][2] == player2 and board[1][1] == player2 and board[2][0] == player2:
        return player2
    if board[0][2] == player1 and board[1][1] == player1 and board[2][0] == player1:
        return player1

    # No winner/tie
    return None


def terminal(board, player1, player2):
    """
    Returns True if game is over, False otherwise.
    """
    # Checks if board is full or if there is a winner
    empty_counter = 0
    #board = request.session['board']
    for row in board:
        empty_counter += row.count(None)
    if empty_counter == 0:
        return True
    elif winner(board,player1,player2) is not None:
        return True
    else:
        return False
    