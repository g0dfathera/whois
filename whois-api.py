import requests
import json

API_KEY = 'YOUR_API_KEY'

domain_name = input("Enter domain name: ")

url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={API_KEY}&domainName={domain_name}&outputFormat=JSON'

response = requests.get(url)

if response.status_code == 200:
    whois_data = response.json()
    
    # print("Raw WHOIS Response:")
    # print(json.dumps(whois_data, indent=4)) 

    def clean_whois_data(whois_data):
        record = whois_data.get('WhoisRecord', {})

        # Extract the necessary fields from the raw WHOIS response
        cleaned_whois = {
            "domainName": record.get('domainName', 'Not available'),
            "createdDate": record.get('registryData', {}).get('createdDate', 'Not available'),
            "expiresDate": record.get('registryData', {}).get('expiresDate', 'Not available'),
            "registrarName": record.get('registrarName', 'Not available'),
            "registrarIANAID": record.get('registrarIANAID', 'Not available'),
            "estimatedDomainAge": record.get('estimatedDomainAge', 'Not available'),
            "nameServers": record.get('registryData', {}).get('nameServers', {}).get('hostNames', []),
            "contactEmail": whois_data.get('contactEmail', 'Not available'),
            "auditCreatedDate": record.get('audit', {}).get('createdDate', 'Not available'),
            "auditUpdatedDate": record.get('audit', {}).get('updatedDate', 'Not available')
        }

        # Clean up registrant, technical contact, and administrative contact info
        registrant = record.get('registryData', {}).get('registrant', {})
        cleaned_whois["registrant"] = {
            "name": registrant.get('name', 'Not available'),
            "email": registrant.get('email', 'Not available')
        }

        tech_contact = record.get('registryData', {}).get('technicalContact', {})
        cleaned_whois["technicalContact"] = {
            "name": tech_contact.get('name', 'Not available'),
            "email": tech_contact.get('email', 'Not available')
        }

        admin_contact = record.get('registryData', {}).get('administrativeContact', {})
        cleaned_whois["administrativeContact"] = {
            "name": admin_contact.get('name', 'Not available'),
            "email": admin_contact.get('email', 'Not available')
        }

        return cleaned_whois

    # Clean the WHOIS data and print it
    cleaned_whois = clean_whois_data(whois_data)

    # Output the cleaned-up WHOIS data as a single JSON response
    print("\n--- Cleaned-up WHOIS Response ---")
    print(json.dumps(cleaned_whois, indent=4))

else:
    print(f"Error: Unable to fetch WHOIS data for {domain_name}. Status Code: {response.status_code}")
