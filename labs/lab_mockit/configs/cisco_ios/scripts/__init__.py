
from src.ssh_server.db_operations import create_table, create_record, read_record, update_record, delete_record
import re

# Create the table for VLANs if not exists
create_table('cisco_ios')

def handle_command(command: str):
    if command.startswith("vlan"):
        # Get the VLAN number
        match = re.search(r'vlan (\d+)', command)
        if match:
            vlan_number = match.group(1)
            vlan_name = f"VLAN{vlan_number.zfill(4)}"
            vlan_status = "active"
            vlan_ports = " "  # Default port, you may want to make this configurable

            # Check if VLAN already exists
            existing_vlans = read_record("cisco_ios", "vlan")

            # If VLAN exists, update it; otherwise, create a new record
            if existing_vlans:
                if vlan_name not in existing_vlans:
                    update_record("cisco_ios", "vlan", existing_vlans + f"\n{vlan_number} {vlan_name} {vlan_status} {vlan_ports}")
            else:
                create_record("cisco_ios", "vlan", f"{vlan_number} {vlan_name} {vlan_status} {vlan_ports}")
            return True

    if command == "show vlan brief":
        # Read VLANs from the database
        vlans = read_record("cisco_ios", "vlan")
        if vlans:
            # Format the VLANs into a table
            table_header = "{:<4} {:<32} {:<9} {:<30}".format("VLAN", "Name", "Status", "Ports")
            table_separator = "-" * len(table_header)
            table_rows = [table_header, table_separator]

            # Add each VLAN to the table
            for vlan in vlans.split("\n"):
                vlan_details = vlan.split(" ")
                vlan_row = "{:<4} {:<32} {:<9} {:<30}".format(vlan_details[0], vlan_details[1], vlan_details[2], vlan_details[3])
                table_rows.append(vlan_row)

            # Join the rows into a formatted string
            return "\n".join(table_rows)