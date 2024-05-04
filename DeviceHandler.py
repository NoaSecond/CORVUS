import pywinusb.hid as hid
from time import sleep
from msvcrt import kbhit

def get_device_info(device):
    device_info = {
        'parent_instance_id': device.parent_instance_id,
        'serial_number': device.serial_number,
        'vendor_id': device.vendor_id,
        'product_id': device.product_id,
        'version_number': device.version_number,
        'vendor_name': device.vendor_name,
        'product_name': device.product_name
    }
    return device_info  

def get_device_list():
    devices = hid.HidDeviceFilter().get_devices()
    device_list = []
    for device in devices:
        if get_device_info(device).get('product_name')[0] != '@':
            device_list.append(device)            
    return device_list

def count_elements(report):
    buttons = 0
    axes = 0
    hats = 0
    for byte in report:
        if byte < 32:  # Les premiers 32 bytes sont généralement des boutons
            buttons += 1
        elif byte == 39:  # 39 est souvent utilisé pour les chapeaux
            hats += 1
        else:
            axes += 1
    print(f"Nombre de boutons : {buttons}")
    print(f"Nombre d'axes : {axes}")
    print(f"Nombre de chapeaux : {hats}")

def count_elements_in_reports(device):
    try:
        device.open()
        reports = device.find_input_reports()  # Trouve tous les rapports d'entrée
        for report in reports:
            print("Report:", report)
            count_elements(report.raw_data)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        device.close()