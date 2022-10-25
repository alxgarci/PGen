import base64
import binascii
import random
import shutil
import string
import pyperclip
import os
import colorama
import getpass
import configparser
import logging

# FILE PATHS
BACKUP_PATH = "config/backup"
FILE_PATH = "config/settings.ini"
LOG_PATH = "config/log.txt"

# TERMINAL CHAR WIDTH
TOTAL_CHARS_ANCHO = 64

# PASSWORD LENGTH AND ASCII MULTIPLIER AS RANDOM SEED
ASCII_MULTIPLIER = 0
LONG_PASS = 0

# VERSION INFO
VERSION = ""
GITHUB_URL = "github.com/"
FECHA_COMP = ""
KEY = ""
PASS = ""


# READ SAVED SETTINGS
def read_ini(file_path):
    global LONG_PASS, VERSION, FECHA_COMP, KEY, PASS, KEY, ASCII_MULTIPLIER
    config = configparser.ConfigParser()
    config.read(file_path)
    LONG_PASS = int(config.get("SETTINGS", "LONG_PASS"))
    VERSION = config.get("INFO", "VERSION")
    FECHA_COMP = config.get("INFO", "FECHA_COMP")
    KEY = config.get("SETTINGS", "KEY")
    ASCII_MULTIPLIER = int(config.get("SETTINGS", "ASCII_MULTIPLIER"))
    PASS = decode(KEY, config.get("SETTINGS", "PASS_ENC").encode("utf-8"))

    logging.info(".ini read [" + FILE_PATH + "]")


def write_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    config.set("INFO", "VERSION", VERSION)
    config.set("INFO", "FECHA_COMP", FECHA_COMP)
    config.set("SETTINGS", "LONG_PASS", str(LONG_PASS))
    config.set("SETTINGS", "PASS_ENC", encode(KEY, PASS).decode("utf-8"))
    config.set("SETTINGS", "KEY", KEY)
    config.set("SETTINGS", "ASCII_MULTIPLIER", str(ASCII_MULTIPLIER))
    c = 0
    with open(file_path, 'w') as f:
        config.write(f)
        c += 1
    logging.info(str(c) + " lines written in [" + FILE_PATH + "]")
    read_ini(FILE_PATH)


def write_pass(ps):
    global PASS
    PASS = ps
    config = configparser.ConfigParser()
    config.read(FILE_PATH)
    config.set("SETTINGS", "PASS_ENC", encode(KEY, PASS).decode("utf-8"))
    with open(FILE_PATH, 'w') as f:
        config.write(f)
    logging.info(
        "PASS written in [" + FILE_PATH + "] with key " + KEY + " - PASS [" + ps[0] + "****" + ps[len(ps) - 1] + "]")
    read_ini(FILE_PATH)


