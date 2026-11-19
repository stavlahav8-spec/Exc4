from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class AboutWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("About")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Stav Lahav"))
        layout.addWidget(
            QLabel(
                "Course: [Course Name]\n"
                "Assignment: Exercise 4 - Student Grade-Correction Tool"
            )
        )

        repository_link = QLabel(
            '<a href="https://github.com/USERNAME/REPO_NAME">'
            "GitHub repository</a>"
        )
        repository_link.setOpenExternalLinks(True)
        layout.addWidget(repository_link)
