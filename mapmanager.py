import pickle

class Mapmanager():
    def __init__(self):
        # модель кубика лежить у файлі block.egg
        self.model = 'block.egg' 
        # використовуємо таку текстуру
        self.texture = 'block.png'        
        self.colors = [
           (0.2, 0.2, 0.35, 1),
           (0.2, 0.5, 0.2, 1),
           (0.7, 0.2, 0.2, 1),
           (0.5, 0.3, 0.0, 1)
        ] #rgba
        # створюємо основний вузол карти
        self.startNew()


   #Метод, що створює основу для нової карти
    def startNew(self):
        self.land = render.attachNewNode("Land") # вузол, до якого прив'язані всі блоки картки
   

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]
  
  
    def addBlock(self, position):
        # створення моделі
        self.block = loader.loadModel(self.model)
        # закріплення текстури на моделі
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        # встановлення кольору моделі
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        # додавння до блоку тегу та значення тегу (його позиція)   
        self.block.setTag("at", str(position))
        #прив'язуємо блок до вузла land
        self.block.reparentTo(self.land)


   #Метод, що обнуляє карту
    def clear(self):
        self.land.removeNode()
        self.startNew()


   #Метод, що створює карту землі з текстового файлу, повертає її розміри
    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                       block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y
    

    # Метод дозволяє знайти всі блоки, що знаходяться за координатою pos 
    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos)) #знаходимо всі можливі об'єкти, які оточують точку
                                                           #потеційно, ця точка - позиція нашого героя 
    

    # Метод для визначення, чи зайнятий перед нами блок   
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos) #викликаємо верхню функцію, дізнаємось чи є блоки навколо точки
                                      #отримуємо список блоків
        if blocks: #якщо список blocks не порожній
            return False #повертаємо False (навколо точки НЕ порожньо)
        else: 
            return True #інакше - повертаємо True (навколо точки порожньо)


    # Метод для визначення верхнього незайнятого блоку     
    def findHighestEmpty(self, pos):
        x, y, z = pos #дізнаємось позиції точки
        z = 1 #починаємо рух з 1
        while not self.isEmpty( (x, y, z) ): #через цикл шукаємо точку по висоті, де не буде жодного блоку 
            z += 1 #збільшуємо висоту поки не дійдемо до порожньої точки
        #цикл зупиниться як тільки  ми знайдемо порожню точку
        return x, y, z #повертаємо координати точки, де немає жодного блоку
    

    # Ставимо блок з урахуванням гравітації
    def buildBlock(self, pos):
        x, y, z = pos #дізнаємось позицію на яку потенційно будемо ставити блок
        new = self.findHighestEmpty(pos) #шукаємо найвищу порожню точку
        if new[2] <= z + 1:
           self.addBlock(new)
            

    def delBlock(self, pos): 
        blocks = self.findBlocks(pos) #перевіряємо наявність об'єктів в певній точці і поруч
        for block in blocks: #через цикл перебираємо список знайдених об'єктів
            block.removeNode() #видаляємо


    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos) #знаходимо точку без блоку
        position = x, y, z-1 #віднімаємо від z  одиницю, оскільки під найвищою порожньою точкою Є блок
        blocks = self.findBlocks(position) 
        for block in blocks: #через цикл перебираємо список знайдених об'єктів
            block.removeNode() #видаляємо


    #зберігає всі блоки, включаючи споруди, у бінарний файл
    # повертає колекцію NodePath для всіх існуючих у карті світу блоків   #1.1 #####################
    def saveMap(self):
        blocks = self.land.getChildren()
        # відкриваємо бінарний файл на запис
        with open('my_map.dat', 'wb') as file:
            # зберігаємо на початок файлу кількість блоків
            pickle.dump(len(blocks), file)
            # обходимо всі блоки
            for block in blocks:
                # зберігаємо позицію
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file)


    def loadMap(self):                                      
        # видаляємо всі блоки
        self.clear()
        # відкриваємо бінарний файл на читання
        with open('my_map.dat', 'rb') as file:
            # зчитуємо кількість блоків
            length = pickle.load(file)
            for i in range(length):
                # зчитуємо позицію
                pos = pickle.load(file)
                # створюємо новий блок
                self.addBlock(pos)


    # Встановлення блокам текстури дерева
    def set_wood(self):
       self.texture  = "wood.png"
    

    # Встановлення блокам текстури каменю
    def set_stone(self):
       self.texture  = "stone.png"


    # Встановлення блокам текстури цегли
    def set_brick(self):
       self.texture  = "brick.png"
    

    # Встановлення блокам звичайної текстури
    def set_block(self):
       self.texture  = "block.png"