# ENCODE AND DECODE MASTER KEY
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = (ord(clear[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    return base64.urlsafe_b64encode(bytes(enc))


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


# CLEAN TERMINAL (MULTI OS)
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def read_input():
    input_st = input(">>: ")
    return input_st


def enter_continue():
    print(colorama.Fore.YELLOW + "PRESS ENTER TO CONTINUE".center(TOTAL_CHARS_ANCHO) + colorama.Style.RESET_ALL)
    read_input()


def read_pass():
    input_ps = getpass.getpass(prompt=">>: ")
    return input_ps


def generate_ascii_multiplier(bottom_range, top_range):
    res = random.randint(bottom_range, top_range)
    return res


def print_intro():
    cls()

    comp = "v" + VERSION + " - " + FECHA_COMP
    print(colorama.Fore.BLUE
          + print_separator("<<>>", int(TOTAL_CHARS_ANCHO / 4)))

    logo_str = ("      ___         ___           ___           ___      \n" +
                "     /\  \       /\__\         /\__\         /\  \     \n" +
                "    /::\  \     /:/ _/_       /:/ _/_        \:\  \    \n" +
                "   /:/\:\__\   /:/ /\  \     /:/ /\__\        \:\  \   \n" +
                "  /:/ /:/  /  /:/ /::\  \   /:/ /:/ _/_   _____\:\  \  \n" +
                " /:/_/:/  /  /:/__\/\:\__\ /:/_/:/ /\__\ /::::::::\__\ \n" +
                " \:\/:/  /   \:\  \ /:/  / \:\/:/ /:/  / \:\––\––\/__/ \n" +
                "  \::/__/     \:\  /:/  /   \::/_/:/  /   \:\  \       \n" +
                "   \:\  \      \:\/:/  /     \:\/:/  /     \:\  \      \n" +
                "    \:\__\      \::/  /       \::/  /       \:\__\     \n" +
                "     \/__/       \/__/         \/__/         \/__/     \n")

    for line in logo_str.split("\n"):
        print(line.center(TOTAL_CHARS_ANCHO))
    print(comp.center(TOTAL_CHARS_ANCHO))
    print(print_separator("<<>>", int(TOTAL_CHARS_ANCHO / 4)) + "\n"
          + colorama.Style.RESET_ALL)


def print_separator(symbol, times):
    sep = symbol * times
    return sep.center(TOTAL_CHARS_ANCHO)


def pedir_clave_maestra():
    print("> Enter the new MASTER PASSWORD :")
    clave_m = read_pass()
    logging.info("MASTER PASSWORD written in [" + FILE_PATH + "] with key " + KEY)
    return clave_m


def pedir_nombre_sitio():
    print("> Enter the site name ['HE' for help]:")
    clave_m = read_input()
    if clave_m.casefold() == "he":
        print("> IMPRIMIENDO AYUDA:")
        print("  Enter the domain name,\n"
              "without spaces and just the domain w/o .com, .net ...")
        read_input()
    logging.info("PASS for site " + clave_m + " generated")

    return clave_m


def ascii_pass(total_ascii):
    conjunto_chars = string.ascii_letters + string.digits + "!.#@"
    random.seed(total_ascii)
    res = ''.join(random.choice(conjunto_chars) for i in range(LONG_PASS))
    return res


def calcular_contra(cmaestra, nsitio):
    ascii_cm = cmaestra.strip().casefold().encode('ascii')
    total_cm = 0
    for x in ascii_cm:
        total_cm += x

    ascii_ns = nsitio.strip().casefold().encode('ascii')
    total_ns = 0
    for j in ascii_ns:
        total_ns += j

    total_ascii = total_cm * total_ns * ASCII_MULTIPLIER

    return ascii_pass(total_ascii)


def generate_key_token():
    st = binascii.hexlify(os.urandom(20)).decode("utf-8")
    logging.info("new KEY generated [" + st + "]")
    return st


def get_menu():
    # With line "{:<64}".format("STRING") if string is less than 64 chars, autocompletes with spaces
    st_caution = colorama.Fore.RED + "[CAUTION]" + colorama.Fore.GREEN
    print("{:<68}".format(colorama.Fore.GREEN + " [MENU] Main menu").center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > SETUP - First time setup/reset key and seed " + st_caution).center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > R - Regenerate password encryption key " + st_caution).center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > C - Change master password " + st_caution).center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > G - Force write all changes").center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > M - Show master password").center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > W - Force write all changes").center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > B - Backup settings.ini").center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > P - Autogenerate new password").center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > N - Generate new one-time password").center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > CLEAN - Clean log.txt" + st_caution).center(TOTAL_CHARS_ANCHO))
    print("{:<68}".format("   > QUIT - Quit the app" + colorama.Style.RESET_ALL).center(TOTAL_CHARS_ANCHO))
    return read_input()


def backup_settings(file_name):
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)

    target = os.path.join(os.getcwd(), BACKUP_PATH)

    if os.path.exists(file_name):
        shutil.copyfile(file_name, os.path.join(target, "settings_backup.bak"))
        return 1
    else:
        return 0


def new_onetime_password():
    ps = ascii_pass(generate_ascii_multiplier(0, 99999) * generate_ascii_multiplier(0, 99999))
    return ps


def print_and_clipboard_password(ps):
    pyperclip.copy(ps)
    print()
    print(colorama.Fore.GREEN + print_separator("* ", 25) + colorama.Style.RESET_ALL)
    print("PASSWORD COPIED TO CLIPBOARD!".center(TOTAL_CHARS_ANCHO))
    print(colorama.Fore.YELLOW + print_separator("* ", 25) + colorama.Style.RESET_ALL)
    print(colorama.Back.GREEN + ps.center(TOTAL_CHARS_ANCHO) + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + print_separator("* ", 25) + colorama.Style.RESET_ALL)


def is_first_run():
    config = configparser.ConfigParser()
    config.read(FILE_PATH)
    ps = decode(KEY, config.get("SETTINGS", "PASS_ENC").encode("utf-8"))
    if len(ps) == 0:
        return True
    else:
        return False


