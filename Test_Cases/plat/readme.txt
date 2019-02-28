1、PMC上导入DevInfo.csv里的10个基础数据。
2、入网一个在线的解码器，获取相关信息后用于电视墙的用例操作。
3、在10.20.20.210磁阵上新建一个iscsi虚拟磁盘，赋予平台权限。
4、修改脚本的Python_Interface_VIID\Conf\Conf.conf里的Thread_Num 为1.


SVN服务：svn://10.20.20.222。admin/admin123
	开机后开启svn：svnserve -d -r /opt/svnrepos
jenkins服务器：10.20.20.222:8080。admin/admin123