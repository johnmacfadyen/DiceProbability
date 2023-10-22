# Application to work out the probability of rolling a certain number on a dice using cumulative distribution function. 
# PyQt6 GUI application to display the results.

# Importing the required libraries
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QPushButton, QComboBox, QLabel, QLineEdit, QMessageBox, QSpinBox, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon
import pyqtgraph as pg
from pyqtgraph import AxisItem
import numpy as np

# Configure PyQTGraph settings
x_axis_labels = ['Win', 'Partial Win', 'Loss'] # X-axis labels for the bar graph

# Function to calculate the cumulative probabilities
def cumulative_probabilities(dice_sides, target_number, max_rolls=10, cache={}):
    # Check if the probability is already in the cache
    if (max_rolls, target_number) in cache:
        return cache[(max_rolls, target_number)]

    # Initialize the probability array
    probabilities = [[0] * (target_number + 1) for _ in range(max_rolls + 1)]

    # Base case: after 1 roll
    for i in range(1, dice_sides + 1):
        if i <= target_number:
            probabilities[1][i] = 1 / dice_sides

    # Dynamic programming: compute probabilities for 2 to max_rolls rolls
    for roll in range(2, max_rolls + 1):
        for total in range(1, target_number + 1):
            for face in range(1, dice_sides + 1):
                if total - face > 0:
                    probabilities[roll][total] += probabilities[roll - 1][total - face] / dice_sides

    # Sum the probabilities for achieving the target in up to max_rolls
    win_probability = sum(probabilities[roll][target_number] for roll in range(1, max_rolls + 1))
    partial_win_probability = 0
    for roll in range(1, max_rolls + 1):
        if 0 < target_number - 1 < len(probabilities[roll]):
            partial_win_probability += probabilities[roll][target_number - 1]
        if 0 < target_number + 1 <= dice_sides and target_number + 1 < len(probabilities[roll]): 
            partial_win_probability += probabilities[roll][target_number + 1]

    # Store the probability in the cache
    cache[(max_rolls, target_number)] = (win_probability, partial_win_probability)

    return win_probability, partial_win_probability

class StringAxis(AxisItem):
    def __init__(self, strings, *args, **kwargs):
        super().__init__(orientation='bottom', *args, **kwargs)  # Add 'orientation' argument here
        self.strings = strings

    def tickStrings(self, values, scale, spacing):
        return [self.strings[int(value)] for value in values]

# Defining the main window class

