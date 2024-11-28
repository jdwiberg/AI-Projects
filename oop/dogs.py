


class Dog:
    species = 'Canis Familiaris'

    def __init__(self, name, age):
      self.name = name
      self.age = age

    def __repr__(self):
      return f"{self.name} is a {self.age} year old {self.species}."

    def speak(self, sound):
       return f"{self.name} says {sound}."

class JackRussellTerrior(Dog):
   def speak(self, sound='yap'):
      return super().speak(sound)

class Bernedoodle(Dog):
   def speak(self, sound='aroof'):
      return super().speak(sound)

class YellowLab(Dog):
   def speak(self, sound='arf'):
      return super().speak(sound)



gus = Bernedoodle('Gus', 4)
miles = YellowLab('Miles', 7)
print(gus.speak())



