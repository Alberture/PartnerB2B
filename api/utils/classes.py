class PartnerUserWrapper:
    """
        Since I'm using django JWT I need to pass a User-like object to the RefreshToken object
        because the RefreshToken object is based on the User object.
        Excepted that instead of a User id it will be a Partner id here.
    """
    def __init__(self, id): 
        self.id = id

    @property
    def is_active(self): return True  # required by JWT