class App(QWidget):
    def __init__(self):
        super().__init__()
               
        self.title = 'Dice Probability Calculator'
        self.left = 100
        self.top = 100
        
        self.init_ui()                                          # Calling the init_ui function
        self.setWindowTitle(self.title)                         # Setting the window title
        self.setWindowIcon(QIcon("dice.png"))                   # Setting the window icon
        self.setGeometry(self.left, self.top, 400, 300)         # Setting the window geometry
        self.graph_widget = None
        self.show()
        
    # Init GUI
    def init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.dice_combo = QComboBox(self)
        self.dice_combo.addItems(["D4", "D6", "D8", "D10", "D12", "D20"])
        self.dice_combo.currentIndexChanged.connect(self.update_max_value)

        self.target_label = QLabel("Target Number:")
        self.target_input = QLineEdit(self)
        
        self.win_prob_label = QLabel(self)
        self.partial_win_prob_label = QLabel(self)

        self.calculate_btn = QPushButton('Calculate Probabilities', self)
        self.calculate_btn.clicked.connect(self.on_calculate)
        
        self.clear_btn = QPushButton('Clear', self)
        self.clear_btn.clicked.connect(self.on_clear)
        
        self.rolls_spinbox = QSpinBox(self)
        self.rolls_spinbox.setRange(1, 100)  # Adjust range as needed
        self.rolls_spinbox.setValue(10)      # Default to 10 rolls
        self.rolls_spinbox.valueChanged.connect(self.update_max_value)        
        
        self.max_val_label = QLabel("", self)
        
        self.win_payout_input = QLineEdit("2.0", self)  # default value is 2:1 for full win
        self.partial_win_payout_input = QLineEdit("1.0", self)  # default value is 1:1 for partial win
        
        self.bet_input = QLineEdit(self)
        self.bet_input.setPlaceholderText("Enter your bet (Default: $100)")
        
        self.win_payout_label = QLabel("")
        self.partial_win_payout_label = QLabel("")
        
        # Use addRow for QFormLayout with direct string labels
        form_layout.addRow("Select Dice:", self.dice_combo)
        form_layout.addRow("Target Number:", self.target_input)
        form_layout.addRow("Max Rolls:", self.rolls_spinbox)
        form_layout.addRow("Max Possible Value:", self.max_val_label)
        form_layout.addRow("Probability of a Win:", self.win_prob_label)
        form_layout.addRow("Probability of a Partial Win:", self.partial_win_prob_label)
        form_layout.addRow("Win Payout Ratio (e.g., 2.0 for 2:1):", self.win_payout_input)
        form_layout.addRow("Partial Win Payout Ratio (e.g., 1.0 for 1:1):", self.partial_win_payout_input)
        form_layout.addRow("Enter your bet:", self.bet_input)
        form_layout.addRow("Win Payout:", self.win_payout_label)
        form_layout.addRow("Partial Win Payout:", self.partial_win_payout_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.calculate_btn)
        button_layout.addWidget(self.clear_btn)
        
        
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.update_max_value()
        self.setLayout(main_layout)
      
    def update_max_value(self):
        dice_sides = int(self.dice_combo.currentText()[1:])
        max_rolls = self.rolls_spinbox.value()
        max_possible_value = dice_sides * max_rolls
        self.max_val_label.setText(f"{max_possible_value}")

    # Calculate Probabilities
    def on_calculate(self):
        dice_sides = int(self.dice_combo.currentText()[1:])
        target_text = self.target_input.text().strip()
        max_rolls = self.rolls_spinbox.value()
        
        # Check if the target number contains a valid integer
        try:
            target_number = int(target_text)
        except ValueError:
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(f"Error: Please enter a valid integer for the target number.")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec()
            return
        
        # Check if the target number is out of bounds
        if target_number > dice_sides * max_rolls or target_number < dice_sides:
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(f"Error: The target number should be more than the dice size and not exceed the possible bounds for a {dice_sides}-sided dice with a maximum of {max_rolls} rolls.")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec()
            return
        
        win_prob, partial_win_prob = cumulative_probabilities(dice_sides, target_number, max_rolls)
        
        max_possible_value = dice_sides * max_rolls
        self.max_val_label.setText(f"{max_possible_value}")

        if win_prob is None or partial_win_prob is None:
            # Handle the error by showing a message to the user or any other way you see fit
            print("Error: Target number is too high.")
            return

        labels = ["Win", "Partial Win", "Loss"]
        values = [win_prob, partial_win_prob, 1 - (win_prob + partial_win_prob)]
        
        # Display Possible Payout
        if not self.bet_input.text().strip():
            bet = 100.0  # default bet
        else:
            bet = float(self.bet_input.text())
            
        # Retrieve payout ratios from the input fields
        try:
            win_payout_ratio = float(self.win_payout_input.text())
        except ValueError:
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(f"Error: Please enter a valid payout ratio for the win.")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec()
            return
        
        try:
            partial_win_payout_ratio = float(self.partial_win_payout_input.text())
        except ValueError:
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Icon.Critical)
            error_dialog.setText(f"Error: Please enter a valid payout ratio for the partial win.")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec()
            return

        # Calculate potential payouts
        win_payout = bet + bet * win_payout_ratio
        partial_win_payout = bet + bet * partial_win_payout_ratio

        self.win_payout_label.setText(f"${win_payout:.2f}")
        self.partial_win_payout_label.setText(f"${partial_win_payout:.2f}")
        
        # Display the raw probabilities
        self.win_prob_label.setText(f"{win_prob:.6f}")
        self.partial_win_prob_label.setText(f"{partial_win_prob:.6f}")

        # Check if there's an existing graph and remove it
        if self.graph_widget:
            self.layout().removeWidget(self.graph_widget)
            self.graph_widget.deleteLater()
            self.graph_widget = None

        # Creating a PyQtGraph bar graph
        self.graph_widget = pg.PlotWidget(self, title=f'Probabilities for Target Number on a d{dice_sides}', axisItems={'bottom': StringAxis(strings=x_axis_labels)})
        self.graph_widget.setMinimumSize(400, 300) # Adjust the size as needed
        self.graph_widget.setYRange(0,1)  # This sets the y-axis to range from 0 to 1
        
        x_axis = self.graph_widget.getAxis('bottom')
        y_axis = self.graph_widget.getAxis('left')
        
        x_axis.setLabel('Outcome')          # X Axis Label
        y_axis.setLabel('Probability')      # Y Axis Label

        self.graph_widget.setBackground('w')
        self.graph_widget.setTitle(f'Probabilities for Target Number on a d{dice_sides}')
        self.graph_widget.setYRange(0, 1)
        
        viewbox = self.graph_widget.getViewBox()
        viewbox.setLimits(yMin=0, yMax=1)
        
        bar_width = 0.6
        bg1 = pg.BarGraphItem(x=np.array([0]), height=[values[0]], width=bar_width, brush='g', name='Win')
        bg2 = pg.BarGraphItem(x=np.array([1]), height=[values[1]], width=bar_width, brush='y', name='Partial Win')
        bg3 = pg.BarGraphItem(x=np.array([2]), height=[values[2]], width=bar_width, brush='r', name='Loss')

        self.graph_widget.addItem(bg1)
        self.graph_widget.addItem(bg2)
        self.graph_widget.addItem(bg3)

        self.layout().addWidget(self.graph_widget)
        self.adjustSize()
            
    def on_clear(self):
        if self.graph_widget:
            self.layout().removeWidget(self.graph_widget)
            self.graph_widget.deleteLater()
            self.graph_widget = None
        self.target_input.clear()
        self.adjustSize()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
