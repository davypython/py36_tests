import os

# 动态获取config_path路径
config_path = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
root_path = os.path.dirname(config_path)

# 动态获取data目录，若无则创建
data_path = os.path.join(root_path,'data')
if not os.path.exists(data_path):
    os.mkdir(data_path)
# 动态获取logs目录，若无则创建
logs_path = os.path.join(root_path,'logs')
if not os.path.exists(logs_path):
    os.mkdir('logs')
# 动态获取report目录，若无则创建
reports_path = os.path.join(root_path,'reports')
if not os.path.exists(reports_path):
    os.mkdir('reports')
# 动态获取tests目录，若无则创建
tests_path = os.path.join(root_path,'tests')
if not os.path.exists(tests_path):
    os.mkdir('tests')

if __name__ == '__main__':
    print(data_path)