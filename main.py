# ----- موتور جستجوی کد آیدیکد -----
from pathlib import Path
import sys

# گرفتن کلمه و مسیر پوشه از کاربر برای جستجو
word = input("\033[34mEnter a word: \033[0m")
directory = Path(input("\033[34mEnter a directory (folder): \033[0m"))

# مدیریت خطاهای ممکن در مسیر ورودی
if not directory.exists():
    print("\n\033[31mERROR: FOLDER NOT FOUND!\033[0m")
    sys.exit()

if not directory.is_dir():
    print("\n\033[31mERROR: PATH IS NOT A DIRECTORY!\033[0m")
    sys.exit()


# دریافت لیست همه فایل ها در دایرکتوری و زیرپوشه هایش
files = [str(f.resolve()) for f in directory.rglob("*") if f.is_file()]

# جدا کردن فایل های کدنویسی مختلف
cpp_files = [file for file in files if (file.endswith(".cpp"))]
py_files = [file for file in files if (file.endswith(".py"))]
c_files = [file for file in files if (file.endswith(".c"))]
h_files = [file for file in files if (file.endswith(".h"))]

# چاپ تعداد فایل های درحال پردازش
number_of_files = len(cpp_files) + len(py_files) + len(c_files) + len(h_files)
print(f"\n\033[33mAnalyzing {number_of_files} files...\033[0m")

# پردازش فایل ها و بدست آوردن تعداد خطوط، کلاس ها، توابع و نتیجه جستجو
classes = []
functions = []
search_result = []
total_lines = 0

# پردازش فایل های C++
for file in cpp_files:

    with open(file, "r") as f:
        lines = f.readlines()

    total_lines += len(lines)
    for i in range(0, len(lines)):
        # تمیز کردن خط
        lines[i] = lines[i].strip()
        # جستجوی کلمه
        word_count_in_line = lines[i].count(word)
        if (word_count_in_line > 0):
            search_result.append(f"{file}:{i+1}")
        
        # بررسی وجود تابع
        if ("(" in lines[i] and ")" in lines[i]):
            left = lines[i].split("(")[0]
            name = left.split()[-1]
            if (name not in ("for", "while", "switch", "if", "catch")):
                functions.append(f"{name}() in {file} line {i+1}")
        # بررسی وجود کلاس
        line_tokens = lines[i].split()
        if (len(line_tokens) > 1):
            if (line_tokens[0] == "class"):
                classes.append(f"{line_tokens[1].replace("{", "").replace(":", "")} in {file} line {i+1}")

# پردازش فایل های پایتون
for file in py_files:

    with open(file, "r") as f:
        lines = f.readlines()

    total_lines += len(lines)
    for i in range(0, len(lines)):
        # تمیز کردن خط
        lines[i] = lines[i].strip()
        # جستجوی کلمه
        word_count_in_line = lines[i].count(word)
        if (word_count_in_line > 0):
            search_result.append(f"{file}:{i+1}")
            line_tokens = lines[i].split()

            if (len(line_tokens) > 1):
                # بررسی وجود تابع
                if (line_tokens[0] == "def"):
                    functions.append(f"{line_tokens[1].split("(")[0]}() in {file} line {i+1}")
                # بررسی وجود کلاس
                if (line_tokens[0] == "class"):
                    classes.append(f"{line_tokens[1].replace(":", "")} in {file} line {i+1}")

# پردازش فایل های C (سی کلاس ندارد)
for file in c_files:

    with open(file, "r") as f:
        lines = f.readlines()

    total_lines += len(lines)
    for i in range(0, len(lines)):
        # تمیز کردن خط
        lines[i] = lines[i].strip()
        # جستجوی کلمه
        word_count_in_line = lines[i].count(word)
        if (word_count_in_line > 0):
            search_result.append(f"{file}:{i+1}")
            line_tokens = lines[i].split()

        # بررسی وجود تابع
        if ("(" in lines[i] and ")" in lines[i]):
            left = lines[i].split("(")[0]
            name = left.split()[-1]
            if (name not in ("for", "while", "switch", "if", "catch")):
                functions.append(f"{name}() in {file} line {i+1}")

# پردازش فایل های هدر کتابخانه سی
for file in h_files:

    with open(file, "r") as f:
        lines = f.readlines()

    total_lines += len(lines)
    for i in range(0, len(lines)):
        # تمیز کردن خط
        lines[i] = lines[i].strip()
        # جستجوی کلمه
        word_count_in_line = lines[i].count(word)
        if (word_count_in_line > 0):
            search_result.append(f"{file}:{i+1}")
        line_tokens = lines[i].split()

        # بررسی وجود تابع
        if ("(" in lines[i] and ")" in lines[i]):
            left = lines[i].split("(")[0]
            name = left.split()[-1]
            if (name not in ("for", "while", "switch", "if", "catch")):
                functions.append(f"{name}() in {file} line {i+1}")

# چاپ نتایج
print("\033[33mTotal lines:", total_lines)

print("\n\033[32mFunctions:")
if (len(functions) == 0):
    print("No function.")
else:
    for func in functions:
        print("-", func)

print("\n\033[35mClasses:")
if (len(classes) == 0):
    print("No class.")
else:
    for clas in classes:
        print("-", clas)

print(f"\n\033[36mSearch result for \"{word}\":")
if (len(search_result) == 0):
    print("No result.")
else:
    for result in search_result:
        print("-", result)

print("\033[0m")
input()
