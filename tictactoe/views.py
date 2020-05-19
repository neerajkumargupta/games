from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls  import reverse

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

    