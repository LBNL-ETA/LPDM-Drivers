class Light_Data(object):
    def __init__(self, id, timestamp, als, led_power, battery_charge_power, presence, mode, dcharge_power, soc, soh):
        self.id = id
        self.timestamp = timestamp
        self.als = als
        self.led_power = led_power
        self.battery_charge_power = battery_charge_power
        self.presence = presence
        self.mode = mode
        self.discharge_power = dcharge_power
        self.soc = soc
        self.soh = soh