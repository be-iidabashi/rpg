import pyxel

class PyxresToListExtractor:
    def __init__(self):
        # pyxelを初期化
        pyxel.init(16, 16)
        
        # .pyxres ファイルを読み込む
        pyxel.load("my_resource.pyxres")

        # イメージバンク0の (x=0, y=0) から 16x16 のドット絵をリスト化
        dot_data = self.extract_16x16_list(img_id=0, start_x=0, start_y=0)

        # 結果を表示（Pythonの2次元リストとして出力）
        print("--- 16x16 ドット絵リストデータ ---")
        for row in dot_data:
            print(f"{row},")

        # Pyxel終了
        pyxel.quit()

    def extract_16x16_list(self, img_id, start_x, start_y):
        dot_list = []
        image = pyxel.images[img_id]

        for y in range(start_y, start_y + 16):
            row = []
            for x in range(start_x, start_x + 16):
                # 修正箇所: get(x, y) -> pget(x, y)
                color_code = image.pget(x, y)
                row.append(color_code)
            dot_list.append(row)

        return dot_list

if __name__ == "__main__":
    PyxresToListExtractor()