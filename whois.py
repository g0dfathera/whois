import subprocess
import ipaddress

def is_internal_ip(target_ip):
    try:
        private_networks = [
            ipaddress.IPv4Network("10.0.0.0/8"),
            ipaddress.IPv4Network("172.16.0.0/12"),
            ipaddress.IPv4Network("192.168.0.0/16"),
            ipaddress.IPv4Network("169.254.0.0/16")
        ]

        ip = ipaddress.IPv4Address(target_ip)

        for network in private_networks:
            if ip in network:
                return True
        return False
    except ValueError:
        return False
      
def run_whois_search(target_ip):
    # WHOIS search logic
    if is_internal_ip(target_ip):
        return "Error: WHOIS lookup for internal IPs is not allowed."

    try:
        # Execute WHOIS command
        command = ["whois", target_ip]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
