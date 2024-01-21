import os
import shutil
from pathlib import Path
import zipfile
import tarfile
import sys
from concurrent.futures import ThreadPoolExecutor
import logging



extensions = {
    'jpg': 'images',
    'jpeg': 'images',
    'png': 'images',
    'gif': 'images',
    'svg': 'images',
    'avi': 'videos',
    'mp4': 'videos',
    'mov': 'videos',
    'mkv': 'videos',
    'doc': 'documents',
    'docx': 'documents',
    'txt': 'documents',
    'pdf': 'documents',
    'xlsx': 'documents',
    'pptx': 'documents',
    'mp3': 'audio',
    'ogg': 'audio',
    'wav': 'audio',
    'amr': 'audio',
    'zip': 'archives',
    'gz': 'archives',
    'tar': 'archives',
}


# Konfiguracja loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def transliterate_and_normalize(input_string):
    # Tworzenie mapy transliteracji polskich znaków na znaki ASCII
    transliteration_map = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l',
        'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z',
        'ż': 'z',
    }

    # Wykonaj transliterację na znaku po znaku i zamień inne znaki na '_'
    normalized_string = ''
    for char in input_string:
        normalized_char = transliteration_map.get(char, char)
        if not normalized_char.isalnum() and normalized_char != '.':
            normalized_char = '_'
        normalized_string += normalized_char

    return normalized_string

# Zapytanie czy na pewno ten katalog chce się uporządkować.


def confirm_directory_cleanup(path):
    confirmation = input(
        f"Czy na pewno chcesz posprzątać ten katalog: {path}? (Tak/Nie): ").strip().lower()
    if confirmation == 'tak':
        return True
    else:
        print("Operacja anulowana.")
        return False


# Wyodrębnianie rozszerzeń, tworzenie folderów, przenoszenie plików
def organize_files_by_extension_worker(args):
    folder, extensions, verbose = args
    archives_folder = os.path.join(folder, 'archives')

    for folder, subfolders, files in os.walk(folder):
        if os.path.normpath(folder) == os.path.normpath(archives_folder):
            subfolders[:] = []
            continue
        for file in files:
            extension = file.split('.')[-1].lower()
            if extension in extensions:
                folder_name = extensions[extension]
                if not os.path.exists(os.path.join(folder, folder_name)):
                    os.mkdir(os.path.join(folder, folder_name))
                src = os.path.join(folder, file)
                dst = os.path.join(folder, folder_name, file)
                if verbose:
                    logger.info(f'Moving {src} to {dst}')
                shutil.move(src, dst)

def organize_files_by_extension_parallel(path, extensions, verbose=False):
    with ThreadPoolExecutor() as executor:
        args_list = [(path, extensions, verbose) for _ in os.walk(path)]
        executor.map(organize_files_by_extension_worker, args_list)


# Przenoszenie i rozpakowywanie spakowanych plików
def unpack_archives(archives_folder, path):
    # Przeszukaj katalog "archives" w poszukiwaniu plików archive
    for folder, subfolders, files in os.walk(archives_folder):
        for file in files:
            extension = file.split('.')[-1].lower()
            if extension in ('zip', 'gz', 'tar'):
                archive_path = os.path.join(folder, file)

                # Usuń rozszerzenie z nazwy archiwum
                folder_name = os.path.splitext(file)[0]
                if not os.path.exists(os.path.join(path, folder_name)):
                    os.mkdir(os.path.join(path, folder_name))
                destination_path = os.path.join(archives_folder, folder_name)

                # Jeśli katalog docelowy już istnieje, dodaj unikalny sufiks
                count = 1
                while os.path.exists(destination_path):
                    destination_path = os.path.join(
                        archives_folder, f"{folder_name}_{count}")
                    count += 1

                # Rozpakuj archiwum
                if extension == 'zip':
                    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                        zip_ref.extractall(destination_path)
                elif extension == 'gz':
                    with tarfile.open(archive_path, 'r:gz') as tar_ref:
                        tar_ref.extractall(destination_path)
                elif extension == 'tar':
                    with tarfile.open(archive_path, 'r') as tar_ref:
                        tar_ref.extractall(destination_path)

                # Usuń oryginalne archiwum
                if os.path.exists(archive_path):
                    os.remove(archive_path)


