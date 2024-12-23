import os

from database_manager import DatabaseConnection
import random
from datetime import datetime
import time

db_manager = DatabaseConnection()
conn, cursor = db_manager.open()

def addi(table_name, path):
    with open(path, "r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            values = []
            i = i.split(",")
            for k in range(3):
                if (k == 1):
                    number = random.randint(40000, 50000)
                    values.append(number)
                else:
                    values.append(i[k])
            values.append("1")
            db_manager.add_to_table(table_name, values)


def add(table_name, path):
    with open(path, "r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            values = []
            i = i.split(",")
            for k in i[1:]:
                if (k == ""):
                    values.append("1")
                else:
                    values.append(k)
            db_manager.add_to_table(table_name, values)


def add2(table_name, path):
    with open(path, "r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            time.sleep(0.1)
            values = []
            i = i.split(",")
            for k in i[1:]:
                if (k == ""):
                    number = random.randint(1, 100)
                    values.append(number)
                else:
                    if ("/" in k):
                        date_obj = datetime.strptime(k, "%m/%d/%Y")
                        k = date_obj.strftime("%Y/%m/%d")
                    values.append(k)
            db_manager.add_to_table(table_name, values)

"""
folder_path = "/home/cihaneray/Project/WholeSaleManagement/photos/customers"

# Müşteri ID'leri
cursor.execute("SELECT customer_id FROM customer")
customer_ids = cursor.fetchall()

# Müşterilerle eşleşen resim dosyalarını bul ve güncelle
for ind, customer_id in enumerate(customer_ids):

    file_path = os.path.join(folder_path, os.listdir(folder_path)[ind % 7])

    # Yalnızca dosyaları kontrol et
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        # Veritabanını güncelle
        update_query = "UPDATE customer SET image = %s WHERE customer_id = %s"
        cursor.execute(update_query, (binary_data, customer_id[0]))
        conn.commit()
        print(f"Müşteri ID {customer_id[0]} için resmi güncellendi.")

# Bağlantıyı kapatma
cursor.close()
conn.close()
print("Tüm resimler güncellendi ve veritabanı bağlantısı kapatıldı.")

"""

"""# Çıktı klasörü (Kaydedilecek dosyalar için)
output_folder = "/home/cihaneray/Project/WholeSaleManagement/photos/download"
os.makedirs(output_folder, exist_ok=True)

# Fotoğrafları sorgula
cursor.execute("SELECT customer_id, image FROM customer")
rows = cursor.fetchall()

# Fotoğrafları indir ve kaydet
for row in rows:
    customer_id = row[0]
    image_data = row[1]

    # Dosya adı oluştur
    filename = f"customer_{customer_id}.jpg"  # veya uygun bir uzantı belirleyin
    file_path = os.path.join(output_folder, filename)

    # Fotoğrafı kaydet
    with open(file_path, 'wb') as file:
        file.write(image_data)
    print(f"Müşteri ID {customer_id} için fotoğraf {filename} olarak kaydedildi.")

# Bağlantıları kapatma
cursor.close()
conn.close()
print("Tüm fotoğraflar indirildi.")"""


"""folder_path = "/home/cihaneray/Project/WholeSaleManagement/photos/items"

# Müşteri ID'leri
cursor.execute("SELECT item_id FROM item")
item_ids = cursor.fetchall()

# Müşterilerle eşleşen resim dosyalarını bul ve güncelle
for ind, item_id in enumerate(item_ids):

    file_path = os.path.join(folder_path, os.listdir(folder_path)[ind % 9])

    # Yalnızca dosyaları kontrol et
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        # Veritabanını güncelle
        update_query = "UPDATE item SET image = %s WHERE item_id = %s"
        cursor.execute(update_query, (binary_data, item_id[0]))
        conn.commit()
        print(f"Item ID {item_id[0]} için resmi güncellendi.")

# Bağlantıyı kapatma
cursor.close()
conn.close()
print("Tüm resimler güncellendi ve veritabanı bağlantısı kapatıldı.")"""