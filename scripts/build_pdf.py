from pdf_exporter.export_pdf import ExportPdf
import time
import argparse

def analyse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site_url", help="The url of the site", required=True)
    parser.add_argument("--municipalite", help="The name of the municipality", required=True)
    parser.add_argument("--directory", help="The directory of the data", required=True)
    parser.add_argument("--export_file_name", help="The name of the file to export")
    return parser.parse_args()

if __name__ == "__main__":
    args = analyse_arguments()
    site_url = args.site_url
    municipalite = args.municipalite 
    directory = args.directory
    export_file_name= args.export_file_name if args.export_file_name else "output.pdf"
    start_time = time.time()
    ExportPdf(directory, export_file_name, site_url, municipalite).export_pdf()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time required: {elapsed_time} seconds")
