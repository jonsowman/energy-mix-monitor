import urequests as requests
import ujson as json
import network


class EnergySource(object):
    """
    An EnergySource is a fuel and the current fraction of UK supply for which
    it is responsible.
    """
    def __init__(self, fuel, percent):
        self.fuel = fuel
        self.percent = percent

    def __str__(self):
        return "{}: {}%".format(self.fuel, self.percent)


class EnergyMix(object):
    """
    An EnergyMix is a collection of EnergySource objects comprising the
    total UK energy mix.
    """
    def __init__(self):
        self.sources = []

    def percent(self, fuel):
        try:
            return [s.percent for s in self.sources if s.fuel == fuel][0]
        except IndexError:
            return 0

    def from_json(self, json):
        for source in json['data']['generationmix']:
            self.sources.append(EnergySource(fuel=source['fuel'],
                percent=source['perc']))

    def __str__(self):
        return "\n".join([str(s) for s in self.sources])


class EnergyIntensity(object):
    def __init__(self):
        self.current = 0
        self.forecast = 0

    def from_json(self, json):
        self.current = json['data'][0]['intensity']['actual']
        self.forecast = json['data'][0]['intensity']['forecast']

    def __str__(self):
        return "Current carbon intensity {}g/kWh (versus {}g/kWh forecast)".format(
                self.current, self.forecast)

def mix():
    r = requests.get('https://api.carbonintensity.org.uk/generation')
    mix = EnergyMix()
    mix.from_json(json.loads(r.text))
    return mix

def intensity():
    r = requests.get('https://api.carbonintensity.org.uk/intensity')
    ci = EnergyIntensity()
    ci.from_json(json.loads(r.text))
    return ci

