class InfoMessage:
    """Информационное сообщение о тренировке."""
    INFO_DIGIT_FORMAT = 3

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: '
                f'{self.duration:.{self.INFO_DIGIT_FORMAT}f} ч.; '
                f'Дистанция: {self.distance:.{self.INFO_DIGIT_FORMAT}f} км; '
                f'Ср. скорость: {self.speed:.{self.INFO_DIGIT_FORMAT}f} км/ч; '
                f'Потрачено ккал: {self.calories:.{self.INFO_DIGIT_FORMAT}f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    MIN_IN_H = 60
    LEN_STEP = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self, LEN_STEP=LEN_STEP) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / self.M_IN_KM

    def get_mean_speed(self, LEN_STEP=LEN_STEP) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_result = self.get_distance(LEN_STEP) / self.duration
        return mean_speed_result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, training_type="Swimming", LEN_STEP=LEN_STEP):
        info_message = InfoMessage(training_type, self.duration,
                                   self.get_distance(LEN_STEP),
                                   self.get_mean_speed(LEN_STEP),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    WORKOUT_TYPE = "Running"

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WORKOUT_TYPE = "SportsWalking"
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float):
        super(SportsWalking, self).__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        a = self.get_mean_speed() * self.KMH_IN_MSEC
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (a**2 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    WORKOUT_TYPE = "Swimming"
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int):
        super(Swimming, self).__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self, LEN_STEP=LEN_STEP) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed(self.LEN_STEP)
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


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

    info = training.show_training_info(
        training.WORKOUT_TYPE, training.LEN_STEP)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
