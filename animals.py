import math
import random

from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem
from PyQt5.QtCore import Qt

from meal import CMeal
from object import CObject

from functools import reduce


class CAnimal(CObject):
    def __init__(self, x, y, repl, health, gender, max_age, mob, straight, vision, world, parent=None):
        super().__init__(x, y, world, parent)
        self.kingdom = 'animal'
        self.size = world.anim_size_min
        self.gender = gender
        self.health = health
        self.max_age = max_age
        self.repl = repl
        self.last_repl = 0
        self.mobility = mob
        self.vision = vision
        self.straight = straight
        self.color_m = QColor(world.anim_male_color)
        self.color_f = QColor(world.anim_female_color)

        if self.gender == 'm':
            self.brush = QBrush(self.color_m)
        else:
            self.brush = QBrush(self.color_f)
        self.pen = QPen(Qt.darkBlue, 0.1, Qt.SolidLine)
        self.direction = random.randint(1, 8)

        self.viruses = []

        self.body = QGraphicsEllipseItem(self)
        self.body.setPen(self.pen)
        self.body.setBrush(self.brush)
        self.addToGroup(self.body)

        meal = self.world.getMeal(self.x, self.y)
        if meal:
            self.health += meal.energy
            meal.kill()
        # self.redraw()

    def redraw(self):
        s = self.world.cell_size
        self.body.setRect(-s / 2, -s / 2, s, s)
        self.body.setStartAngle(15 * 16)
        self.body.setSpanAngle(330 * 16)
        for i in range(len(self.viruses)):
            self.viruses[i].body.setRect(-s / 4, -s / 4, s / 2, s / 2)
            self.viruses[i].body.setStartAngle((15 + 330 / len(self.viruses) * i) * 16)
            self.viruses[i].body.setSpanAngle(330 / len(self.viruses) * 16)

        self.setRotation((self.direction + 5) * 45)
        self.setPos(self.x * s + s / 2, self.y * s + s / 2)
        self.setScale(self.size)

    def get_next_pos(self):
        if self.direction == 1:
            return (self.x, self.y - 1)
        elif self.direction == 2:
            return (self.x + 1, self.y - 1)
        elif self.direction == 3:
            return (self.x + 1, self.y)
        elif self.direction == 4:
            return (self.x + 1, self.y + 1)
        elif self.direction == 5:
            return (self.x, self.y + 1)
        elif self.direction == 6:
            return (self.x - 1, self.y + 1)
        elif self.direction == 7:
            return (self.x - 1, self.y)
        elif self.direction == 8:
            return (self.x - 1, self.y - 1)
        else:
            return (self.x, self.y)

    def get_direction(self, m):
        v = ((self.x - m.x) ** 2 + (self.y - m.y) ** 2) ** 0.5
        f = (m.x - self.x) / v
        at = math.acos(f) * 180 / math.pi
        if self.y < m.y:
            at = - at + 360
        at = at % 360
        d = (-round(at / 45, 0) + 2) % 8 + 1
        return d

    def next_gen(self):

        # проверяем есть ли поблизости другие организым и заражаем их вирусами.
        for i in range(len(self.viruses) - 1, -1, -1):
            if self.viruses[i].age <= self.viruses[i].duration:
                for a in self.find_animals():
                    if self.viruses[i].inf_gen < self.world.generation:
                        self.viruses[i].attack(a)
            self.viruses[i].next_gen()

        # Определяем направление. Сначала ищем еду и поворачиваемся к ней. иначе поворачиваемся в зависимости от прямолинейности
        next_pos = self.get_next_pos()
        m = self.find_meal(self.vision)
        # if m:
        #    print(f'found meal {m.x,m.y} здоровье {self.health} max_age {self.max_age} Mobility: {self.mobility} ')

        needmeal = False
        isCorrectDir = False
        # print(f'max_age: {self.max_age} age: {self.age} health: {self.health} Mobility: {self.mobility} ' )
        if self.health <= (self.max_age - self.age) * (
                0.1 + self.mobility / 100) and m:  # если усредненно до конца жизни не хватит здоровья, то надо искать еду
            # и если поблизости есть еда, то меняем направление в ее сторону ближайшей. иначе меняем направление рандомно
            needmeal = True
            dir = self.get_direction(m)
            dir_delta = (self.direction - dir) % 8

            # поворот в сторону ближайшей еды. один поворот за одно поколение
            if dir_delta == 4:
                self.direction = (self.direction - 1 + random.choice((-1, 1))) % 8 + 1
            elif dir_delta > 4:
                self.direction = (self.direction - 1 + 1) % 8 + 1
            elif 0 < dir_delta < 4:
                self.direction = (self.direction - 1 - 1) % 8 + 1
            if self.direction == dir:
                isCorrectDir = True  # указывает что направление для движения выбрано правильно

        else:
            if random.randint(1, 100) <= (100 - self.straight) or not self.world.isAvaibleCell(next_pos[0],
                                                                                               next_pos[1]):
                self.direction = (self.direction - 1 + random.choice((-1, 1))) % 8 + 1
            isCorrectDir = True  # когда направление выбираем рандомно то считаем что оно всегда правильное

        # Расчет движения
        if ((random.randint(0, 100) <= self.mobility * (
        2 if needmeal else 1))) and isCorrectDir:  # вероятность движения зависит от мобильности
            next_pos = self.get_next_pos()
            if self.world.isAvaibleCell(next_pos[0], next_pos[1]):
                if self.age - self.last_repl > self.repl and self.gender == 'f' and not self.is_ill() and self.health >= 20:
                    self.last_repl = self.age
                    _mobility = min(self.world.anim_mobility_max,
                                    max(self.world.anim_mobility_min, self.mobility + random.randint(-10, 10)))
                    _straight = min(self.world.anim_straight_max,
                                    max(self.world.anim_straight_min, self.straight + random.randint(-10, 10)))
                    _vision = min(self.world.anim_vision_max,
                                  max(self.world.anim_vision_min, self.vision + random.randint(-1, 1)))
                    _repl = min(self.world.anim_repl_age_max,
                                max(self.world.anim_repl_age_min, self.repl + random.randint(-5, 5)))
                    _max_age = min(self.world.anim_max_age,
                                   max(self.world.anim_min_age, self.max_age + random.randint(-10, 10)))
                    _health = round(
                        _max_age * random.randint(self.world.anim_health_min, self.world.anim_health_max) / 100)
                    _gender = 'f' if random.randint(1, 99) < self.world.anim_gender_bal else 'm'

                    CAnimal(self.x, self.y, _repl, _health, _gender, _max_age, _mobility, _straight, _vision,
                            self.world)
                    self.health -= 20  # во время рождения расходуется здоровье
                self.health -= 1  # для движения расходуется здоровье

                self.move(next_pos[0], next_pos[1])

                # если попалась еда, то поглащаем ее
                meal = self.world.getMeal(self.x, self.y)
                if meal:
                    self.health = min(self.health + meal.energy, self.max_age * 1.5)
                    meal.kill()

        self.age += 1
        self.health -= 0.1  # даже в случае простоя здоровье расходуется

        self.size = self.world.anim_size_min + (self.world.anim_size_max - self.world.anim_size_min) * (
                    self.age / self.max_age)  # размер меняется в зависимости от возраста

        if self.age >= self.max_age or self.health <= 0:  # умираем если достигли возраста или кончилось здоровье
            if self.world.meal_freq > 0:
                CMeal(self.x, self.y, max(1, int(self.world.meal_energy_min / 4)), self.world,
                      'meat')  # после смерти остается маленький кусочек мяса
            self.kill()

    # проверяет наличие определенного вируса в любой файзе
    def has_virus(self, name):
        for virus in self.viruses:
            if name == virus.name:
                return True
        return False

    # если болеет хот одним вирусом
    def is_ill(self):
        for virus in self.viruses:
            if virus.age <= virus.duration:
                return True
        return False

    def damage(self, n):
        self.health -= n

    # ищем всех животных в заданном радиусе
    def find_animals(self, dist=1):
        animals = []
        for _x in range(dist * 2 + 1):
            for _y in range(dist * 2 + 1):
                a = self.world.getAnimal(self.x - dist + _x, self.y - dist + _y)
                if a and a != self and round(((self.x - a.x) ** 2 + (self.y - a.y) ** 2) ** 0.5, 0) <= dist:
                    animals.append(a)
        return animals

    def find_meal(self, dist=1):
        meals = []
        # ищем еду сначала в маленьком квадрате, затем расширяем квадратную зону поиска
        for _d in range(0, dist):
            for _x in range((_d + 1) * 2 + 1):
                m = self.world.getMeal(self.x - _d - 1 + _x, self.y - _d - 1)
                if m:
                    meals.append(m)
                m = self.world.getMeal(self.x - _d - 1 + _x, self.y + _d + 1)
                if m:
                    meals.append(m)
            for _y in range((_d + 1) * 2 - 1):
                m = self.world.getMeal(self.x - _d - 1, self.y - _d + _y)
                if m:
                    meals.append(m)
                m = self.world.getMeal(self.x + _d + 1, self.y - _d + _y)
                if m:
                    meals.append(m)

            # из всей еды в квадрате выбираем только ту, которая попадает в круг
            _meals = list(filter(lambda a: round(((self.x - a.x) ** 2 + (self.y - a.y) ** 2) ** 0.5, 0) <= dist, meals))
            if len(_meals) > 0:
                return _meals[random.randint(0, len(_meals) - 1)]  # если еды несколько, товыбираем любую
        return None
