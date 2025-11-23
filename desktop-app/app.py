import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QListWidget, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- CONFIG ---
TOKEN = "6a5788d528d4768b63df56c2911f500879bedab7"
BASE_URL = "http://127.0.0.1:8000/api"

HEADERS = {"Authorization": f"Token {TOKEN}"}
NUMERIC_COLUMNS = ['Flowrate', 'Pressure', 'Temperature']

# --- HELPER FUNCTIONS ---
def save_pdf(dataset_name, row_count, averages, type_dist, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Dataset Report: {dataset_name}")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Total Rows: {row_count}")
    y -= 30

    c.drawString(50, y, "Averages:")
    y -= 20
    if averages:
        for k, v in averages.items():
            c.drawString(60, y, f"{k}: {v:.2f}")
            y -= 20
    else:
        c.drawString(60, y, "No numeric data found")
        y -= 20

    c.drawString(50, y, "Type Distribution:")
    y -= 20
    if type_dist:
        for k, v in type_dist.items():
            c.drawString(60, y, f"{k}: {v}")
            y -= 20
    else:
        c.drawString(60, y, "No type data found")
        y -= 20

    c.save()


# --- MAIN APP ---
class ChemicalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Upload CSV
        self.upload_label = QLabel(
            "Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
        )
        self.layout.addWidget(self.upload_label)
        self.upload_btn = QPushButton("Select & Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.upload_btn)

        # History
        self.history_label = QLabel("Last 5 Datasets:")
        self.layout.addWidget(self.history_label)
        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)
        self.history_list.itemClicked.connect(self.view_dataset)

        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.clicked.connect(self.load_history)
        self.layout.addWidget(self.refresh_btn)

        # Summary Table
        self.summary_table = QTableWidget()
        self.layout.addWidget(self.summary_table)

        # Chart Canvas
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Download PDF
        self.pdf_btn = QPushButton("Download PDF of Selected Dataset")
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.layout.addWidget(self.pdf_btn)

        # Load initial history
        self.load_history()
        self.current_dataset = None

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                res = requests.post(f"{BASE_URL}/upload/", headers=HEADERS, files=files)
            if res.status_code == 201:
                QMessageBox.information(self, "Success", "Upload Successful!")
                self.load_history()
            else:
                QMessageBox.warning(self, "Failed", f"Upload Failed! {res.json()}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_history(self):
        try:
            res = requests.get(f"{BASE_URL}/history/", headers=HEADERS)
            if res.status_code != 200:
                QMessageBox.warning(self, "Error", f"Could not fetch history! {res.text}")
                return
            self.history_list.clear()
            self.datasets = res.json()
            for d in self.datasets:
                self.history_list.addItem(f"{d['id']} - {d['original_filename']} ({d['row_count']} rows)")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def view_dataset(self, item):
        idx = self.history_list.currentRow()
        dataset = self.datasets[idx]
        self.current_dataset = dataset

        try:
            res = requests.get(f"{BASE_URL}/datasets/{dataset['id']}/", headers=HEADERS)
            if res.status_code != 200:
                QMessageBox.warning(self, "Error", f"Could not fetch dataset! {res.text}")
                return
            df_res = res.json()
            summary = df_res.get('summary', {})
            averages = summary.get('averages', {})
            type_dist = summary.get('type_distribution', {})

            # Display in table
            self.summary_table.clear()
            headers = ["Metric", "Value"]
            self.summary_table.setColumnCount(2)
            self.summary_table.setRowCount(len(averages) + len(type_dist) + 1)
            self.summary_table.setHorizontalHeaderLabels(headers)

            row = 0
            self.summary_table.setItem(row, 0, QTableWidgetItem("Total Rows"))
            self.summary_table.setItem(row, 1, QTableWidgetItem(str(dataset['row_count'])))
            row += 1

            for k, v in averages.items():
                self.summary_table.setItem(row, 0, QTableWidgetItem(f"Avg {k}"))
                self.summary_table.setItem(row, 1, QTableWidgetItem(f"{v:.2f}" if v is not None else "N/A"))
                row += 1

            for k, v in type_dist.items():
                self.summary_table.setItem(row, 0, QTableWidgetItem(f"Type: {k}"))
                self.summary_table.setItem(row, 1, QTableWidgetItem(str(v)))
                row += 1

            # Draw charts inside canvas
            self.figure.clear()
            ax1 = self.figure.add_subplot(121)
            if averages:
                ax1.bar(averages.keys(), averages.values(), color='skyblue')
                ax1.set_title("Numeric Averages")
            ax2 = self.figure.add_subplot(122)
            if type_dist:
                ax2.bar(type_dist.keys(), type_dist.values(), color='orange')
                ax2.set_title("Type Distribution")
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def download_pdf(self):
        if not self.current_dataset:
            QMessageBox.warning(self, "Error", "Please select a dataset first!")
            return

        dataset = self.current_dataset
        try:
            res = requests.get(f"{BASE_URL}/datasets/{dataset['id']}/", headers=HEADERS)
            if res.status_code != 200:
                QMessageBox.warning(self, "Error", f"Could not fetch dataset! {res.text}")
                return
            df_res = res.json()
            summary = df_res.get('summary', {})
            averages = summary.get('averages', {})
            type_dist = summary.get('type_distribution', {})

            file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", f"{dataset['original_filename']}.pdf", "PDF Files (*.pdf)")
            if file_path:
                save_pdf(dataset['original_filename'], dataset['row_count'], averages, type_dist, file_path)
                QMessageBox.information(self, "Success", f"PDF saved to {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# --- RUN APP ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChemicalApp()
    window.show()
    sys.exit(app.exec_())
