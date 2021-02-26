'''
项目的主程序入口
功能：收集用例、执行用例、生成报告
获取时间戳+report.html生成执行用例后生成格式报告
'''

from datetime import datetime
from config import path
import os,pytest
# 获取报告文件名=report+时间戳.html
ts =datetime.now().strftime('%Y-%m-%d %H-%M-%S')
report_name = 'report'+ts+'.html'
# 拼接路径
reports_dir= path.reports_path
report_file_name = os.path.join(reports_dir,report_name)
if __name__ == '__main__':
    pytest.main(['--html={}'.format(report_file_name),'-s'])
