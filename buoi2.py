class Game:
    def __init__(self, name, price, size, type, so_luong_da_ban):
        self.name = name
        self.price = price
        self.size = size
        self.type = type
        self.so_luong_da_ban = so_luong_da_ban

    def buy(self):
        self.so_luong_da_ban += 1
        print("Giá của game", self.name, "là", self.price)
        print("Số lượng đã bán của game", self.name, "là", self.so_luong_da_ban)

    def giam_gia(self, phan_tram):
        self.price = self.price * (100 - phan_tram) / 100
        print("Giá gmae", self.name, "sau khi giảm giá là", self.price)

    def show_name(self):
        print(self.name)


wukong = Game("ff", 8386, "1GB", "adventure", 1000000)
wukong.show_name()
j97 = Game("j97", 10000, "2GB", "action", 1000000)
j97.show_name()
