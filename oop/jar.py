

class Jar():
    def __init__(self, contains, quantity):
        self.contains = contains
        self.quantity = quantity

    def __repr__(self):
        return f"This jar contains {self.quantity} {self.contains}"

class BeanContainer(Jar):
    def __init__(self, contains, quantity, bean_type):
        super().__init__(contains, quantity)
        self.bean_type = bean_type

    def __repr__(self):
        return f"Jar contains {self.quantity} {self.bean_type}."

cookie_jar = Jar('cookies', 17)
bean_jar = BeanContainer('beans', 113, 'cocoa beans')
pill_jar = Jar('pills', 98)

print(bean_jar)
