import socket, argparse, os 

def parse_args():
    parser = argparse.ArgumentParser(description="simple fingerprinting service. grab info on your target")

    # force ip/port 
    parser.add_argument("-t",
                        "--target",
                        help="target to scan")
    parser.add_argument("-p",
                        "--port",
                        help="port to scan",
                        type=int)

    parser.add_argument("-v",
                        "--verbose",
                        help="verbose info")
    
    return parser.parse_args()
    

def create_socket(args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # family - type
    ip = args.target
    port = args.port
    try:
     s.connect((ip,port))

     #banner grabbing
     banner = s.recv(1024).decode().strip()
     print(f"Banner: {ip}:{port} -> {banner}")   
     data = s.recv(10024).decode().strip()
     return data
    except (OSError, socket.error) as e:
       print(f"ERROR: {e}")
    else:
       pass
    finally:
       s.close()


def identify_service(args, response_data):
   
    response_data = create_socket(args.target,args.port)
    SIGNATURES = {
    "Apache": ["Apache", "Server: Apache"],
    "nginx": ["nginx"],
    "OpenSSH": ["SSH-"],
    "FTP": ["220", "FileZilla"],
    "SMTP": ["ESMTP", "SMTP"],
    }
    try: 
      for service_name, sig_list in SIGNATURES.items():
         if response_data in sig_list:
            print(f"Found best matching signature: {service_name}")
    except Error as e:
      print(f"ERROR: {e}")
   


    '''
    takes the banner/probe response

     loops through SIGNATURES

     returns best match
    '''
   
def start_fingerprinter(args):
   try:
      identify_service(args)
   except Error as e:
      print(f"ERROR: {e}")

def probe_service(ip,port):
   '''
   If no banner is received, this function sends probes

    Probe logic depends on port → HTTP, SMTP, FTP, etc.

    Returns whatever the target responds with
   '''
   pass

def extract_version(service_name, response_data):
   '''
   Given known service type (Apache, SSH, Postfix), attempt to extract versions using regex patterns

    Return version or None
   '''
   pass

def scan_target(ip,port):
   '''
   “Orchestrator” for scanning a single port

    Steps:

    Establish connection

    Get banner

    If no banner → probe

    Identify service

    Extract version

    Return structured result
   '''
   pass

def format_output(result):
    '''
    Convert the result dictionary into:

    Pretty console output

    or JSON

    or files

    Controlled by the CLI flags
    '''
    pass

def save_results(result, filepath):
   '''
    Write JSON or text output to a file

    Directory creation handling

    Append vs overwrite depending on your design
   '''
   pass


        

def main():
    args = parse_args()
    start_fingerprinter(args)

if __name__ == "__main__":
    main()