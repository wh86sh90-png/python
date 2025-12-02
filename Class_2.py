# Class_2.py
# Developer 클래스를 정의하려고 하는데, id, name, skill 속성을 추가 하고 싶어
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"Person(id={self.id}, name={self.name})")
class Developer(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        print(f"Developer(id={self.id}, name={self.name}, skill={self.skill})")
def main():
    dev = Developer(1, "Alice", "Python")
    dev.printInfo()
if __name__ == "__main__":
    main()
    