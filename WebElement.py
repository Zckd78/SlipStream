class WebElement():
    def __init__(self, name, type, props):
        # Stuff will go here someday...
        self.eName = name
        self.eType = type
        self.eProps = props

    @property
    def Name(self):
        return self.eName

    @property
    def Type(self):
        return self.eType

    @property
    def Props(self):
        return self.eProps


