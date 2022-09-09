from pathlib import Path
import re
import shutil
import sys

EXT_DICT = {'images' : ('JPEG', 'PNG', 'JPG', 'SVG'),
            'video' : ('AVI', 'MP4', 'MOV', 'MKV'),
            'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX'),
            'audio' : ('MP3', 'OGG', 'WAV', 'AMR'),
            'archives' : ('ZIP', 'GZ', 'TAR')}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

non_checked_folders = []    

def normalize(file):
    """Функія замінює всі букви на латиницю і всі знаки окрім букв, цифр та '_' на знак '_'"""
    return re.sub('\W', '_', file.name.rstrip(file.suffix).translate(TRANS)) + file.suffix


def unzip_file(folder_name, file_zip):
    """Розархівірує файл в каталог archives"""
    shutil.unpack_archive(file_zip, Path.joinpath(folder_name, file_zip.name.rstrip(file_zip.suffix)))

def move_file_to_folder(directory, folder_name, extension):
    """Переміщує файл згідно з EXT_DICT"""
    for file in directory.glob('*.' + extension):
        if not Path.exists(folder_name):
            Path.mkdir(folder_name)
            non_checked_folders.append(folder_name)
        
        new_path = Path.joinpath(folder_name, normalize(file))
        if not Path.exists(new_path):
            file.rename(new_path)
            if folder_name.name == 'archives':
                unzip_file(folder_name, new_path)
    for f in directory.iterdir():
        if f.is_dir():
            if f in non_checked_folders:
                continue
            move_file_to_folder(f, folder_name, extension)

def rename_files(directory, new_path_directory = None):
    for f in directory.iterdir():
        if Path.is_dir(f):
            if f in non_checked_folders:    #не перевыряємо каталог, як що він вже відсортований                 
                continue
            else:
                name_folder = normalize(f)
                if name_folder != f.name:   #як що треба змінити ім'я каталогу
                    if new_path_directory == None:
                        new_path = Path.joinpath(f.parent, name_folder)
                    else:
                        new_path = Path.joinpath(new_path_directory, name_folder)
                    if not Path.exists(new_path):
                        Path.mkdir(new_path)
                    if not new_path in non_checked_folders:
                        non_checked_folders.append(new_path)
                else:
                    new_path = f
                rename_files(f, new_path)
                if len(list(f.glob('*'))) == 0:
                    f.rmdir()       
        else:
            new_name = normalize(f)
            if new_name != f.name or directory != new_path_directory:     #як що треба змінити ім'я файлу або директорію
                if new_path_directory == None:
                    f.rename(Path.joinpath(f.parent, new_name))
                else:
                    f.rename(Path.joinpath(new_path_directory, new_name))




def sort_files(directory):
    '''Функція сортує файли по їх розширенню'''

    #Сортуємо розширення зі списку
    for key, extensions in EXT_DICT.items():
        folder_name = Path.joinpath(directory, key)
        non_checked_folders.append(folder_name)
        for extension in extensions:
            move_file_to_folder(directory, folder_name, extension)

    #Переіменовуємо файли які не були відсортовані
    rename_files(directory)
 

def main():
    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()
    path = sys.argv[1]
    directory = Path(path_directory)
    if not directory.is_dir():
        path('Path incorrect')
        exit()

    sort_files(directory)


if __name__ == '__main__':
    exit(main()) 
