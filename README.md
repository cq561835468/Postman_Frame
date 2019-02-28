# Postman+jekins的自动化集成框架

# 流程：
1. 使用postman编写测试用例
2. 将测试用例同步到SVN之类的工具中
3.在jenkins上设置同步Test_Cases文件夹
4.jenkins上新建每日构建任务

# 介绍：
1. Auto_Para_Script：测试用例的参数化工具，将公共外部数据提取后自动生成
2. Python_Interface_VIID：执行测试用例工具，批量执行测试所有测试用例，支持多线程、同步CMO系统等功能
3. report：存放备份报告
4. Test_Cases：存放测试用例
5. Doc：搭建文档等
