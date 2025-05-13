from StatesRepository import StatesRepository

class Launcher:
    repo = StatesRepository()
    repo.add_state("00Q", "computacional", [1, 0])
    repo.add_state("01Q", "computacional", [0, 1])
    repo.save_states("states.csv")

    repo2 = StatesRepository()
    repo2.load_states("states.csv")
    print(repo2.list_states())