class QiYue(object):
    def __init__(self):
        self.gender = 'male'
        self.name = 'hippie'
        self.age = 18

    def keys(self):
        # return ('name',)
        # return ['name']
        # return ('name', 'age', 'gender')
        return self.__dict__

    def __getitem__(self, item):
        return getattr(self, item)


o = QiYue()
print(o['name'])
print(o['age'])
print(dict(o))
