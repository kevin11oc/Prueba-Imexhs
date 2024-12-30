from fileManagment import FileProcessor

def main():
    processor = FileProcessor(base_path="./data", log_file="./errors.log")

    # Listar contenido de la carpeta
    print("\n=== List Folder Contents ===")
    processor.list_folder_contents(folder_name="test_folder", details=True)

    # Analizar un archivo CSV
    print("\n=== Analyze CSV File ===")
    processor.read_csv(
        filename="sample-01-csv.csv",
        report_path="./data/reports",
        summary=True
    )

    # Analizar un archivo DICOM
    print("\n=== Analyze DICOM File ===")
    processor.read_dicom(
        filename="sample-01-dicom.dcm",
        tags=[(0x0010, 0x0010), (0x0008, 0x0060)],
        extract_image=True
    )

if __name__ == "__main__":
    main()
