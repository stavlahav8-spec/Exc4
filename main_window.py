import os
import subprocess
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from about_window import AboutWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''
        self.setWindowTitle("Student Grade Correction")

        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.load_file_button = QPushButton("Load Grades File")
        self.load_file_button.clicked.connect(self.on_load_file)
        main_layout.addWidget(self.load_file_button)

        self.table = QTableWidget(50, 3, self)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        main_layout.addWidget(self.table)

        bonus_layout = QHBoxLayout()
        bonus_layout.addWidget(QLabel("Bonus points:"))
        self.bonus_input = QSpinBox(self)
        self.bonus_input.setRange(-999999, 999999)
        self.bonus_input.editingFinished.connect(self.on_bonus_entered)
        bonus_layout.addWidget(self.bonus_input)
        main_layout.addLayout(bonus_layout)

        buttons_layout = QHBoxLayout()
        self.update_file_button = QPushButton("Update File")
        self.update_file_button.clicked.connect(self.on_update_file)
        buttons_layout.addWidget(self.update_file_button)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        buttons_layout.addWidget(self.about_button)
        main_layout.addLayout(buttons_layout)

        style_path = os.path.join(os.path.dirname(__file__), "style.qss")
        with open(style_path, encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

    def on_load_file(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Load Grades File",
            "",
            "CSV files (*.csv);;All files (*)",
        )
        if filepath:
            self.selected_file = filepath
            self.student_ids.clear()
            self.original_grades.clear()
            self.corrected_grades.clear()

            with open(self.selected_file, 'r') as f:
                next(f)
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        self.student_ids.append(parts[0])
                        self.original_grades.append(int(parts[1]))
                        self.corrected_grades.append(int(parts[1]))

            self.update_table()
            
    def update_table(self) -> None:
        self.table.clearContents()
        self.table.setRowCount(50)

        for row, values in enumerate(
            zip(self.student_ids, self.original_grades, self.corrected_grades)
        ):
            if row >= self.table.rowCount():
                break
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))

    def on_bonus_entered(self) -> None:
        bonus_points = self.bonus_input.value()
        # TODO: Update self.corrected_grades using bonus_points, then call
        # self.update_table().

    def on_update_file(self) -> None:
        if not self.selected_file:
            QMessageBox.warning(self, "No file selected", "Load a grades file first.")
            return

        # TODO: Overwrite self.selected_file with the updated CSV data.
        self.open_file_cross_platform(self.selected_file)

    def open_file_cross_platform(self, filepath: str) -> None:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Grades file does not exist: {filepath}")

        if sys.platform == "win32":
            os.startfile(filepath)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", filepath])
        else:
            subprocess.Popen(["xdg-open", filepath])

    def show_about(self) -> None:
        self.about_window = AboutWindow(self)
        self.about_window.exec()


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
