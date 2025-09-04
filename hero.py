class Hero():
    def __init__(self, posititon, map):
        self.map = map
        self.hero_model = loader.loadModel("smiley")
        self.hero_model.reparentTo(render)
        self.hero_model.setPos(posititon)
        self.hero_model.setScale(0.3)
        self.camera_on = 0
        self.main_mode = False
        self.camera_bind()
        self.accept_event()
        self.mouse_pos_x = None                                     # властивість, яка зберігатиме позицію мишки по х
        self.mouse_pos_y = None                                     # властивість, яка зберігатиме позицію мишки по у
        taskMgr.add(self.mouse_control_task, "mouse_control_task")  # додаємо нове завдання Менеджеру завдань


    # Завдання, яке виконується на кожному кадрі ігрвого цикла
    def mouse_control_task(self, task):
        if self.camera_on == 1 or self.camera_on == 2:
            # якщо мишка активна і знаходиться у вікні - викликаємо метод для обробки її руху
            if base.mouseWatcherNode.hasMouse():
                self.handle_mouse_position()
        return task.cont


    # Метод, який реагує на рух миші, щоб повертати гравця
    def handle_mouse_position(self):
        # Перевіряємо, чи збережена попередня позиція мишки
        if self.mouse_pos_x is not None and self.mouse_pos_y is not None:
            # отримуємо зміну положення мишки по горизонталі і по вертикалі
            dx = base.mouseWatcherNode.getMouseX() - self.mouse_pos_x
            dy = base.mouseWatcherNode.getMouseY() - self.mouse_pos_y
        
            if dx > 0.01:
                self.turn_right()
            elif dx < -0.01:
                self.turn_left()

            if dy > 0.01:
                self.turn_down(-dy)
            elif dy < -0.01:
                self.turn_up(dy)

        # Після обробки руху мишки відцентруємо її в ігровому вікні 
        base.win.movePointer(0, base.win.getXSize() // 2, base.win.getYSize() // 2)
        # Скидаємо логічну х-координату та у-координату мишки на 0
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0

    # нахил вниз
    def turn_down(self, dy):
        new_angle = self.hero_model.getP() + dy * 100
        new_angle = max(-90, min(90, new_angle))
        self.hero_model.setP(new_angle)

    # нахил вгору
    def turn_up(self, dy):
        new_angle = self.hero_model.getP() - dy * 100
        new_angle = max(-90, min(90, new_angle))
        self.hero_model.setP(new_angle)

    # метод для закріплення камери на гравці (від 1-го лиця)
    def camera_bind(self):
        # вимикаємо керування камерою за допомогою мишки
        base.disableMouse()
        # поворот камери на 180 градусів
        base.camera.setH(180)   
        # прив'язуємо камеру до гравця
        base.camera.reparentTo(self.hero_model)
        # встановлюємо камеру в задані координати
        base.camera.setPos(0, 0, 1.5)
        # властивість яка показує, що камера закрілена на гравці
        self.camera_on = 1

    # метод для закріплення камери на гравці (від 3-го лиця)
    def camera_bind_third(self):
        # встановлюємо камеру в задані координати
        base.camera.setPos(0, 15, 3)
        self.camera_on = 2

    # метод для відкріплення камери від гравця
    def camera_unbind(self):
        base.enableMouse()
        base.camera.reparentTo(render)
        self.camera_on = False

    # метод для зміни розташування камери
    def change_view(self):
        if self.camera_on == 0:
            self.camera_bind()
        elif self.camera_on == 1:
            self.camera_bind_third()
        elif self.camera_on == 2:
            self.camera_unbind()
           
    # метод для повороту вліво
    def turn_left(self):
        new_angle = (self.hero_model.getH() + 5) % 360
        self.hero_model.setH(new_angle)
    
    # метод для повороту вправо
    def turn_right(self):
        new_angle = (self.hero_model.getH() - 5) % 360
        self.hero_model.setH(new_angle)

    # Метод, що дозволяє розділяти види рухів в різних ігрових режимах
    def move_to(self, angle):
        if self.main_mode == False:
            self.just_move(angle)
        else:
            self.try_move(angle)

    # Метод для переміщення гравця в режимі спостерігача
    def just_move(self, angle):
        new_coordinates = self.look_at(angle)
        self.hero_model.setPos(new_coordinates)

    # Метод, що повертає координати, в які переміститься гравець, якщо зробить крок у напрямку кута angle
    def look_at(self, angle):
        x = round(self.hero_model.getX())
        y = round(self.hero_model.getY())
        z = round(self.hero_model.getZ())
        dx, dy = self.check_dir(angle)
        return (x+dx, y+dy, z)

    # Метод, що повертає зміни координат x та у, відповідні переміщенню у бік кута angle
    def check_dir(self, angle):
        if angle >=0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)
        
    # Метод руху вперед
    def forward(self):
        angle = self.hero_model.getH()
        self.move_to(angle)

    # Метод руху назад
    def back(self):
        angle = (self.hero_model.getH() + 180) % 360
        self.move_to(angle)

    # Метод руху вліво
    def left(self):
        angle = (self.hero_model.getH() + 90) % 360
        self.move_to(angle)

    # Метод руху вправо
    def right(self):
        angle = (self.hero_model.getH() + 270) % 360
        self.move_to(angle)

    # Метод для переміщення гравця в основному ігровому режимі
    def try_move(self, angle):
        coordinates = self.look_at(angle)
        # якщо в цих coordinates вільно
        if self.map.isEmpty(coordinates):
            # можливо треба впасти вниз (знаходимо координати найвищого вільного місця)
            empty_coordinates = self.map.findHighestEmpty(coordinates)
            self.hero_model.setPos(empty_coordinates)
        # якщо в цих coordinates зайнято
        else:
            # можливо треба залізти на один блок вище
            new_coordinates = (coordinates[0], coordinates[1], coordinates[2] + 1)
            if self.map.isEmpty(new_coordinates):
                self.hero_model.setPos(new_coordinates)

    # Метод для руху вгору (тільки в режимі спостерігача)
    def up(self):
        if self.main_mode == False:
            self.hero_model.setZ(self.hero_model.getZ() + 1)

    # Метод для руху вниз (тільки в режимі спостерігача)
    def down(self):
        if self.main_mode == False:
            self.hero_model.setZ(self.hero_model.getZ() - 1)

    # Метод для перемикання ігрового режиму на протилежний
    def change_mode(self):
        if self.main_mode == False:
            self.main_mode = True
        else:
            self.main_mode = False

    # Метод для будування блоків
    def build(self):
        angle = self.hero_model.getH()
        coordinates = self.look_at(angle) # координати в яких потенційно будемо ставити блок
        # В залежності від режима логіка будування різна
        if self.main_mode == False:
            self.map.addBlock(coordinates)
        else:
            # шукаємо найвище вільне місце
            highest_empty_coord = self.map.findHighestEmpty(coordinates)
            if highest_empty_coord[2] <= coordinates[2] + 1:
                self.map.addBlock(highest_empty_coord)

    # Метод для руйнування блоків
    def destroy(self):
        angle = self.hero_model.getH()
        coordinates = self.look_at(angle) # координати в яких потенційно будемо видаляти блок
        print(f"Точка перед гравцем: {coordinates}")
        if self.main_mode == False:
            # перевряємо наявність блоків в точці coordinates
            blocks = self.map.land.findAllMatches("=block=" + str(coordinates))
            print(f"Блоки в точці {coordinates}: {blocks}")
            # через цикл перебираємо знайдені блоки та видялємо їх вузли
            for block in blocks:
                block.removeNode()
        else:
            # шукаємо координати найвищого вільного місця
            x, y, z = self.map.findHighestEmpty(coordinates)
            # під ним 100% буде стояти блок
            new_positon = (x, y, z-1)
            blocks = self.map.land.findAllMatches("=block=" + str(new_positon))
            for block in blocks:
                block.removeNode()

    # метод для підключення подій
    def accept_event(self):
        # зберігання карти
        base.accept("k", self.map.save_map)
        # завантаження раніше збереженої карти
        base.accept("l", self.map.load_saved_map)
        # будуванння блоків
        base.accept("b", self.build)
        # руйнування блоків
        base.accept("n", self.destroy)
        # перемикання режиму
        base.accept("m", self.change_mode)
        # рух вгору\вниз
        base.accept("arrow_up", self.up)
        base.accept("arrow_up-repeat", self.up)
        base.accept("arrow_down", self.down)
        base.accept("arrow_down-repeat", self.down)
        # перемикання камери
        base.accept("c", self.change_view)
        # повороти вліво\вправо
        base.accept("arrow_left", self.turn_left)
        base.accept("arrow_left-repeat", self.turn_left)
        base.accept("arrow_right", self.turn_right)
        base.accept("arrow_right-repeat", self.turn_right)
        # рух вперед
        base.accept("w", self.forward)
        base.accept("w-repeat", self.forward)
        # рух назад
        base.accept("s", self.back)
        base.accept("s-repeat", self.back)
        # рух вліво
        base.accept("a", self.left)
        base.accept("a-repeat", self.left)
        # рух вправо
        base.accept("d", self.right)
        base.accept("d-repeat", self.right)
        # встановлення текстур
        base.accept("1", self.map.set_bedrock)
        base.accept("2", self.map.set_grass)
        base.accept("3", self.map.set_block)
        base.accept("4", self.map.set_brick)
        base.accept("5", self.map.set_grass)
        base.accept("6", self.map.set_ground)
        base.accept("7", self.map.set_sand)
        base.accept("8", self.map.set_stone)
        base.accept("9", self.map.set_wood)