# Funkcja zamiany liter polskich na zwykłe i normalizacja nazw plików i folderów
def normalize_and_rename_files(path):
    archives_folder = os.path.join(path, 'archives')

    for folder, subfolders, files in os.walk(path):
        # Sprawdź, czy aktualny folder jest folderem "archives"
        if os.path.normpath(folder) == os.path.normpath(archives_folder):
            # Jeśli tak, pomiń ten folder i jego podfoldery
            subfolders[:] = []
            continue
        for file in files:
            old_file_path = Path(folder, file)

            # Pobieranie rozszerzenie pliku
            file_extension = old_file_path.suffix

            # usuwa rozszerzenie z nazwy pliku
            file_name_without_extension = old_file_path.stem

            # Wykonanie transliteracji polskich znaków na znaki ASCII i zamień inne znaki na '_'
            normalized_name = transliterate_and_normalize(
                file_name_without_extension)

            # Dodanie z powrotem rozszerzenia
            new_file_name = f"{normalized_name}{file_extension}"
            new_file_path = Path(folder, new_file_name)

            old_file_path.rename(new_file_path)


def normalize_and_rename_folders(path):
    archives_folder = os.path.join(path, 'archives')
    for folder, subfolders, _ in os.walk(path, topdown=False):
        # Sprawdź, czy aktualny folder jest folderem "archives"
        if os.path.normpath(folder) == os.path.normpath(archives_folder):
            # Jeśli tak, pomiń ten folder i jego podfoldery
            subfolders[:] = []
            continue
        for subfolder in subfolders:
            old_folder_path = Path(folder, subfolder)

            # Transliteracja polskich znaków na znaki ASCII i zamień inne znaki na '_'
            normalized_name = transliterate_and_normalize(subfolder)

            # Dodanie z powrotem rozszerzenie
            new_folder_path = Path(folder, normalized_name)

            # Przenoszenie (zmiana nazwy) folderu
            old_folder_path.rename(new_folder_path)


# Usuwa puste foldery
def remove_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"[+] Removed empty folder: {folder_path}")


# Podsumowanie
# 1. Lista plików w każdej kategorii
def list_files_in_categories(path, extensions):
    category_files = {category: [] for category in set(extensions.values())}

    for folder, _, files in os.walk(path):
        for file in files:
            extension = file.split('.')[-1].lower()
            if extension in extensions:
                folder_name = extensions[extension]
                category_files[folder_name].append(file)

    print("List of files in each category:")
    for category, files in category_files.items():
        print(f"{category}:")
        for file in files:
            print(f"  {file}")


# 2. Wykaz rozszerzeń, które pojawiły się w katalogach docelowych z podziałem na kategorie
def list_extensions_in_categories(path, target_categories):
    target_categories = ['images', 'videos', 'documents', 'audio', 'archives']
    extensions_in_target_categories = {category: []
                                       for category in target_categories}

    for category in target_categories:
        for folder, _, files in os.walk(os.path.join(path, category)):
            for file in files:
                extension = file.split('.')[-1].lower()
                if extension not in extensions_in_target_categories[category]:
                    extensions_in_target_categories[category].append(extension)

    print("Extensions in the target categories:")
    for category, ext_list in extensions_in_target_categories.items():
        print(f"{category}: {', '.join(ext_list)}")


# 3. Wykaz nierozpoznanych rozszerzeń
def list_unrecognized_extensions(path, extensions):
    unrecognized_extensions = set()

    for folder, subfolders, files in os.walk(path):
        if "archives" in subfolders:
            subfolders.remove("archives")
        for file in files:
            extension = file.split('.')[-1].lower()
            if extension not in extensions:
                unrecognized_extensions.add(extension)

    print("Unrecognized extensions in the target folder:")
    for ext in unrecognized_extensions:
        print(f"  {ext}")


# Wywołanie programu przy wpisaniu python sort.py lokalizacja pliku lub .\sort.py lokalizacja pliku przy PS
def main(path):
    target_categories = ['images', 'videos', 'documents', 'audio', 'archives']

    try:
        archives_folder = os.path.join(path, 'archives')

        organize_files_by_extension_parallel(path, extensions, verbose=True)
        normalize_and_rename_files(path)
        normalize_and_rename_folders(path)
        unpack_archives(archives_folder, path)
        remove_empty_folders(path)
        list_files_in_categories(path, extensions)
        list_extensions_in_categories(path, target_categories)
        list_unrecognized_extensions(path, extensions)

    except Exception as e:
        logger.error(f"Wystąpił błąd: {str(e)}")


def clean_and_organize_folder():
    if len(sys.argv) != 2:
        print("Użycie: clean-folder <ścieżka_do_folderu>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} nie istnieje.")
        sys.exit(1)

    main(folder_path)


if __name__ == "__main__":
    clean_and_organize_folder()