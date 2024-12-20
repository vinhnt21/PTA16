"""
PhuongTien:
	name
	color
	price

Container:
	tai_trong
	
Bus:
	so_luong_toi_da
"""


class PhuongTien:
    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price

    def show_name(self):
        print(self.name)


class Container(PhuongTien):
    def __init__(self, name, color, price, tai_trong):
        super().__init__(name, color, price)
        self.tai_trong = tai_trong


class Bus(PhuongTien):
    def __init__(self, name, color, price, so_luong_toi_da):
        super().__init__(name, color, price)
        self.so_luong_toi_da = so_luong_toi_da


container1 = Container("Huyndai Pro Ultra Note Max", "pink", 5000000, 5000)
container1.show_name()
