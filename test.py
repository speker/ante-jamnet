from subprocess import check_output
module_ip = check_output(['hostname', '--all-ip-addresses']).decode("utf-8").strip()
module_name = check_output(['hostname']).decode("utf-8").strip()
print(module_ip)