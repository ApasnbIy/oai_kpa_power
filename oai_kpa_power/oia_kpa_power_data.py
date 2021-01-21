# -*- coding: utf-8 -*-

import time
import threading
import oai_modbus
import json


class CfgParameter:
    def __init__(self, **kwargs):
        self.serial_number = kwargs.get('serial_num', '208236A0424D')


class OaiKpaPower:
    def __init__(self, *args, **kwargs):
        # объект с параметрами
        self.cfg = CfgParameter(serial_num="208236A0424D")
        
        # разбор именованных параметров
        self.serial_number = kwargs.get('serial_num', '208236A0424D')
        self.debug = kwargs.get('debug', False)
        # создание объекта для общения по МодБас
        self.client = oai_modbus.OAI_Modbus(serial_num=[self.serial_number])
        self.client.debug_print_flag = True
        # параметры связи
        self.state = 0
        # описание связи через запись/чтение регистров

        self.register_addr = {
            "scaler": 1337,
            "voltage": 1338,
            "on_off": 1339,
            "overvoltage": 1340,
            "overcurrent": 1341,
            "calibration_1": 1342,
            "calibration_2": 1343,
            "flag_new_constrain": 1344,
            "flag_new_calibration": 1345,
            "it_is_power_module_flag": 1346,
            "ina_allert_reset": 1347
        }
        # параметры работы модуля
        self.iteration = 0
        self.voltage_expexted = 27000
        self.voltage_real = 0
        self.overcurrent = 2000;
        self.overvoltage = 32000;
        self.calibration_1 = 0
        self.calibration_2 = 0
        self.on_off = 0
        self.init_flag = 0


        #self.read_write_thread = threading.Thread(target=self.stm_update, args=(), daemon=True)
        #self.read_write_thread.start()
        #self.adc_data_lock = threading.Lock()

    def connect(self, serial_num=None):
        """
        connection to the HW-module
        connection parameter can be updated
        :param serial_num: serial_number
        :return: nothing
        """
        if serial_num:
            self.serial_number = serial_num
            self.client.serial_numbers.append(self.serial_number)
        pass
        if self.client.connect() == 1:
            self.state = 1
        else:
            self.state = -1
        return self.state

    def disconnect(self):
        try:
            if self.client.disconnect() == 0:
                self.state = 0
            else:
                self.state = -1
        except AttributeError:
            self.state = -1
            pass
        return self.state

    def init_module(self):
        pass

    def start_continiousread(self):
        if self.client.connection_status:
            self.client.start_continuously_queue_reading(ai=[[2074, 2078]], ao=[], write=[])
        pass

    def voltage_set(self):
        if self.client.connection_status:
           self.client.write_regs(offset=self.register_addr.get("scaler"), data_list=[1, self.voltage_expexted])

        pass
    def voltage_on_off(self):
        if self.client.connection_status:
            self.client.write_regs(offset=self.register_addr.get("on_off"), data_list=[self.on_off])
            self.client.write_regs(offset=self.register_addr.get("scaler"), data_list=[1])
        pass
    def set_calibration(self):
        if self.client.connection_status:
            if self.calibration_1 < 0:
                self.calibration_1 = 65535 + self.calibration_1
            if self.calibration_2 < 0:
                self.calibration_2 = 65535 + self.calibration_2
            self.client.write_regs(offset=self.register_addr.get("calibration_1"), data_list=[self.calibration_1, self.calibration_2])
            self.client.write_regs(offset=self.register_addr.get("flag_new_calibration"), data_list=[1])
            self.client.write_regs(offset=self.register_addr.get("scaler"), data_list=[1])
        pass

    def set_constrain(self):
        if self.client.connection_status:
            self.client.write_regs(offset=self.register_addr.get("overvoltage"), data_list=[self.overvoltage, self.overcurrent])
            self.client.write_regs(offset=self.register_addr.get("flag_new_constrain"), data_list=[1])
            self.client.write_regs(offset=self.register_addr.get("scaler"), data_list=[1])
        pass
    def init_power_module(self):
        self.voltage_expexted  = 27000
        self.overcurrent = 2000
        self.calibration_1 = 0
        self.calibration_2 = 0
        self.on_off = 0
        self.client.write_regs(offset=self.register_addr.get("scaler"), data_list=[1, self.voltage_expexted, self.on_off, self.overvoltage, self.overcurrent, self.calibration_1, self.calibration_2])
        pass



    ''' классная штука чтобы возвращать понятную строку
    def __repr__(self):
        return_str = "oai_kpa_stm module: ser_num %s\n" % self.serial_number
        for adc in range(self.adc_param["adc_num"]):
            return_str += "\t <adc %02d> " % adc
            for ch_num in range(self.adc_param["channel_num"]):
                return_str += "\t %02d: %04.3f" % (ch_num, self.channel_adc_voltage[adc][ch_num])
            return_str += "\n"
        return return_str
    '''

if __name__ == '__main__':
    itteration_num = 0
    power_mod = OaiKpaPower(serial_num="208236A0424D", debug=False)
    print("Connect")
    power_mod.connect()
    power_mod.calibration_1 = 0
    power_mod.calibration_2 = 200
    power_mod.overvoltage = 30000
    #power_mod.set_constrain()
    #power_mod.set_calibration()
    power_mod.voltage_expexted = 22000

    power_mod.on_off = 1
    power_mod.voltage_on_off()
    power_mod.voltage_set()
    while 1:
        power_mod.client.read_regs(target="ai", read_ranges=[[2141, 2143]])
        print(power_mod.client.ai_register_map[2141:2143])
