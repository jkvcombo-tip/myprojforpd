import os
import csv

def convert_all_to_csv(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
            convert_to_csv(input_file, output_file)

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='replace') as infile:
        lines = infile.readlines()

    csv_data = [line.strip() for line in lines]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
        csv_writer.writerow(['Timestamp', 'Log Message'])  # Replace with actual column names

        for line in csv_data:
            try:
                # Assuming your syslog format, you may need to adjust this based on your actual syslog format
                timestamp, log_message = line.split(' ', 1)
                csv_writer.writerow([timestamp, log_message])
            except ValueError:
                # Handle cases where the line cannot be split into timestamp and log message
                print(f"Error processing line in {input_file}: {line}")

    print(f"Conversion completed. CSV file saved to {output_file}")

if __name__ == "__main__":
    syslog_folder = './SYSLOG/END DEVICE/'
    csv_output_folder = './SYSLOG/END DEVICE/'

    convert_all_to_csv(syslog_folder, csv_output_folder)
