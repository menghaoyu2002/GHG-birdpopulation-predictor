import csv
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class GreenhouseGas:
    """ dataclass representing greenhouse gas emissions of a region in a given year

    Instance Attributes:
     - year: year of the given data
     - region: region of the given data
     - co2: amount of co2 emissions in the given year for the given region
     - ch4: amount of ch4 emissions in the given year for the given region
     - hfc: amount of HPC emissions in the given year for the given region
     - pfc: amount of PFC emissions in the given year for the given region
     - sf6: amount of sf6 emissions in the given year for the given region
     - nf3: amount of nf3 emissions in the given year for the given region
     - total: the total amount of greenhouse gas emissions in data
    """
    year: int
    region: str
    co2: float
    ch4: float
    n2o: float
    hfc: float
    pfc: float
    sf6: float
    nf3: float
    total: float


class Province:
    """ A class representing the greenhouse gas emission data of a specific region
    in Canada (a province or territory)

    Instance attributes:
     - name: name of the region of the given data
     - co2: a list representing the amount of co2 emissions for the given
            region in chronological order
     - ch4: a list representing the amount of ch4 emissions for the given
            region in chronological order
     - hfc: a list representing the amount of hfc emissions for the given
            region in chronological order
     - pfc: a list representing the amount of pfc emissions for the given
            region in chronological order
     - sf6: a list representing the amount of sf6 emissions for the given
            region in chronological order
     - nf3: a list representing the amount of nf3 emissions for the given
            region in chronological order
     - total: the total amount of greenhouse gas emissions in data

    Representation Invariants:
     - self.name != ''
     - all(value <=  for value in self.co2)
    """

    # Private Attributes
    _data: List[GreenhouseGas]  # total GHG data
    _dict_data: Dict[int, float]  # mapping of year to GHG emissions for that year

    # Public Attributes
    name: str
    co2: List[float]
    ch4: List[float]
    n2o: List[float]
    hfc: List[float]
    pfc: List[float]
    sf6: List[float]
    nf3: List[float]
    total: List[float]

    def __init__(self, data: List[GreenhouseGas]) -> None:
        self.name = data[0].region
        self._data = data
        self._dict_data = self._sort_ghg_data()

        self.co2 = self.adjust_list(1990, 2016, 0)
        self.ch4 = self.adjust_list(1990, 2016, 1)
        self.n2o = self.adjust_list(1990, 2016, 2)
        self.hfc = self.adjust_list(1990, 2016, 3)
        self.pfc = self.adjust_list(1990, 2016, 4)
        self.sf6 = self.adjust_list(1990, 2016, 5)
        self.nf3 = self.adjust_list(1990, 2016, 6)
        self.total = self.adjust_list(1990, 2016, 7)

    def _sort_ghg_data(self) -> Dict[int, GreenhouseGas]:
        """ Return a dictionary mapping year to a list of greenhouse gas
        emissions for that year

        Note: This is a private method used only to initialize _dict_data.
        """
        sorted_dict = {}
        for row in self._data:
            sorted_dict[row.year] = [row.co2,
                                     row.ch4,
                                     row.n2o,
                                     row.hfc,
                                     row.pfc,
                                     row.sf6,
                                     row.nf3,
                                     row.total]

        return sorted_dict

    def adjust_list(self, start: int, end: int, index: int) -> List[float]:
        """ Return a list representing the data of a specific greenhouse gas
        emissions for self, which starts from <start> year and ends on <end> year.

        The index is based off of the order which the greenhouse gasses appear
        in the dictionary values.

        That is:
         - co2 = 0
         - ch4 = 1
         - n20 = 2
         - hfc = 3
         - pfc = 4
         - sf6 = 5
         - nfc = 6
         - total = 7

        Preconditions:
         - 0 <= index < 8
         - start < end
         - 1990 <= start <= 2016
         - 1990 <= end <= 2016
        """
        trimmed_list = []
        for year in range(start, end + 1):
            trimmed_list.append(self._dict_data[year][index])

        return trimmed_list


