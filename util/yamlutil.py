# 使用方法
# 1.import导入方法
# from Yamlutil import YamlReader
# 2.初始化yamutils, 传入文件名称
# reader = YamlReader(yamlfile=yaml_file)
# 3.1读取单个文档的yml
# 调用方法,输出结果
# data = reader.read_data()  # 读取单个文件
# print(data)
# 3.2读取多个文档的yml
# data_all = reader.read_data_all()  # 读取多个文件
# print(data_all)
# for data in data_all:
#     print(data)

import yaml
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
yaml_file = os.path.join(BASE_DIR, 'config.yml')


# 创建类
class YamlReader:
    # 初始化方法，判断文件是否存在
    def __init__(self, yamlfile):
        if os.path.exists(yamlfile):
            self.yamlf = yamlfile
        else:
            raise FileNotFoundError("文件不存在")
        self._data = None  # 默认没有读取过文件
        self._data_all = None  # 默认没有读取过文件

    # 定义方法, Yaml读取单个文档
    def read_data(self):
        if not self._data:  # 判断是否有读取文件
            with open(self.yamlf, 'r', encoding="utf8") as f:
                self._data = yaml.safe_load(f)
        return self._data

    # 定义方法, Yaml读取多个文档
    def read_data_all(self):
        if not self._data_all:  # 判断是否有读取文件
            with open(self.yamlf, 'r', encoding="utf8") as f:
                self._data_all = list(yaml.safe_load_all(f))
        return self._data_all


reader = YamlReader(yamlfile=yaml_file)
data_all = reader.read_data_all()