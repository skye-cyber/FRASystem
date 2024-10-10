import os
import sys
from datetime import datetime
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook


class A_LOGGER:
    def __init__(self):
        self = self
        self.csv_path = os.path.join(Path(__file__).resolve().parent.parent.parent, 'media/enrollments/attendance.csv')

    def log_attendance(self, name):
        try:

            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path)

            else:

                # Create an empty DataFrame if file doesn't exist
                df = pd.DataFrame(
                    columns=['Name', 'Timestamp'])

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_entry = {'Name': name, 'Timestamp': timestamp}

            # concatenate new_entry to the csv

            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

            # Alternatively

            # df.loc[len(df)] = new_entry

            df.to_csv(self.csv_path, index=False)

            # Print the csv content

            # print(df.head())

        except pd.errors.EmptyDataError:
            print(
                f"\033[31mError: The file \033[36m'{self.csv_path}'\033[31m is empty or contains no data.\033[0m")

        except FileNotFoundError:
            print(
                f"\033[31mError: The file \033[36m'{self.csv_path}'\033[31m was not found.\033[0m")

        except Exception as e:
            print(f"\033[31mError: {str(e)}\033[0m")

    def export_xlsx(self):  # Requires openpyxl
        '''# Write multiple DataFrames to different sheets in the same Excel file
        excel_file_path = 'path_to_your_excel_file.xlsx'
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            df1.to_excel(writer, sheet_name='Sheet1', index=False)
        df2.to_excel(writer, sheet_name='Sheet2', index=False)
        '''
        try:
            excel_file_path = f'{self.csv_path[:-3]}xlsx'

            # Read the CSV file into a DataFrame
            df = pd.read_csv(self.csv_path)

            # Write the DataFrame to an Excel file
            df.to_excel(excel_file_path, index=False, engine='openpyxl')

            # Load the workbook and the sheet
            workbook = load_workbook(excel_file_path)
            sheet = workbook.active

            # Adjust column widths
            print("Adjust columns")
            for column in sheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except Exception:
                        pass

                adjusted_width = (max_length + 2)
                sheet.column_dimensions[column_letter].width = adjusted_width

            # Save the workbook
            workbook.save(excel_file_path)
            print(
                f"\033[1:36mCSV file '{self.csv_path}' has been converted to Excel file '{excel_file_path}' with adjusted column widths.\033[0m")

        except KeyboardInterrupt:
            print("Quit")
            sys.exit(1)

        except KeyError:
            print("KeyError")

        except Exception as e:
            print(f"\033[32m{e}\033[0m")
