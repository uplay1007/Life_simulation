import random
import sqlite3
import time
from statistics import mean

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from custom_view import CGraphicsScene
from animals import CAnimal
from meal import CMeal


class CWorld(CGraphicsScene):
    def __init__(self, dbname='sim.db'):
        super().__init__()
        self.dbname = dbname

        self.name = "Default"
        self.size_x = 100
        self.size_y = 70
        self.cell_size = 10

        self.anim_size_min = 0.5
        self.anim_size_max = 1.5
        self.anim_straight_min = 1
        self.anim_straight_max = 100
        self.anim_mobility_min = 1
        self.anim_mobility_max = 100
        self.anim_min_age = 100
        self.anim_max_age = 300
        self.anim_male_color = Qt.yellow
        self.anim_female_color = Qt.magenta
        self.anim_gender_bal = 50
        self.anim_health_min = 25
        self.anim_health_max = 50
        self.anim_repl_age_min = 25
        self.anim_repl_age_max = 50
        self.anim_vision_min = 3
        self.anim_vision_max = 7

        self.meal_energy_min = 25
        self.meal_energy_max = 50
        self.meal_freq = 5

        self.load_world()

        self.generation = 0
        # self.anim_num = 0
        # self.anim_repl = 0

        self.animals = []
        self.animals_cache = []

        self.meal_calc = []

        self.create_grid(self.size_x, self.size_y, self.cell_size)
        self.resize_cache()

        self.start = time.time()

    def resize_cache(self):
        if self.animals_cache:
            del self.animals_cache
        self.animals_cache = [[[] for _y in range(self.size_y)] for _x in range(self.size_x)]
        for a in self.animals:
            self.animals_cache[a.x][a.y].append(a)

    def isAvaibleCell(self, x, y):
        a = self.getAnimal(x, y)
        if 0 <= x < self.size_x and 0 <= y < self.size_y and not a:
            return True
        return False

    def getAnimal(self, x, y):
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            for a in self.animals_cache[x][y]:
                if a.kingdom == 'animal':
                    return a
        return None

    def getMeal(self, x, y):
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            for a in self.animals_cache[x][y]:
                if a.kingdom in ['plant', 'meat']:
                    return a
        return None

    def next_gen(self):
        # print(list(map(lambda x: x.age, self.animals)))

        start1 = self.start
        self.start = time.time()
        for a in list(filter(lambda x: x.kingdom == 'animal', self.animals)):
            a.next_gen()
        # Для еды пока не запускаем nextGen

        if self.meal_freq > 0:
            if len(self.meal_calc) == 0:
                self.meal_calc = [1] * self.meal_freq + [0] * (100 - self.meal_freq)
                random.shuffle(self.meal_calc)
                print(self.meal_calc)
            _f = self.meal_calc.pop()

            if self.meal_freq >= 100 or _f == 1:
                q = max(int(round(
                    self.size_x * self.size_y / 500 * (1 + self.meal_freq / 100 if self.meal_freq > 100 else 1), 0)), 1)
                self.generate_random_meals(q, random.randint(self.meal_energy_min, self.meal_energy_max))

        self.end = time.time()
        l = len(self.animals)

        _h = [x.health for x in self.animals if x.kingdom == 'animal']
        if _h:
            avg_health = mean(_h)
        else:
            avg_health = 0
        print(
            f'Gen: {self.generation}, Num: {l}, Delay: {self.start - start1} Dur: {self.end - self.start} Avg: {(self.end - self.start) / l if l != 0 else "NA"} Avg health: {avg_health}')

        self.generation += 1

    def get_available_cells(self):
        all = set()
        for y in range(self.size_y):
            for x in range(self.size_x):
                all.add((x, y))
        for e in self.animals:
            all.discard((e.x, e.y))

        return list(all)

    def generate_random_meals(self, num_meal, energy):
        pole = self.get_available_cells()

        n = min(len(pole), num_meal)
        for i in range(n):
            r = random.randint(0, len(pole) - 1)
            CMeal(pole[r][0], pole[r][1], energy, self)
            del pole[r]

    def generate_random_animals(self, num_anim, repl, helth, max_age, gender_bal, mob, straight, vision):
        pole = []
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.isAvaibleCell(x, y):
                    pole.append((x, y))
        n = min(len(pole), num_anim)
        f = int(round((n * gender_bal / 100), 0))
        m = n - f
        for i in range(f):
            r = random.randint(0, len(pole) - 1)
            ma = random.randint(max_age[0], max_age[1])
            h = round(ma * random.randint(helth[0], helth[1]) / 100)
            CAnimal(pole[r][0], pole[r][1], random.randint(repl[0], repl[1]), h, 'f',
                    ma, random.randint(mob[0], mob[1]),
                    random.randint(straight[0], straight[1]), random.randint(vision[0], vision[1]), self)
            del pole[r]
        for i in range(m):
            r = random.randint(0, len(pole) - 1)
            ma = random.randint(max_age[0], max_age[1])
            h = round(ma * random.randint(helth[0], helth[1]) / 100)
            CAnimal(pole[r][0], pole[r][1], random.randint(repl[0], repl[1]), h, 'm',
                    ma, random.randint(mob[0], mob[1]),
                    random.randint(straight[0], straight[1]), random.randint(vision[0], vision[1]), self)
            del pole[r]

    def redraw(self):
        for anim in self.animals:
            anim.redraw()

    def clear_all(self):
        for i in range(len(self.animals) - 1, -1, -1):
            self.animals[i].kill()
        self.generation = 0
        self.meal_calc = []
        self.redraw()
        self.update()

    def resize(self, size_x, size_y, cell_size):
        self.size_x = size_x
        self.size_y = size_y
        self.cell_size = cell_size

        self.create_grid(self.size_x, self.size_y, self.cell_size)

        animals = list(
            filter(lambda anim: anim.x >= self.size_x or anim.y >= self.size_y, self.animals))
        for i in range(len(animals) - 1, -1, -1):
            animals[i].kill()
        self.resize_cache()
        self.redraw()

    def load_world(self, name="Default"):
        print(name)
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        # rez = cur.execute("""SELECT id, size_x, size_y, size_cell FROM world WHERE id = 1""").fetchall()
        res = cur.execute("""
            SELECT
                id,
                size_x,
                size_y,
                size_cell,
                anim_size_min,
                anim_size_max,
                anim_straight_min,
                anim_straight_max,
                anim_mobility_min,
                anim_mobility_max,
                anim_min_age,
                anim_max_age,
                anim_male_color,
                anim_female_color,
                anim_gender_bal,
                anim_health_min,
                anim_health_max,
                anim_repl_age_min,
                anim_repl_age_max,
                anim_vision_min,
                anim_vision_max, 
                meal_energy_min,
                meal_energy_max,
                meal_freq,
                name
            FROM world
            WHERE name = "{0}"
        """.format(name)).fetchall()
        if res:
            self.size_x = res[0][1]
            self.size_y = res[0][2]
            self.cell_size = res[0][3]
            self.anim_size_min = res[0][4]
            self.anim_size_max = res[0][5]
            self.anim_straight_min = res[0][6]
            self.anim_straight_max = res[0][7]
            self.anim_mobility_min = res[0][8]
            self.anim_mobility_max = res[0][9]
            self.anim_min_age = res[0][10]
            self.anim_max_age = res[0][11]
            self.anim_male_color = res[0][12]
            self.anim_female_color = res[0][13]
            self.anim_gender_bal = res[0][14]
            self.anim_health_min = res[0][15]
            self.anim_health_max = res[0][16]
            self.anim_repl_age_min = res[0][17]
            self.anim_repl_age_max = res[0][18]
            self.anim_vision_min = res[0][19]
            self.anim_vision_max = res[0][20]
            self.meal_energy_min = res[0][21]
            self.meal_energy_max = res[0][22]
            self.meal_freq = res[0][23]
            self.name = res[0][24]
        cur.close()
        con.close()

    def save_world(self):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        cur.execute("""
            UPDATE world SET                                 
                    size_x = ?,
                    size_y = ?,
                    size_cell = ?,
                    anim_size_min = ?,
                    anim_size_max = ?,
                    anim_straight_min = ?,
                    anim_straight_max = ?,
                    anim_mobility_min = ?,
                    anim_mobility_max = ?,
                    anim_min_age = ?,
                    anim_max_age = ?,
                    anim_male_color = ?,
                    anim_female_color = ?,
                    anim_gender_bal = ?,
                    anim_health_min = ?,
                    anim_health_max = ?,
                    anim_repl_age_min = ?,
                    anim_repl_age_max = ?,
                    anim_vision_min = ?,
                    anim_vision_max = ?,
                    meal_energy_min = ?,
                    meal_energy_max = ?,
                    meal_freq = ?                
                WHERE name = "{0}"        
            """.format(self.name), (self.size_x, self.size_y, self.cell_size, self.anim_size_min, self.anim_size_max,
                                    self.anim_straight_min, self.anim_straight_max, self.anim_mobility_min,
                                    self.anim_mobility_max,
                                    self.anim_min_age, self.anim_max_age, QColor(self.anim_male_color).name(),
                                    QColor(self.anim_female_color).name(),
                                    self.anim_gender_bal, self.anim_health_min, self.anim_health_max,
                                    self.anim_repl_age_min,
                                    self.anim_repl_age_max, self.anim_vision_min, self.anim_vision_max,
                                    self.meal_energy_min,
                                    self.meal_energy_max, self.meal_freq
                                    ))
        con.commit()
        cur.close()
        con.close()
