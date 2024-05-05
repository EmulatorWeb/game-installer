import sys
import os
import json
from shutil import copyfile
from PIL import Image
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

# Define supported devices
devices = ["DS", "GBA"]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create and initialize labels
        self.rom_path_label = QLabel("No ROM selected")
        self.public_folder_label = QLabel("No public folder selected")
        self.cover_image_label = QLabel("No cover image selected")

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

        layout.addWidget(self.cover_image_label)
        cover_image_button = QPushButton("Select Cover Image")
        cover_image_button.clicked.connect(self.select_cover_image)
        layout.addWidget(cover_image_button)

        layout.addWidget(submit_button)

        self.setLayout(layout)

        self.setWindowTitle("EmulatorWeb Game Installer")

    def select_rom(self):
        self.rom_path = filedialog.askopenfilename(filetypes=[("All files", "*")])
        if self.rom_path:
            self.rom_path_label.setText(os.path.basename(self.rom_path))

    def select_cover_image(self):
        self.cover_image_path = filedialog.askopenfilename(title="Select Cover Image")
        if self.cover_image_path:
            # Convert the image to PNG if needed and rename it to "cover.png"
            converted_image_path = os.path.join(os.path.dirname(self.cover_image_path), "cover.png")
            if self.cover_image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # If the image is already in PNG format or a supported format, copy it to the destination folder
                copyfile(self.cover_image_path, converted_image_path)
            else:
                # Convert the image to PNG
                with Image.open(self.cover_image_path) as img:
                    img.save(converted_image_path, "PNG")
            self.cover_image_label.setText("cover.png")

    def copy_file_to_folder(self, file_path, folder_path):
        if file_path:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(folder_path, file_name)
            copyfile(file_path, destination_path)

    def get_game_name(self, game_name_entry):
        return game_name_entry.text()

    def get_device(self, device_dropdown):
        return device_dropdown.currentText()

    def select_public_folder(self):
        self.public_folder_path = filedialog.askdirectory(title="Select Public Folder")
        if self.public_folder_path:
            self.public_folder_label.setText(self.public_folder_path)

    def submit_info(self, game_name_entry, device_dropdown):
        game_name = self.get_game_name(game_name_entry)
        device = self.get_device(device_dropdown)

        # Validate input
        if not self.rom_path or not self.public_folder_path:
            print("Please select both a ROM file and a public folder.")
            return

        # Get next available folder ID
        folder_path = os.path.join(self.public_folder_path, "rom", device)
        folder_id = 1
        while os.path.isdir(os.path.join(folder_path, str(folder_id))):
            folder_id += 1

        # Create the folder
        os.makedirs(os.path.join(folder_path, str(folder_id)), exist_ok=True)

        # Copy the ROM file to the destination folder
        self.copy_file_to_folder(self.rom_path, os.path.join(folder_path, str(folder_id)))

        # Copy the cover image if selected
        self.copy_file_to_folder(os.path.join(os.path.dirname(self.cover_image_path), "cover.png"), os.path.join(folder_path, str(folder_id)))

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