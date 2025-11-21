import argparse
import time 
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
                        choices={"print", "live", "file"},
                        help="",
                        default="file")
    

    return parser.parse_args()

def alert_mode(args):
    try:
          match args.mode:
                case args.print:
                    sentinel_print_mode()
                    print("STARTING: Running Sentinel in PRINT mode....")
                    time.sleep(2)
                case (args.live):
                    sentinel_live_mode()
                case (args.file):
                    sentinel_file_mode()
    except Exception as e:
        print(f"ERROR: {e}")
    if args.mode == None:
        sentinel_file_mode()

def sentinel_print_mode(args):
    pass   

def sentinel_live_mode(args):
    pass

def sentinel_file_mode(args):
    print("STARTING: Running Sentinel in FILE mode....")
    time.sleep(2)
    keyword_list = read_log_file(args)
    save_to_file(args, keyword_list)
    close_file(args)
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
                print(msg) ## remove at some point 
                keyword_list.append(msg)
    except FileNotFoundError:
        print(f"ERROR: File {args.file} not found")
    except Exception as e:
        print(f"ERROR: {e}")
    return keyword_list

def save_to_file(args, generic_list):
    args.output.write(str(generic_list))

def close_file(args):
    try:
        args.file.close()
    except Exception as e:
        print(f"ERROR: {e}")
    if getattr(args, "output", None):
        try:
            args.output.close()
        except Exception:
            pass

    

def main():
    args = parse_args() ## parses args 
    alert_mode(args) ## checks mode 
    #keyword_list = read_log_file(args) ## retrieves list of keywords 
    

if __name__ == '__main__':
    main()