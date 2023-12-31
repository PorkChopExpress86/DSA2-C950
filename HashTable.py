class HashTable:
    """Custom python class that will create a hash table of some size (13 by default). Python's hash function is used
    to create the hash quickly. A prime number for size should be used to minimize collisions.
    Insert if O(1) look-ups are O(n) in worst case, but O(1) in best case.
    """

    def __init__(self, size=31):
        """Initialize the hashtable with an empty list of the size

        :param size:  of the list. Recommended to be a prime number
        to properly reduce collisions.
        """
        self.data_map: list = [None] * size
        self.size = size
        self.entries = 0
        self.load_factor = self.entries / self.size

    def __hash(self, key: int) -> int:
        """Creates a hash of the key
        :param key: id or key of item
        :return: integer of the bucket for the hash table
        """
        return key % len(self.data_map)

    def insert(self, key: int, value) -> None:
        """Insert a package in the hashtable
        :param key: package id
        :param value: the package object
        :return: None
        Big(O): O(1)"""
        index = self.__hash(key)
        if self.data_map[index] is None:
            self.data_map[index] = []
        self.data_map[index].append([key, value])
        self.entries += 1

    def get_item(self, key: int):
        """Return an item from the hash table using the id of the package
        :param key: id of the pacakge
        :return Package: if found a package object will be returned
        Big(O): O(n)"""
        # get the index
        index = self.__hash(key)
        # if the address is not none
        if self.data_map[index] is not None:
            # loop over the items
            for i in range(len(self.data_map[index])):
                # check if the key matches
                if self.data_map[index][i][0] == key:
                    # if there is a match, then return the value
                    return self.data_map[index][i][1]
        return None

    def remove_item(self, key: int) -> None:
        """Remove item from the hash table
        :param key: integer of the package id
        :return: None
        Big(O): O(n)"""
        index = self.__hash(key)
        if self.data_map[index] is not None:
            for i in range(len(self.data_map[index])):
                if self.data_map[index][i][0] == key:
                    del self.data_map[index][i]

    def keys(self) -> list:
        """Get a list of all the keys in the hash table
        :return list: of all keys
        Big(O): O(n^2)"""
        all_keys = []
        # Loop over all the indexes
        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for j in range(len(self.data_map[i])):
                    all_keys.append(self.data_map[i][j][0])
        return all_keys

    def print_table(self) -> None:
        for i, val in enumerate(self.data_map):
            print(i, ": ", val)

    def get_number_of_packages(self) -> int:
        """Get the number of packages available in the hash table
        Big(O):O(n^2) since it will call the keys function"""
        return max(self.keys())


# pytest
def fill_hash_table():
    test_data = [
        [1, "Citizen Kane - 1941"],
        [2, "Casablanca - 1942"],
        [3, "The Godfather - 1972"],
        [4, "Gone with the Wind - 1939"],
        [5, "Lawrence of Arabia - 1962"],
    ]

    my_hash_table = HashTable(4)

    for row in range(len(test_data)):
        my_hash_table.insert(test_data[row][0], test_data[row][1])

    # my_hash_table.print_table()
    return my_hash_table


def test_get_items():
    my_hash_table = fill_hash_table()
    assert my_hash_table.get_item(1) == "Citizen Kane - 1941"
    assert my_hash_table.get_item(2) == "Casablanca - 1942"
    assert my_hash_table.get_item(3) == "The Godfather - 1972"
    assert my_hash_table.get_item(4) == "Gone with the Wind - 1939"
    assert my_hash_table.get_item(5) == "Lawrence of Arabia - 1962"
    assert max(my_hash_table.keys()) == 5
    assert my_hash_table.get_number_of_packages() == 5
