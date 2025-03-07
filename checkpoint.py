"""
C1: C
C2: C
C3: C
C4: C
C5: C
C6: C
C7: C
C8: C
C9: C
C10: C
"""

"""
Lớp trưởng An muốn xây dựng chương trình để quản lý thông tin các
bạn trong lớp.
Hãy xây dựng lớp HocSinh là lớp mô tả cho các đối tượng học sinh
trong lớp học. Biết mỗi bạn học sinh đều có:
● Họ và tên
● Địa chỉ
● Chiều cao
● Cân nặng
● Học lực
Hãy thiết lập các hành động sau cho lớp HocSinh:
● Khởi tạo để tạo học sinh với tên, địa chỉ, chiều cao và cân nặng
được cung cấp.
● Cập nhật địa chỉ mới khi học sinh chuyển nhà.
● Cập nhật chiều cao và cân nặng mới cho học sinh khi đến kỳ
khám sức khỏe.
● Xuất ra thông tin của học sinh.
"""


class HocSinh:
    def __init__(
        self,
        full_name,
        address,
        height,
        weight,
        hoc_luc,
    ):
        self.full_name = full_name
        self.address = address
        self.height = height
        self.weight = weight
        self.hoc_luc = hoc_luc

    def update_address(self, address):
        self.address = address

    def update_height_weight(self, height, weight):
        self.height = height
        self.weight = weight

    def display(self):
        print("Họ và tên:", self.full_name)
        print("Địa chỉ:", self.address)
        print("Chiều cao:", self.height)
        print("Cân nặng:", self.weight)
        print("Học lực:", self.hoc_luc)


dang = HocSinh("Minh Đăng đóm", "Ben Tre", 189, 50, "Gioi")
dang.display()
dang.update_address("TPHCM")
dang.update_height_weight(180, 70)
dang.display()
