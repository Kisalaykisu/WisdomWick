import win32com.client
import pandas as pd
import os



# Modify the example usage to prompt for associate ID
while True:
    associate_id = input("Enter the associate's email ID (or type 'exit' to quit): ")
    if associate_id.lower() == 'exit':
        break
def get_exchange_user_reportees(email_address, max_level=100):
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        recipient = outlook.CreateRecipient(email_address)
        recipient.Resolve()
        if recipient.Resolved:
            exchange_user = recipient.AddressEntry.GetExchangeUser()
            if exchange_user:
                reportees = get_direct_reports(exchange_user, level=0, max_level=max_level)
                return reportees
    except Exception as e:
        print(f"Error fetching reportees: {e}")
    return []

def get_direct_reports(exchange_user, level, max_level, reportees=[]):
    if level < max_level:
        direct_reports = exchange_user.GetDirectReports()
        if direct_reports:
            for report in direct_reports:
                user = report.GetExchangeUser()
                if user:
                    reportees.append(user.Alias)
                    get_direct_reports(user, level+1, max_level, reportees)
    return reportees

def read_reportee_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        reportee_ids = [line.strip() for line in file if line.strip()]
    return reportee_ids


def write_reportees_to_excel(reportees, excel_file_path):
    try:
        df = pd.DataFrame(reportees, columns=['ReporteeID'])
        #writer = pd.ExcelWriter(excel_file_path, engine='openpyxl')
        df.to_excel(excel_file_path, sheet_name='Sheet1', index=False)
    except Exception as e:
        print(f"Error writing to Excel: {e}")

def open_excel_file(path):
    os.startfile(path)  
    
          
# Dummy reportee IDs
reportees = ['ID001', 'ID002', 'ID003', 'ID004', 'ID005','ID005','ID005']  
print(reportees)  # Add this line before calling write_reportees_to_excel
      

# Example usage
associate_id = 'pixiebillucool@outlook.com'  # Replace this with the actual associate's email ID
#reportees = get_exchange_user_reportees(associate_id)
excel_file_path = "C:/Users/Kisalay/Downloads/Kisalay.xlsx"
#print("Reportees to be written to Excel:", reportees)
write_reportees_to_excel(reportees, excel_file_path)

# Open the Excel file
open_excel_file(excel_file_path)

# After breaking out of the loop, you can print the path or do other cleanup if necessary
print(f"The Excel file is available at: {excel_file_path}")
# Return the path to the Excel file for download
excel_file_path

