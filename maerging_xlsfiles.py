import pandas as pd
import os
import openpyxl

dir_name = 'excel_files'
filepaths = os.listdir(dir_name)
dir_path = os.path

access_to_files = [dir_path.join(dir_name, filepath) for filepath in filepaths] ## vytvoří adresy k souborům// 1. filepaths je cesta ke složce se soubory 2. požadované filepath je název souboru 3. join() sloučí názvy