def main():
    global TOTAL_CHARS_ANCHO, KEY, ASCII_MULTIPLIER

    TOTAL_CHARS_ANCHO = os.get_terminal_size().columns
    logging.basicConfig(filename=LOG_PATH,
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%b-%d %H:%M:%S')
    ans = ""

    read_ini(FILE_PATH)

    while "quit" not in ans:

        print_intro()
        if is_first_run():
            print(colorama.Back.YELLOW + colorama.Fore.BLACK +
                  "{:<58}".format("ITS YOUR FIRST RUN! PLEASE, FOLLOW THE FIRST STEPS:")
                  .center(TOTAL_CHARS_ANCHO))
            print("{:<58}".format(" 1 - HEAD UP TO 'SETUP' AND GENERATE A UNIQUE KEY AND SEED")
                  .center(TOTAL_CHARS_ANCHO))
            print("{:<58}".format(" 2 - GO TO OPTION 'C' AND CREATE A MASTER PASSWORD")
                  .center(TOTAL_CHARS_ANCHO))
            print("{:<58}".format(" 3 - START CREATING YOUR STATIC AND SECURE PASSWORDS!")
                  .center(TOTAL_CHARS_ANCHO))
            print("- IF YOU HAVE ANY TROUBLE, HEAD TO THE HOMEPAGE AT -"
                  .center(TOTAL_CHARS_ANCHO))
            print(GITHUB_URL.center(TOTAL_CHARS_ANCHO) + colorama.Style.RESET_ALL)
        ans = get_menu().casefold().strip()
        print_intro()

        if ans == "setup":
            print("A NEW ENCRYPTION TOKEN WILL BE GENERATED".center(TOTAL_CHARS_ANCHO))
            print("AND A NEW SEED NUMBER TO GENERATE NEW PASSWORDS.".center(TOTAL_CHARS_ANCHO))
            print("PRESS ENTER TO CONTINUE".center(TOTAL_CHARS_ANCHO))
            read_input()
            KEY = generate_key_token()
            ASCII_MULTIPLIER = generate_ascii_multiplier(10000, 99999)
            write_ini(FILE_PATH)

            print("KEY GENERATED CORRECTLY")

        elif ans == "r":
            print("PRESS ENTER TO REGENERATE PASSWORD ENCRYPTION KEY, N TO CANCEL".center(TOTAL_CHARS_ANCHO))
            if read_input().casefold() != "n":
                KEY = generate_key_token()
                write_ini(FILE_PATH)

        elif ans == "c":
            cmaestra = pedir_clave_maestra()
            write_pass(cmaestra)
            print("MASTER PASSWORD WRITTEN TO".center(TOTAL_CHARS_ANCHO))
            print(colorama.Fore.GREEN + FILE_PATH.center(TOTAL_CHARS_ANCHO) + colorama.Fore.RESET)

        elif ans == "g":
            write_ini(FILE_PATH)
            print("ALL WRITTEN TO".center(TOTAL_CHARS_ANCHO))
            print(colorama.Fore.GREEN + FILE_PATH.center(TOTAL_CHARS_ANCHO) + colorama.Fore.RESET)

        elif ans == "m":
            print("YOUR MASTER PASSWORD IS".center(TOTAL_CHARS_ANCHO))
            print(colorama.Fore.GREEN + PASS.center(TOTAL_CHARS_ANCHO) + colorama.Fore.RESET)

        elif ans == "w":
            write_ini(FILE_PATH)

        elif ans == "b":
            if backup_settings(FILE_PATH) == 1:
                st = "BACKUP CREATED IN " + BACKUP_PATH
                print(st.center(TOTAL_CHARS_ANCHO))
            else:
                print(colorama.Fore.RED + "ERROR CREATING THE BACKUP".center(TOTAL_CHARS_ANCHO)
                      + colorama.Style.RESET_ALL)

        elif ans == "p":
            nsitio = pedir_nombre_sitio()
            contra_res = calcular_contra(PASS, nsitio)

            print_intro()

            print_and_clipboard_password(contra_res)

        elif ans == "n":
            one_time_ps = new_onetime_password()
            print_and_clipboard_password(one_time_ps)

        elif ans == "clean":
            print(colorama.Back.YELLOW + colorama.Fore.BLACK)
            st1 = "ALL DATA IN " + LOG_PATH + " WILL BE ERASED"
            st2 = "PRESS ENTER TO CLEAN " + "{:.3f}".format(os.stat(LOG_PATH).st_size/1024) + " KB"
            print(st1.center(TOTAL_CHARS_ANCHO))
            print(st2.center(TOTAL_CHARS_ANCHO))
            print("AND 'N' TO CANCEL".center(TOTAL_CHARS_ANCHO) + colorama.Style.RESET_ALL)
            if read_input().casefold() != "n":
                with open(LOG_PATH, 'w'):
                    pass

        elif "quit" not in ans:
            print(colorama.Fore.RED + "OPTION NOT LISTED".center(TOTAL_CHARS_ANCHO) + colorama.Style.RESET_ALL)
        enter_continue()


if __name__ == '__main__':
    main()
