# TKtictac

Tic-tac-toe (American English), noughts and crosses (Commonwealth English), or Xs and Os is a paper-and-pencil game for two players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row is the winner.

<p align="center">
  <img src="https://raw.githubusercontent.com/Saadmairaj/TKtictac/master/assets/sample1.png?token=ALAV6GAWGL2IWXBX5TZP45K7JNR5W" height="300"><img src="https://raw.githubusercontent.com/Saadmairaj/TKtictac/master/assets/sample2.png?token=ALAV6GHKHQVAW3MBNJIFH6C7JNR3C" height="300">
</p>

## Game play

In order to win the game, a player must place three of their marks in a horizontal, vertical, or diagonal row. The game is only one player against the computer. There are 4 difficulty mode which can be selected from the setting menu plus some other options that can be selected as well to improve experience of the user.

<p align="center">
  <img src="https://raw.githubusercontent.com/Saadmairaj/TKtictac/master/assets/settings%20sample.png?token=ALAV6GERAB3QMQFFZYQZDR27JNRX4" height="300">
</p>

## Dependencies

  1. Python 3
  2. Pygame (Used for sound effects)
  3. tkmacosx
  4. Pillow (PIL)

## Installation

1. Clone this git repo
    
    ```bash
    $ git clone https://github.com/Saadmairaj/TKtictac.git
    ```

2. Change directory to the Tktictac and create a virtual environment
    
    ```bash
    $ cd Tktictac
    $ python -m venv env
    ```

3. Activate the virtual environment and install the dependencies

    ```bash
    $ source env/bin/activate
    $ pip install -r requirements.txt
    ```
4. Now, we are ready to go! Run the Tktictac with the following command

    ```bash
    $ python __main__.py
    ```
    
## Changelog

  0.0.2
  * Improved user interface
  * Fix issues with overrideredirect on different platforms

  0.0.1
  * Fixed issues with sound
  * Fixed issues with Light mode
  * Fixed issues with titlebar 
  * Added icon
  * Some other Bug fixes 
  
  0.0.0
  * Stable release

## License

[MIT](https://github.com/Saadmairaj/TKtictac/blob/master/LICENSE)
