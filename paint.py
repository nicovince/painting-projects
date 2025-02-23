class Paint:
    def __init__(self, manufacturer, painttype, name, colorcode):
        self.manufacturer = manufacturer
        self.painttype = painttype
        self.name = name
        self.colorcode = colorcode

    @classmethod
    def placeholder(cls, name):
        return cls("ToBuy", "unknown Type", name, 0x00FF00)


