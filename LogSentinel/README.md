<<<<<<< HEAD
Tool accepts:
--file <path-to-log>
--keywords <comma-separated-list>
--alert-mode <print|write>
--output <path-to-output-file>   (only required when alert-mode = write)

Example usage.
python monitor.py --file /var/log/auth.log --keywords error,login,failed --alert-mode print
python monitor.py --file security.log --keywords malware,hack --alert-mode write --output alerts.txt

=======
# SIEM-portfolio
>>>>>>> 732f5cd6ecdaa82a987d7f8ec73fb3ad76e8e4e0
