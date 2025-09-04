import pickle

class Mapmanager():
    def __init__(self):
        self.model_file = "block.egg"
        self.texture_file = "images/block.png"
        self.textures = ["images/bedrock.jpg", "images/sand.jpg", "images/ground.jpg", "images/grass.jpg"] # список текстур для блоків дефолтної карти
        self.land = render.attachNewNode("land")

    # Метод, який створює блок у визначеній позиції
    def addBlock(self, position, use_height_texture = False):
        self.block = loader.loadModel(self.model_file)
        # вибираємо текстуру залежно від значення параметра use_height_texture
        if use_height_texture == True:
            z = position[2]
            if z < len(self.textures):
                texture = loader.loadTexture(self.textures[z])
            else:
                texture = loader.loadTexture(self.textures[-1])
        else:
            texture = loader.loadTexture(self.texture_file)
        # встановлюємо блоку вибрану текстуру
        self.block.setTexture(texture)
        self.block.setPos(position)
        self.block.reparentTo(self.land)
        self.block.setTag("block", str(tuple(map(int, position))))  # встановлюємо кожному блоку тег (мітку)

    # метод, який додає блоки на карту, зчитуючи інформацію з текстового файлу
    def loadLand(self, filename):
        with open(filename, "r") as file:
            y = 0
            for line in file:
                x = 0
                line_list = line.split()
                for number in line_list:
                    for z in range(int(number) + 1):
                        self.addBlock((x, y, z), use_height_texture = True)  # вказуємо use_height_texture = True
                    x = x + 1
                y = y + 1


    # метод для встановлення текстури бедроку
    def set_bedrock(self):
        self.texture_file = 'images/bedrock.jpg'
    
    # метод для встановлення текстури трави
    def set_grass(self):
        self.texture_file = 'images/grass.jpg'

    # метод для встановлення звичайної текстури блока
    def set_block(self):
        self.texture_file = 'images/block.png'
    
    def set_brick(self):
        self.texture_file = 'images/brick.png'
    
    def set_grass(self):
        self.texture_file = 'images/grass.jpg'

    def set_ground(self):
        self.texture_file = 'images/ground.jpg'

    def set_sand(self):
        self.texture_file = 'images/sand.jpg'

    def set_stone(self):
        self.texture_file = 'images/stone.png'

    def set_wood(self):
        self.texture_file = 'images/wood.png' 


    # Метод для визначення, чи в координатах coordinates зайнято
    def isEmpty(self, coordinates):
        blocks = self.land.findAllMatches("=block=" + str(coordinates))
        if blocks:
            return False
        else:
            return True
        

    # Метод для визначення найвищого вільноо місця в районі точки з координатами coordinates
    def findHighestEmpty(self, coordinates):
        x, y, z = coordinates
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    
    # Метод для збереження наявної карти у бінарний файл
    def save_map(self):
        # шукаємо всі блоки на карті
        blocks = self.land.getChildren()
        with open("my_map.dat", "wb") as file:
            # зберігаємо кількість блоків у файл
            pickle.dump(len(blocks), file)
            #  зберігаємо координати кожного блока у файл
            for block in blocks:
                x, y, z = block.getPos()
                coordinates = (int(x), int(y), int(z))
                pickle.dump(coordinates, file)


    # Метод для завантаження вже збереженої раніше карти з бінарного файла
    def load_saved_map(self):
        self.land.removeNode()
        self.land = render.attachNewNode("land")

        with open("my_map.dat", "rb") as file:
            amount = pickle.load(file)
            for _ in range(amount):
                coordinates = tuple(pickle.load(file))
                self.addBlock(coordinates)
