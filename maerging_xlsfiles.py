import pandas as pd
import os


dir_name = 'excel_files'
filepaths = os.listdir(dir_name)
dir_path = os.path

file_2024 = [str_2024 for str_2024 in filepaths if "2024" in str_2024]
file_2025 = [str_2025 for str_2025 in filepaths if "2025" in str_2025]

access_to_files2024 = [dir_path.join(dir_name, filepath_2024) for filepath_2024 in file_2024] ## vytvoří adresy k souborům// 1. filepaths je cesta ke složce se soubory 2. požadované filepath je název souboru 3. join() sloučí názvy
access_to_files2025 = [dir_path.join(dir_name, filepath_2025) for filepath_2025 in file_2025]

read_excel2024 = [pd.read_excel(filepath2024) for filepath2024 in access_to_files2024]
mergefiles_2024 = pd.concat(read_excel2024, ignore_index=True)

read_excel2025 = [pd.read_excel(filepath2025) for filepath2025 in access_to_files2025]
mergefiles_2025 = pd.concat(read_excel2025, ignore_index=True)

mergefiles_2024.to_excel("2024.xlsx", index=False)
mergefiles_2025.to_excel("2025.xlsx", index=False)

