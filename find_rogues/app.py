from typing import Dict, Optional

import pendulum as pdl
import pycentral
import yaml
from fuzzywuzzy import fuzz, process
from pycentral.base import ArubaCentralBase
from rich import print
from rich.console import Console
from rich.table import Table

with open(".env.yaml", "r") as envf:
    central_info = yaml.safe_load(envf)

with open("ssids.yaml", "r") as ssidsf:
    match_ssids = yaml.safe_load(ssidsf)

# print(central_info['central_info'])

account = "sephora"

ssl_verify = True
central = ArubaCentralBase(central_info=central_info[account],
                           ssl_verify=ssl_verify)
apiParams = {
    "limit": 20,
    "offset": 0
}

def get_groups():
    apiPath = "/configuration/v2/groups"
    apiMethod = "GET"

    return central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)

def get_rogues() -> Optional[Dict]:
    apiPath = "/rapids/v1/rogue_aps"
    apiMethod = "GET"

    return central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)


def get_suspected_rogues() -> Optional[Dict]:
    apiPath = "/rapids/v1/suspect_aps"
    apiMethod = "GET"

    return central.command(apiMethod=apiMethod, apiPath=apiPath, apiParams=apiParams)
    
all_rapids_types = get_rogues()['msg']['rogue_aps'] + get_suspected_rogues()['msg']['suspect_aps'] #type: ignore
len_all_rapids_types = len(all_rapids_types)


def find_ssids(fdata):
    # List SSID returned from Aruba Central
    # for d in fdata:
    #     if 'ssid' in d:
    #         print(d['ssid'])
    
    rogue_ssid_matches = []

    for ea in fdata:
        # If ssid key doesn't exist, add a blank entry
        ea["ssid"] = "" if 'ssid' not in ea else ea['ssid']
        rogue_ssid_matches.extend(ea for ea_ssid in match_ssids['sephora'] if fuzz.partial_ratio(ea['ssid'].lower(), ea_ssid) > 80)

    return rogue_ssid_matches

def show_all_rogues(all_rapids_types):
    # print(f"\nNumber of rogues: {len_all_rapids_types}")
    table = Table(title=f"\n{len_all_rapids_types} All Rogue APs Found")

    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Rogeu SSID", style="green")
    table.add_column("Manufacture")
    table.add_column("Signal", justify="right", style="green")
    table.add_column("Group")
    table.add_column("First Seen")
    table.add_column("Seen by")

    for ea in all_rapids_types:
        ssid = "" if 'ssid' not in ea else ea['ssid']
        dt_last_seen= pdl.parse(ea['last_seen']) #type: ignore
        table.add_row(ea['classification'], ssid, ea['name'], str(ea['signal']), ea['group_name'], dt_last_seen.to_cookie_string(), ea['last_det_device_name']) #type: ignore

    console = Console()
    console.print(table)

def show_rogue_ssids(all_rapids_types):
    # SSIDs that match Rogue SSIDs
    matches = find_ssids(all_rapids_types)

    table = Table(title=f"\n{len(matches)} Sephora Rogue AP SSIDs Found")

    table.add_column("Type", justify="right", style="cyan", no_wrap=True)
    table.add_column("Rogue SSID", style="green")
    table.add_column("Manufacture")
    table.add_column("Signal", justify="right", style="green")
    table.add_column("Group")
    table.add_column("First Seen")
    table.add_column("Seen by")

    for ea in matches:
        ssid = "" if 'ssid' not in ea else ea['ssid']
        dt_last_seen= pdl.parse(ea['last_seen']) #type: ignore
        table.add_row(ea['classification'], ssid, ea['name'], str(ea['signal']), ea['group_name'], dt_last_seen.to_cookie_string(), ea['last_det_device_name']) #type: ignore

    console = Console()
    console.print(table)


if __name__ == "__main__":
    show_all_rogues(all_rapids_types)
    show_rogue_ssids(all_rapids_types)