class Position:

    def __init__(
            self, position_type, opening_time, opening_rate):
        self.__position_type = position_type
        self.__opening_time = opening_time
        self.__opening_rate = opening_rate
        self.__closing_time = None
        self.__closing_rate = None
        self.__is_open = True
        self.probability = 1.0
        self.position_size = 1

    @property
    def position_type(self):
        return self.__position_type

    @property
    def opening_time(self):
        return self.__opening_time

    @property
    def opening_rate(self):
        return self.__opening_rate

    @property
    def closing_time(self):
        return self.__closing_time

    @property
    def closing_rate(self):
        return self.__closing_rate

    @property
    def is_open(self):
        return self.__is_open
    
    def __str__(self):
        attributes = '{},{},{},{},{}'.format(
            self.__opening_time,
            self.__closing_time,
            self.__opening_rate,
            self.__closing_rate,
            self.__position_type)
        return attributes

    def close(self, closing_time, closing_rate):
        self.__closing_time = closing_time
        self.__closing_rate = closing_rate
        self.__is_open = False

    @classmethod
    def create_positions(cls, strategy, df):
        open_positions, closed_positions = strategy.create_positions(df)
        positions = []

        # 建玉
        for pos in open_positions:
            position = cls(
                position_type=pos['position_type'],
                opening_time=pos['opening_time'],
                opening_rate=pos['opening_rate'])
            positions.append(position)

        # エグジットしたポジション
        for pos in closed_positions:
            position = cls(
                position_type=pos['position_type'],
                opening_time=pos['opening_time'],
                opening_rate=pos['opening_rate'])
            # 建玉は closing_time に None が入っている。closing_rate がない。
            if pos['closing_time']:
                # 建玉の中には、closing_rate が NaN のものもあることに留意。
                position.close(pos['closing_time'], pos['closing_rate'])
            positions.append(position)

        return positions
