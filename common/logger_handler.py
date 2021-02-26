import logging  # 导入日志模块




class LoggerHandler(logging.Logger):
    def __init__(self,

            Logger_Name='',
            Logger_Level='',
            Hand_Level='',
            File_Hand_Level='',
            File=None,
            Formatter_join='%(asctime)s---%(levelname)s:%(name)s:%(message)s---%(filename)s---%(lineno)s)',
    ):
        '''初始化logger属性'''
        super().__init__(Logger_Name)

# 日志收集器

        self.setLevel(Logger_Level)  # 设置日志收集器的级别
    # 设置展示格式
        fmt = logging.Formatter(Formatter_join)  # 设置格式（级别名，日志收集器名称，信息，行数）
    # 日志处理器（控制台）
        handler = logging.StreamHandler()  # 获取日志处理器展示在控制台
        handler.setLevel(Hand_Level)  # 日志处理器控制台级别
        self.addHandler(handler)  # 日志收集器添加到控制台
        handler.setFormatter(fmt)  # 将格式设置在控制台中
    # 日志处理器（文件）
        if File:
            file_handler = logging.FileHandler(File,encoding='utf-8') # 获取日志处理器展示在文件
            file_handler.setLevel(File_Hand_Level) # 日志处理器文件级别
            self.addHandler(file_handler)   # 日志收集器添加到文档
            file_handler.setFormatter(fmt)  # 格式添加到文档


# 生成路径文件




if __name__ == '__main__':

    pass