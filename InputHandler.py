import pywinusb.hid as hid
from time import sleep
from msvcrt import kbhit

def get_device_list():
    devices = hid.HidDeviceFilter().get_devices()
    device_list = []
    for i, dev in enumerate(devices):
        device_info = {
            'index': i,
            'parent_instance_id': dev.parent_instance_id,
            'serial_number': dev.serial_number,
            'vendor_id': dev.vendor_id,
            'product_id': dev.product_id,
            'version_number': dev.version_number,
            'product_name': dev.product_name
        }
        device_list.append(device_info)
    return device_list

def sample_handler(data):
    print("Raw data: {0:}".format(data))

def display_input_values(device):
    try:
        device.open()
        # set custom raw data handler
        device.set_raw_data_handler(sample_handler)

        print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
        while not kbhit() and device.is_plugged():
            # just keep the device opened to receive events
            sleep(0.5)
    finally:
        device.close()