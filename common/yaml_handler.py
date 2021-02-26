import yaml
from config.path import config_path
import os
class YamlHandler:
    def __init__(self,fpath):
        """初始化yaml对象"""
        self.fpath = os.path.join(config_path,fpath)

    def yaml_load(self):
        if self.fpath:
            with open(self.fpath,encoding='utf-8') as f:
                data = yaml.load(f,Loader=yaml.SafeLoader)
                return data
        else:
            return '没有yaml文件'

if __name__ == '__main__':
    pass
