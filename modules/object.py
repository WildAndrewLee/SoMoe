class Object(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self)

        for x in args:
            kwargs.update(x)

        self.update(kwargs)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError

    def __setattr__(self, name, val):
        self[name] = val

    def update(self, val):
        for key in val:
            if isinstance(val[key], dict):
                self[key] = Object(val[key])
            elif isinstance(val[key], list):
                self[key] = []

                for x in val[key]:
                    self[key].append(Object(x))
            else:
                self[key] = val[key]

        self.__dict__.update(self)
