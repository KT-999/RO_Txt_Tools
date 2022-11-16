from django.db import models

# Create your models here.

TYPE_CHOICES = (
    ('T1', 'type 1'),
    ('T2', 'type 2'),
    ('T3', 'type 3'),
    ('T4', 'type 4'),
)


class Accessoryid(models.Model):
    creat_user = models.TextField(null=False)  # 編輯者名稱
    view = models.PositiveIntegerField(null=False)  # view值
    view_name = models.TextField(null=False)  # view名稱
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "accessoryid"

    def display_type_name(self):
        return self.get_type_display()


class Accname(models.Model):
    creat_user = models.TextField(null=False)  # 編輯者名稱
    act = models.TextField(null=False)  # 對應檔案名稱
    view_name = models.TextField(null=False)  # view名稱
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "accname"

    def display_type_name(self):
        return self.get_type_display()


class Cardprefixnametable(models.Model):
    creat_user = models.TextField(null=False)  # 編輯者名稱
    item = models.TextField(null=False)  # 物品編號
    card_name = models.TextField(null=False)  # 鑲嵌名稱
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "cardprefixnametable"

    def display_type_name(self):
        return self.get_type_display()


class Num2cardillustnametable(models.Model):
    creat_user = models.TextField(null=False)  # 編輯者名稱
    item = models.TextField(null=False)  # 物品編號
    card_act = models.TextField(null=False)  # 顯示卡片對應外觀
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "num2cardillustnametable"

    def display_type_name(self):
        return self.get_type_display()


class Spriterobeid(models.Model):
    creat_user = models.TextField(null=False)  # 編輯者名稱
    robe_id = models.TextField(null=False)  # 披肩名稱
    view = models.TextField(null=False)  # view
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "spriterobeid"

    def display_type_name(self):
        return self.get_type_display()


class Spriterobename(models.Model):
    creat_user = models.TextField(null=False)  # 編輯者名稱
    robe_id = models.TextField(null=False)  # 披肩名稱
    robe_act = models.TextField(null=False)  # 披肩對應檔案
    robe_id_eng = models.TextField(null=False)  # 披肩名稱_en
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "spriterobename"

    def display_type_name(self):
        return self.get_type_display()


class Item_info(models.Model):
    creat_user = models.TextField(null=False)  # 編輯者名稱
    item = models.PositiveIntegerField(null=False)  # 物品編號
    name_scan = models.TextField(null=False)  # 物品名稱 鑑定後
    name = models.TextField(null=False)  # 物品名稱 鑑定前
    act_scan = models.TextField(null=False)  # 物品對應圖 鑑定後
    act = models.TextField(null=False)  # 物品對應圖 鑑定前
    caption_scan = models.TextField(max_length=40000, null=False)  # 物品說明 鑑定後
    caption = models.CharField(max_length=40000, null=False)  # 物品說明 鑑定前
    card = models.TextField(null=False)  # 洞數
    view = models.TextField(null=False)  # view值
    item_type = models.TextField(null=False)  # 物品種類
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "item_info"

    def display_type_name(self):
        return self.get_type_display()


class itemInfo_data(models.Model):
    creat_user = models.TextField(null=False)  # 上傳者名稱
    info_data = models.FileField(null=False)  # itemInfo 文件
    last_modify_date = models.DateTimeField(auto_now=True)  # 編輯時間

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "itemInfo_data"

    def display_type_name(self):
        return self.get_type_display()


class User_data(models.Model):
    username = models.TextField(null=False)
    login_time = models.DateTimeField(auto_now=True)

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "user_data"

    def display_type_name(self):
        return self.get_type_display()
