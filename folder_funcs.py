# File created by: Liam Newberry
import datetime
import os
import shutil

from app_settings import *



def create_bank_event_dict(year:int,month:int,day:int,destination:str,
                           dollars:float):
    return {"year":year,
            "month":month,
            "day":day,
            "destination":destination,
            "dollars":dollars}

def create_text_file_dict(bank_history:list,stock_history:list,interactions_left:int):
    now = datetime.datetime.now()
    text_file_dict = {"bank history":bank_history,
                      "stock history":stock_history,
                      "month end":{"year":now.year,
                                   "month":now.month,
                                   "interactions left":interactions_left},
                      "last update":{"year":now.year,
                                     "month":now.month,
                                     "day":now.day}}
    return text_file_dict

def create_text_file_folder():
    if os.path.exists(TEXT_FILE_FOLDER_PATH):
        for file in os.scandir(TEXT_FILE_FOLDER_PATH):
            os.remove(file)
    else:
        os.makedirs(TEXT_FILE_FOLDER_PATH)

def create_stock_event_dict(year:int,month:int,day:int,type:str,
                            ticker:str,dollars:float,shares:float):
    return {"year":year,
            "month":month,
            "day":day,
            "type":type,
            "ticker":ticker,
            "dollars":dollars,
            "shares":shares}

def move_text_files(text_file_dict):
    create_text_file_folder()
    for item in text_file_dict:
        shutil.move(CURRENT_PATH + "\\" + item, TEXT_FILE_FOLDER_PATH )

def read_bank_history_file():
    bank_history = []
    with open(TEXT_FILE_FOLDER_PATH + "\\bank history","r") as file:
        content = file.readlines()
        for i in range(0,int(len(content)/5)):
            dictionary = create_bank_event_dict(int(content[i*5][:-1]),
                                                int(content[i*5+1][:-1]),
                                                int(content[i*5+2][:-1]),
                                                content[i*5+3][:-1],
                                                float(content[i*5+4]))
            bank_history.append(dictionary)
    file.close()
    return bank_history

def read_text_files():
    bank_history = read_bank_history_file()
    stock_history = read_stock_history_file()
    month_end = read_month_end_file()
    last_update = read_last_update_file()
    return bank_history,stock_history,month_end,last_update

def read_last_update_file():
    with open(TEXT_FILE_FOLDER_PATH + "\\last update","r") as file:
        content = file.readlines()
        last_update = {"year":int(content[0][:-1]),
                       "month":int(content[1][:-1]),
                       "day":int(content[2])}
    file.close()
    return last_update
        

def read_month_end_file():
    with open(TEXT_FILE_FOLDER_PATH + "\\last update","r") as file:
        content = file.readlines()
        month_end = {"year":int(content[0][:-1]),
                     "month":int(content[1][:-1]),
                     "interactions left":int(content[2])}
    file.close()
    return month_end

def read_stock_history_file():
    stock_history = []
    with open(TEXT_FILE_FOLDER_PATH + "\\stock history","r") as file:
        content = file.readlines()
        for i in range(0,int(len(content)/7)):
            dictionary = create_stock_event_dict(int(content[i*7][:-1]),
                                                 int(content[i*7+1][:-1]),
                                                 int(content[i*7+2][:-1]),
                                                 content[i*7+3][:-1],
                                                 content[i*7+4][:-1],
                                                 float(content[i*7+5][:-1]),
                                                 float(content[i*7+6]))
            stock_history.append(dictionary)
    file.close()
    return stock_history

def write_bank_history_file(history:list):
    with open("bank history","w") as file:
        for dictionary in history:
            for item in dictionary:
                file.write(str(dictionary[item]) + "\n")
    file.close()
    pass

def write_text_files(text_file_dict:dict):
    write_bank_history_file(text_file_dict["bank history"])
    write_stock_history_file(text_file_dict["stock history"])
    write_month_end_file(text_file_dict["month end"])
    write_last_update_file(text_file_dict["last update"])
    move_text_files(text_file_dict)

def write_last_update_file(date:dict):
    with open("last update","w") as file:
        file.write(str(date["year"]) + "\n")
        file.write(str(date["month"]) + "\n")
        file.write(str(date["day"]))
    file.close()

def write_month_end_file(data:dict):
    with open("month end","w") as file:
        file.write(str(data["year"]) + "\n")
        file.write(str(data["month"]) + "\n")
        file.write(str(data["interactions left"]))
    file.close()
                
def write_stock_history_file(history:list):
    with open("stock history","w") as file:
        for dictionary in history:
            for item in dictionary:
                file.write(str(dictionary[item]) + "\n")
    file.close()

# TEST EXAMPLE {
# bh1 = create_bank_event_dict(2007,2,24,"checkings",76686.23)
# sh1 = create_stock_event_dict(1992,3,6,"sell","TSLA",988.23,2.3)
# text_file_dict = create_text_file_dict([bh1,bh1,bh1],[sh1,sh1,sh1],3)

# write_text_files(text_file_dict)

# bh,sh,me,lu = read_text_files()
# print("BH")
# for item in bh:
#     print(item)
# print("SH")
# for item in sh:
#     print(item)
# print("ME")
# for item in me:
#     print(me[item])
# print("LU")
# for item in lu:
#     print(lu[item])
# }