class Bird:
    """ An class representing a the data of a bird species

    Instance Attributes:
     - dict_data: mapping of year to index of change since 1970 for
                  the given bird species

     - list_data: list of all indexes of change since 1970,
                  ordered by year (oldest data to most recent)

    Representation Invariants:
     - min(self.dict_data) == 1990
     - max(self.dict_data) == 2016
     - all(is_instance(self.dict_data[year], float) or self.dict_data[year] == 'n/a'
           for year in self.dict_data)
     - all(element in self.dict_data.values() element in self.list_data)

    Sample Usage:
    >>> bird_data = {year: year for year in range(1990, 2017)}
    >>> bird = Bird(bird_data)
    >>> bird.dict_data == {year: year for year in range(1990, 2017)}
    True
    >>> bird.list_data == [n for n in range(1990, 2017)]
    True
    """
    dict_data: Dict[int, any]  # where any is either a float or 'n/a'
    list_data: list

    def __init__(self, bird_data: dict) -> None:
        self.dict_data = bird_data
        self.list_data = self._data_to_list()

    def trim_data(self, start: int, end: int) -> None:
        """ Create a new dict that contains all bird data from the year <start> to
        the year <end> and reassign self.data to it.

        Note: After the data is trimmed it cannot be reverted or untrimmed.

        Preconditions:
         - start < end
         - 1970 <= end <= 2016
         - 1970 <= start <= 2016

        >>> bird_data = {year: 0.0 for year in range(1990, 2017)}  # an example possible data
        >>> bird = Bird(bird_data)
        >>> bird.trim_data(2000, 2001)
        >>> bird.dict_data
        {2000: 0.0, 2001: 0.0}
        """
        self.dict_data = {year: self.dict_data[year] for year in range(start, end + 1)}

        # updates the list attribute to match the trimmed data
        self.list_data = self._data_to_list()

    def find_first_point(self) -> int:
        """ Return the first year where the data is not 'n/a'

        >>> bird_data = {year: 'n/a' for year in range(1990, 2016)}
        >>> bird_data[2016] = 0.0
        >>> bird = Bird(bird_data)
        >>> bird.find_first_point()
        2016
        """
        for year in self.dict_data:
            if self.dict_data[year] != 'n/a':
                return year

    def _data_to_list(self) -> list:
        """ Return a list containing all the datapoints in data ordered by year

        This is a private method used to initialize list_data

        The function isn't for the user to use. The doctest below is just to exemplify
        how the function works.

        >>> bird = Bird({2002: 0.0, 2003: 1.0, 2004: 2.0})
        >>> bird.list_data
        [0.0, 1.0, 2.0]
        >>> bird.trim_data(2002, 2003)
        >>> bird.list_data
        [0.0, 1.0]
        """
        start = min(self.dict_data)
        end = max(self.dict_data) + 1
        return [self.dict_data[year] for year in range(start, end)]


def read_ghg_data(last_row: int) -> List[GreenhouseGas]:
    """ Return a mapping of province names to a list of GreenhouseGas instances,
    where each instance in the list represents a row in the data set.

    The function will read <last_row> number of rows

    Note: The list of GreenhouseGas are ordered by year
    """
    with open('GHG.csv') as csvfile:
        reader = csv.reader(csvfile)
        ghg_data = {}

        # skips header
        next(reader)

        # reads each row in the dataset, up to the <last_row> row
        for _ in range(last_row):
            row = next(reader)
            province = row[1]

            if province  in ghg_data:
                ghg_data[province].append(GreenhouseGas(year=int(row[0]),
                                                        region=row[1],
                                                        co2=float(row[5]),
                                                        ch4=float(row[6]),
                                                        n2o=float(row[8]),
                                                        hfc=float(row[10]),
                                                        pfc=float(row[11]),
                                                        sf6=float(row[12]),
                                                        nf3=float(row[13]),
                                                        total=float(row[14])))
            else:
                ghg_data[province] = [GreenhouseGas(year=int(row[0]),
                                                    region=row[1],
                                                    co2=float(row[5]),
                                                    ch4=float(row[6]),
                                                    n2o=float(row[8]),
                                                    hfc=float(row[10]),
                                                    pfc=float(row[11]),
                                                    sf6=float(row[12]),
                                                    nf3=float(row[13]),
                                                    total=float(row[14]))]

    return ghg_data


def read_bird_data() -> Dict[int, str]:
    """ Read the 'bird_data.csv' file and Return a dictionary
    mapping each year to a list of
    """
    with open('bird_data.csv') as csvfile:
        reader = csv.reader(csvfile)
        # skips headers
        for _ in range(3):
            next(reader)

        bird_data = {}

        for _ in range(47):
            row = next(reader)
            bird_data[int(row[0])] = [row[1],
                                      row[2],
                                      row[3],
                                      row[4],
                                      row[5],
                                      row[6],
                                      row[7],
                                      row[8],
                                      row[9]]
    return bird_data


def filter_bird_data(bird_data: Dict[int, str], column: int) -> Dict[int, any]:
    """ Return a dictionary mapping the years in bird_data to a
    specific column in the data

        Preconditions:
         - 0 <= column <= 8

    >>> filter_bird_data({2002: ['0.0', '1.0', '2.0', '3.0', '4.0', '5.0'],\
                          2003: ['0.0', '1.0', '2.0', '3.0', '4.0', '5.0'] }, 0)
    {2002: 0.0, 2003: 0.0}
    >>> filter_bird_data({2002: ['0.0', '1.0', '2.0', '3.0', '4.0', '5.0'],\
                          2003: ['n/a', '1.0', '2.0', '3.0', '4.0', '5.0'] }, 0)
    {2002: 0.0, 2003: 'n/a'}
    """
    filtered_dict = {}
    for year in bird_data:
        column_data = bird_data[year][column]
        if column_data != 'n/a':
            filtered_dict[year] = float(column_data)
        else:
            filtered_dict[year] = 'n/a'

    return filtered_dict


if __name__ == '__main__':
#     import python_ta
#     python_ta.check_all(config={
#         'max-line-length': 100,
#         'extra-imports': ['python_ta.contracts', 'dataclasses', 'datetime'],
#         'disable': ['R1705', 'C0200'],
#     })

#     import python_ta.contracts
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()