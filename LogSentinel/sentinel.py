import argparse
import time
from datetime import datetime
import logging 
from logging.handlers import RotatingFileHandler
import os
'''
Title: LogSentinel
Description:
Purpose:
Usage: 
Author: Idris Isci

'''
def parse_args():
    parser = argparse.ArgumentParser(description="real time log monitoring")

    parser.add_argument("-f", 
                        "--file", 
                        type=argparse.FileType('r'), 
                        help="File to read", 
                        required=True)
    parser.add_argument("-k", 
                        "--keywords", 
                        metavar="", 
                        required=True,
                        help="provide the keywords the tool must search to monitor for")
    parser.add_argument("-o", 
                        "--output", 
                        type=argparse.FileType('w'), 
                        metavar="", 
                        help="Write to file")
    parser.add_argument("-m",
                        "--mode", 
                        choices=["print", "live", "file"],
                        help="",
                        default="file")
    

    return parser.parse_args()

def start_sentinel(args):
    try:
          match args.mode:
                case "print":
                    sentinel_print_mode(args)
                case "live":
                    sentinel_live_mode(args)
                case "file":
                    sentinel_file_mode(args)
    except Exception as e:
        print(f"ERROR: {e}")

def sentinel_print_mode(args):
    print("STARTING: Running Sentinel in PRINT mode....")
    time.sleep(2)
    keyword_list = read_log_file(args)

    logged_status = True

    # get line number from list 
    try:
        print("original list", keyword_list)
        keywords = [k.strip() for k in args.keywords.split(";")]
        for k in keyword_list: # K looks like: "Line: 1 : line system is 0wned"
            parts = k.split(":") # parts -> ["Line", " 1 " ", " line system is 0wned]

            if len(parts) >= 3:
                line_num_str = parts[1].strip()
                line_txt = parts[2].strip()

                try:
                    line_num = int(line_num_str)
                except ValueError:
                    line_num = line_num_str
                
                print(
                    f"Line: {line_num} ---"
                    f"Keyword detected: {', '.join(keywords)} --- "
                    f"Severity MEDIUM --- "
                    f"Logged: {logged_status}" 
                )
    except FileNotFoundError:
        print(f"ERROR: File {args.file} not found")
    except Exception as e:
        print(f"ERROR: {e}")
    return keyword_list

    pass   

def sentinel_live_mode(args):
    pass

def sentinel_file_mode(args):
    print("STARTING: Running Sentinel in FILE mode....")
    time.sleep(2)
    keyword_list = read_log_file(args)
    save_to_file(args, keyword_list)
    close_file(args)
    print("Log file has been created and is ready for analysis.")
    return keyword_list


def read_log_file(args):
    try:
        content = args.file.read()
        if not args.keywords:
            print("No keywords given.")
            return
        
        lines = content.splitlines() # this is a string
        keywords = args.keywords.split(",")
        keyword_list = []

        for line_number, line in enumerate(lines, 1):
            if (any(k.strip() in line for k in keywords)):
                msg = f"Line: {line_number} : line {line}"
                keyword_list.append(msg)
    except FileNotFoundError:
        print(f"ERROR: File {args.file} not found")
    except Exception as e:
        print(f"ERROR: {e}")
    return keyword_list

def save_to_file(args, generic_list):
    try:
        content = '\n'.join(generic_list)
        args.output.write(content)
    except Exception as e:
        print(f"ERROR: {e}")

def close_file(args):
    try:
        args.file.close()
    except Exception as e:
        print(f"ERROR: {e}")
    if getattr(args, "output", None):
        try:
            args.output.close()
        except Exception as e:
            print(f"ERROR: {e}")

    
def make_log_file():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"sentinel_{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}.log")

    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # console handling
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(console_handler)
    return logger

def make_log_stream():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    formatter = logging.formatter("%{levelname}s:%{name}s:%{message}s")
    stream_handler.setFormatter(formattter)
    logger.addHandler(stream_handler)
 
def main():
    args = parse_args() ## parses args 
    file_logger = make_log_file() # prevent log file creation on every run
    file_logger.info("Started Sentinel.")
    start_sentinel(args) ## checks mode 
    file_logger.info("Shutting Sentinel.")
    

if __name__ == '__main__':
    main()