import os
import logging
import csv
from typing import Optional, List, Tuple
import statistics
import pydicom
from pydicom.data import get_testdata_files
from PIL import Image
import numpy as np


class FileProcessor:
    def __init__(self, base_path: str, log_file: str):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

        # Configuración del logger
        logging.basicConfig(
            filename=log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger()

    def list_folder_contents(self, folder_name: str, details: bool = False) -> None:
        folder_path = os.path.join(self.base_path, folder_name)

        if not os.path.exists(folder_path):
            self.logger.error(f"Folder not found: {folder_path}")
            print(f"Error: Folder '{folder_name}' does not exist.")
            return

        elements = os.listdir(folder_path)
        print(f"Folder: {folder_path}")
        print(f"Number of elements: {len(elements)}")

        for element in elements:
            element_path = os.path.join(folder_path, element)
            if os.path.isdir(element_path):
                info = "(Folder)"
            else:
                info = "(File)"

            if details and os.path.isfile(element_path):
                size_mb = os.path.getsize(element_path) / (1024 * 1024)
                modified_time = os.path.getmtime(element_path)
                print(
                    f" - {element} {info} ({size_mb:.2f} MB, Last Modified: {modified_time})")
            else:
                print(f" - {element} {info}")

    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False) -> None:
        file_path = os.path.join(self.base_path, filename)

        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            print(f"Error: File '{filename}' does not exist.")
            return

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                if not rows:
                    print("The CSV file is empty.")
                    return

                print(f"Columns: {reader.fieldnames}")
                print(f"Rows: {len(rows)}")

                numeric_columns = {col: [] for col in reader.fieldnames if rows[0][col].replace(
                    '.', '', 1).isdigit()}

                for row in rows:
                    for col in numeric_columns:
                        try:
                            numeric_columns[col].append(float(row[col]))
                        except ValueError:
                            self.logger.error(
                                f"Non-numeric data found in column: {col}")

                for col, values in numeric_columns.items():
                    if values:
                        avg = statistics.mean(values)
                        std_dev = statistics.stdev(
                            values) if len(values) > 1 else 0
                        print(
                            f" - {col}: Average = {avg:.2f}, Std Dev = {std_dev:.2f}")

                if report_path:
                    report_file = os.path.join(
                        report_path, f"{os.path.splitext(filename)[0]}_report.txt")
                    with open(report_file, 'w') as report:
                        for col, values in numeric_columns.items():
                            if values:
                                avg = statistics.mean(values)
                                std_dev = statistics.stdev(
                                    values) if len(values) > 1 else 0
                                report.write(f"{col}: Average = {
                                             avg:.2f}, Std Dev = {std_dev:.2f}\n")
                    print(f"Saved summary report to {report_file}")

                if summary:
                    for col in reader.fieldnames:
                        if col not in numeric_columns:
                            unique_values = {row[col]: 0 for row in rows}
                            for row in rows:
                                unique_values[row[col]] += 1
                            print(
                                f" - {col}: Unique Values = {len(unique_values)}, Frequencies = {unique_values}")

        except Exception as e:
            self.logger.error(f"Error reading CSV file: {e}")

    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> None:
        file_path = os.path.join(self.base_path, filename)

        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            print(f"Error: File '{filename}' does not exist.")
            return

        try:
            dicom_data = pydicom.dcmread(file_path)

            print(f"Patient Name: {dicom_data.get('PatientName', 'N/A')}")
            print(f"Study Date: {dicom_data.get('StudyDate', 'N/A')}")
            print(f"Modality: {dicom_data.get('Modality', 'N/A')}")

            if tags:
                for tag in tags:
                    try:
                        value = dicom_data.get(tag, 'N/A')
                        print(f"Tag {tag}: {value}")
                    except Exception as e:
                        self.logger.error(f"Error retrieving tag {tag}: {e}")

            if extract_image:
                if hasattr(dicom_data, 'pixel_array'):
                    image_data = dicom_data.pixel_array
                    img = Image.fromarray(image_data)
                    png_file = os.path.join(
                        self.base_path, f"{os.path.splitext(filename)[0]}.png")
                    img.save(png_file)
                    print(f"Extracted image saved to {png_file}")
                else:
                    self.logger.error("No pixel data found in DICOM file.")
                    print("Error: No pixel data found in DICOM file.")

        except Exception as e:
            self.logger.error(f"Error reading DICOM file: {e}")
            print(f"Error reading DICOM file: {e}")
