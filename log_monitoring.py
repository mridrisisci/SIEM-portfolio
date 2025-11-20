import argparse

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
    parser.add_argument("--alert-mode", 
                        metavar="", 
                        help="")
    parser.add_argument("-o", 
                        "--output", 
                        type=argparse.FileType('w'), 
                        metavar="", 
                        help="Write to file")
    parser.add_argument("-m",
                        "--mode", 
                        choices={"print", "live"},
                        help="run the tool in live mode to monitor real time or " \
                        "use the print mode")
    

    return parser.parse_args()


def monitor_file(args):
    try:
        content = args.file.read()
        if not args.keywords:
            print("No keywords given.")
            return
        
        lines = content.splitlines() # this is a string
        keywords = args.keywords.split(",")
        generic_list = []

        for line_number, line in enumerate(lines, 1):
            if (any(k.strip() in line for k in keywords)):
                msg = f"Line: {line_number} : line {line}"
                print(msg)
                generic_list.append(msg, "\n")
    except FileNotFoundError:
        print(f"ERROR: File {args.file} not found")
    except Exception as e:
        print(f"ERROR: {e}")
    return generic_list

def save_to_file(args, generic_list):
    with open(args.output, 'x') as file:
        file.write(generic_list)

def close_file(args):
    try:
        args.file.close()
    except Exception as e:
        pass
    if getattr(args, "output", None):
        try:
            args.output.close()
        except Exception:
            pass

    

def main():
    args = parse_args()
    
    monitor_file(args)
    close_file(args)

if __name__ == '__main__':
    main()