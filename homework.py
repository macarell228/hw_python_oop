class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, mean_speed, calor):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = mean_speed
        self.calories = calor

    def get_message(self):
        print(f'Тип тренировки: {self.training_type}; '
              f'Длительность: {self.duration} ч.; '
              f'Дистанция: {self.distance} км; '
              f'Ср. скорость: {self.speed} км/ч; '
              f'Потрачено ккал: {self.calories}')


class Training:
    """Базовый класс тренировки."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self, LEN_STEP) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / 1000

    def get_mean_speed(self, LEN_STEP) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_result = self.get_distance(LEN_STEP) / self.duration
        return mean_speed_result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, training_type, LEN_STEP):
        info_message = InfoMessage(training_type, self.duration,
                                   self.get_distance(LEN_STEP),
                                   self.get_mean_speed(LEN_STEP),
                                   self.get_spent_calories())
        return info_message.get_message()


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed(self.LEN_STEP)
                + (self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / 1000 * (self.duration * 60))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65

    def __init__(self, action, duration, weight, height):
        super(SportsWalking, self).__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        some_thing1 = 0.035
        km = 1000
        one_hour = 3600
        LEN_STEP = 0.65
        a = some_thing1 * self.weight + (self.get_mean_speed(LEN_STEP))
        b = (a * km / one_hour) ** 2 / (self.height * 0.029
        * self.weight * self.duration)
        return b


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, pool_lenth, count_pool):
        super(Swimming, self).__init__(action, duration, weight)
        self.pool_lenth = pool_lenth
        self.count_pool = count_pool

    def get_mean_speed(self, len_step) -> float:
        a = self.pool_lenth * self.count_pool / 1000 / self.duration
        return a

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        a = (self.get_mean_speed(self.LEN_STEP) + 1.1) * 2
        return a * self.weight * self.duration


def read_package(workout_type, data):
    """Прочитать данные полученные от датчиков."""
    diction = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    workout = diction[workout_type]
    return workout(*data)


def main(training) -> None:
    """Главная функция."""
    if workout_type == 'SWM':
        training.show_training_info(workout_type, 1.38)
    elif workout_type == 'RUN' or workout_type == 'WLK':
        training.show_training_info(workout_type, 0.65)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
