# Snake

This repository contains code for my final project for Python Programming.
It is a simple Python app using Pygame for GUI interface and logic.
Although this README is written in english, I was using mainly polish while constructing code

## Setup
- Follow the steps below if you want to set up the project and
run the snake game.

- In order to run the code you need to have Python 3.6+ installed.
Then you need to create and activate a virtual environment, like so:
```
python -m venv .venv
source .venv/bin/activate
```

- Then you can install the required dependencies:
```
pip install -r requirements.txt
```

## Run the app
- You can run the Snake game by using:
```
python -m main
```
- The GUI will show up, press any button and the game will start.

## Modify number of rocks on the field
- There is an option to add any number of rocks on the field, by hitting which snake will also die.
- To modify number of rocks, click was used, so you can change it using command (placing number wanted)
- Of course, you can also change it in the code, replacing the "default" digit

```
python -m main --liczba_kamieni_click 5
```
## Change other parameters
- In the code you can also change the size of the board, by changing "liczba_boxow_w_rzedzie" variable in two places of the code - "main" function and "kwadrat" class.
- What is more, you can change speed of the snake by changing "tempo_gry" variable in "main" function.

