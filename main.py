import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from tkinter import filedialog
import os
import json

# Define supported devices
devices = ["DS", "GBA"]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create and initialize labels
        self.rom_path_label = QLabel("No ROM selected")
        self.public_folder_label = QLabel("No public folder selected")

        # Create other UI elements
        game_name_label = QLabel("Game Name:")
        game_name_entry = QLineEdit()

        device_label = QLabel("Device:")
        device_dropdown = QComboBox()
        device_dropdown.addItems(devices)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_info(game_name_entry, device_dropdown))  # Pass both

        # Create layout
        layout = QVBoxLayout()

        # Add widgets to the layout
        layout.addWidget(self.rom_path_label)
        rom_path_button = QPushButton("Select ROM")
        rom_path_button.clicked.connect(self.select_rom)
        layout.addWidget(rom_path_button)

        layout.addWidget(game_name_label)
        layout.addWidget(game_name_entry)

        layout.addWidget(device_label)
        layout.addWidget(device_dropdown)

        layout.addWidget(self.public_folder_label)
        public_folder_button = QPushButton("Select Public Folder")
        public_folder_button.clicked.connect(self.select_public_folder)
        layout.addWidget(public_folder_button)

        layout.addWidget(submit_button)

        self.setLayout(layout)

        self.setWindowTitle("EmulatorWeb Game Installer")

    def select_rom(self):
        filename = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.rom_path_label.setText(filename)

    def get_game_name(self, game_name_entry):
        return game_name_entry.text()

    def get_device(self, device_dropdown):
        return device_dropdown.currentText()

    def select_public_folder(self):
        public_folder_path = filedialog.askdirectory(title="Select Public Folder")
        self.public_folder_label.setText(public_folder_path)

    def submit_info(self, game_name_entry, device_dropdown):
        rom_path = self.rom_path_label.text()
        game_name = self.get_game_name(game_name_entry)
        device = self.get_device(device_dropdown)
        public_folder = self.public_folder_label.text()

        # Validate input
        if not rom_path or not public_folder:
            print("Please select both a ROM file and a public folder.")
            return

        # Get next available folder ID
        folder_path = os.path.join(public_folder, "rom", device)
        folder_id = 1
        while os.path.isdir(os.path.join(folder_path, str(folder_id))):
            folder_id += 1

        # Create the folder
        os.makedirs(os.path.join(folder_path, str(folder_id)))

        # Extract game name and extension from ROM filename
        rom_basename, rom_extension = os.path.splitext(os.path.basename(rom_path))

        # Create the new ROM filename
        new_rom_filename = f"{device}{folder_id}{rom_extension}"

        # Move the ROM file
        os.rename(rom_path, os.path.join(folder_path, str(folder_id), new_rom_filename))

        # Create config.json
        config_data = {"name": game_name}
        with open(os.path.join(folder_path, str(folder_id), "config.json"), "w") as f:
            json.dump(config_data, f)

        print(f"Game installed successfully to folder {folder_id} in {device} category.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
