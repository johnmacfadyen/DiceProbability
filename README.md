# Dice Probability Calculator

This is a Python application that calculates the probability of rolling a certain number on a dice using the cumulative distribution function. It also includes a PyQt6 GUI application to display the results.
Built as a coding challenge from [RobertHartleyGM](https://roberthartleygm.com/) in his discord server for a D&D casino game to help determine payout. 

Logo from [freepngimg](https://freepngimg.com/download/dice/90810-and-dice-d20-dungeons-system-dragons-black.png)

## Installation

To use this application, you will need to have Python 3 installed on your computer. You can download Python from the official website: <https://www.python.org/downloads/>

You will also need to install the following Python libraries:

- PyQt6
- pyqtgraph
- numpy

You can install these libraries using pip, the Python package manager. Open a terminal or command prompt and run the following commands:

```shell
pip install PyQt6
pip install pyqtgraph
pip install numpy
```

## Usage

To use the application, run the `DiceProbability.py` file using Python. This will open the GUI window.

In the GUI window, you can select the number of sides on the dice, the target number, and the maximum number of rolls to consider. Click the "Calculate" button to calculate the probability of rolling the target number in up to the maximum number of rolls.

The results will be displayed in a bar graph, showing the probability of winning, partial winning, and losing. You can hover over each bar to see the exact probability value.

## Code

The `DiceProbability.py` file contains the Python code for the application. The `cumulative_probabilities` function is used to calculate the probabilities using dynamic programming. The PyQt6 library is used to create the GUI window and display the results using a bar graph.
