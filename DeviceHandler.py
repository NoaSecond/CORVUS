import pygame

pygame.init()
pygame.joystick.init()

def get_device_list():
    device_list = []
            
    if pygame.joystick.get_count() == 0:
        return device_list

    for i in range(pygame.joystick.get_count()):
        device_list.append(pygame.joystick.Joystick(i))      

    return device_list

def get_device_info(device):
    device_info = {
        'name': device.get_name(),
        'num_axes': device.get_numaxes(),
        'num_buttons': device.get_numbuttons(),
        'num_hats': device.get_numhats()
    }
    return device_info