#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change Mac address")
    parser.add_option("-m", "--mac", dest="mac", help="New mac address value")
    (options, args) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify your interface, --help for info")
    elif not options.mac:
        parser.error("[-] Please specify value of mac address to change, --help for info")
    else:
        return options  # Wszystko co zwizane z podaniem argumentw powinno byw funkcji z nimi zwizanymi


def change_mac(interface, new_mac):
    print("[+] Changing MAC address")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_from_ifconfig = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_from_ifconfig:
        return mac_from_ifconfig.group(0)
    else:
        print("[-] No mac address found in ifconfig")


def change_validator():
    options = get_arguments()
    change_mac(options.interface, options.mac)
    new_mac = get_current_mac(options.interface)
    if(options.mac == new_mac):
        print("[+] MAC address was sucessfully changed")
    else:
        print("[-] Address not changed")


change_validator()