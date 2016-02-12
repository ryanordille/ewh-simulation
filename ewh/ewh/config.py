from states import TankSize

DESIRED_TEMPERATURE = 75  # in celcius
REGULAR_POWER_LOWER_LIMIT = 70
LOW_POWER_LOWER_LIMIT = 65 # absolute lowest temp (in C) before EWH must turn itself back on
INITIAL_TANK_TEMPERATURE = 20
ACTION_POWER_CONSUMPTION = 1  # power usage when switching state
INSULATION_THERMAL_RESISTANCE = 1

TIME_SCALING_FACTOR = 1
SPECIFIC_HEAT_OF_WATER = 1


class Configuration(object):
    def __eq__(self, given_configuration):
        return self.info() == given_configuration.info()


class ControllerConfiguration(Configuration):
    def __init__(self,
                 power_usage=AVERAGE_KWH,
                 action_power=ACTION_POWER_CONSUMPTION):
        self._kwh = kwh
        self._action_power = action_power

    def info(self):
        return {
            'power_consumption': self.power_consumption,
            'state_change_power_consumption': self.state_change_power_consumption,
        }

    @property
    def power_consumption(self):
        return self._kwh

    @property
    def state_change_power_consumption(self):
        return self._action_power

class HeaterConfiguration(Configuration):
    def __init__(self,
                desired_temperature=DESIRED_TEMPERATURE,
                low_power_temperature=LOW_POWER_LOWER_LIMIT,
                regular_power_temperature=REGULAR_POWER_LOWER_LIMIT,
                tank_size=TankSize.SMALL):
        self._desired_temp = desired_temperature
        self._low_power_temp = low_power_temperature
        self._regular_power_temp = regular_power_temperature

        if tank_size == TankSize.LARGE:
            # 180 liter tank
            self._tank_surface_area = 3.43062  # meters^2
            self._tank_radius = 0.30  # meters
            self._tank_height = 1.52
            self._heating_element_rating = 4.2  # kW
        else:
            # 270 liter tank
            self._tank_surface_area = 2.69172
            self._tank_radius = 0.28
            self._tank_height = 1.25
            self._heating_element_rating = 2.8

    def info(self):
        return {
            'low_power_mode_temperature_lower_limit': self.low_power_temp,
            'desired_temperature': self.desired_temp,
            'regular_mode_temperature_lower_limit': self.regular_power_temp,
            'tank_surface_area': self.tank_surface_area,
            'tank_radius': self.tank_radius,
            'tank_height': self.tank_height,
            'insulation_thermal_resistance': self.insulation_thermal_resistance,
        }

    @property
    def desired_temp(self):
        return self._desired_temp

    @desired_temp.setter
    def desired_temp(self, temp):
        self._desired_temp = temp

    @property
    def low_power_temp(self):
        return self._low_power_temp

    @property
    def regular_power_temp(self):
        return self._regular_power_temp

    @property
    def tank_surface_area(self):
        """Surface area of the outside of the water tank, in square meters"""
        return self._tank_surface_area

    @property
    def tank_radius(self):
        """Radius of the water tank, in meters"""
        return self._tank_radius

    @property
    def tank_height(self):
        """Height of the water tank, in meters"""
        return self._tank_height

    @property
    def initial_tank_temperature(self):
        return self._initial_temperature

    @property
    def insulation_thermal_resistance(self):
        return INSULATION_THERMAL_RESISTANCE

    @property
    def power_input(self):
        """Power input to the tank in btu/hour"""
        return 3412.1 * self._heating_element_rating
