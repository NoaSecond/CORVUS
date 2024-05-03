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