"""
이 파일은 사람을 나타내는 간단한 프로그램이에요.
아주 쉬운 말로 설명하면:

- 사람(Person)은 번호(id)와 이름(name)을 가지고 있어요.
- Manager(관리자)는 사람과 같지만 '직함(title)'이 하나 더 있어요.
- Employee(직원)는 사람과 같지만 '기술(skill)'이 하나 더 있어요.
- printInfo()는 그 사람의 정보를 말해주는 함수예요. (사실은 화면에 출력해요.)

아래에는 예시로 10명의 사람/관리자/직원을 만들어서
각 사람의 정보를 하나씩 말해주는 코드가 있어요.
"""
class Person:
    """
    사람을 나타내는 상자예요.
    아주 쉬운 설명:
    - 이 상자에는 번호(id)와 이름(name)이 있어요.
    - printInfo()를 부르면 '이 사람은 번호 XXX, 이름 YYY예요'라고 말해줘요.
    """
    def __init__(self, id, name):
        # 이 사람의 번호와 이름을 기억해요.
        self.id = id
        self.name = name

    def printInfo(self):
        # 이 사람의 정보를 화면에 보여줘요.
        # 아이에게 말하듯: Person(id=1, name=Alice)
        print(f"Person(id={self.id}, name={self.name})")


class Manager(Person):
    """
    관리자를 나타내는 상자예요. 사람 상자를 물려받아요.
    아주 쉬운 설명:
    - 사람의 번호와 이름도 있고,
    - 거기에 '직함(title)'이 하나 더 있어요.
    - printInfo()를 부르면 '관리자이고 직함은 XXX예요'라고 말해줘요.
    """
    def __init__(self, id, name, title):
        # 먼저 사람의 번호와 이름을 설정해요.
        super().__init__(id, name)
        # 그리고 관리자의 직함을 기억해요.
        self.title = title

    def printInfo(self):
        # 관리자 정보를 화면에 보여줘요.
        print(f"Manager(id={self.id}, name={self.name}, title={self.title})")


class Employee(Person):
    """
    직원을 나타내는 상자예요. 사람 상자를 물려받아요.
    아주 쉬운 설명:
    - 사람의 번호와 이름도 있고,
    - 거기에 '기술(skill)'이 하나 더 있어요.
    - printInfo()를 부르면 '직원이고 기술은 XXX예요'라고 말해줘요.
    """
    def __init__(self, id, name, skill):
        # 먼저 사람의 번호와 이름을 설정해요.
        super().__init__(id, name)
        # 그리고 직원의 기술을 기억해요.
        self.skill = skill

    def printInfo(self):
        # 직원 정보를 화면에 보여줘요.
        print(f"Employee(id={self.id}, name={self.name}, skill={self.skill})")


def main():
    """
    테스트를 실행하는 곳이에요.
    아주 쉬운 설명:
    - 10명의 사람(사람/관리자/직원)을 하나씩 만들어요.
    - 만든 사람들 각각에게 printInfo()를 불러서
      '누구누구의 정보'를 화면에 보여줘요.
    """
    instances = []
    # 명시적 샘플 데이터로 10개 인스턴스 생성
    samples = [
        ("Employee", 1, "Alice", "Python"),
        ("Employee", 2, "Bob", "Java"),
        ("Employee", 3, "Charlie", "Go"),
        ("Person",   4, "Diana"),
        ("Person",   5, "Ethan"),
        ("Person",   6, "Fiona"),
        ("Manager",  7, "Grace", "Engineering Manager"),
        ("Manager",  8, "Henry", "Sales Manager"),
        ("Manager",  9, "Irene", "HR Manager"),
        ("Employee",10, "Jack", "C++"),
    ]

    for s in samples:
        if s[0] == "Employee":
            _, id, name, skill = s
            instances.append(Employee(id, name, skill))
        elif s[0] == "Manager":
            _, id, name, title = s
            instances.append(Manager(id, name, title))
        else:
            _, id, name = s
            instances.append(Person(id, name))

    # 만든 사람들 모두에게 '이 사람은 누구다'를 말하게 해요.
    for obj in instances:
        obj.printInfo()


if __name__ == "__main__":
    main()