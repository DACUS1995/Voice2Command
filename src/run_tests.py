from components import tests as components_tests
from commands import tests as commands_tests

def main():
    components_tests.run_all_tests()
    commands_tests.run_all_tests()

if __name__ == "__main__":
    main()