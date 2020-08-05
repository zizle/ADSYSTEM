【编码问题】
    ①大商所日持仓数据采用zip文件获取,解压时的数据文件名不同平台会可能会出现乱码现象。看情况修改`zipfile.py`中的源码进行修订。
    博文地址:https://blog.csdn.net/zizle_lin/article/details/107732283

【打包问题】
    ①后台系统打包全部打入。客户端系统根据configs.py开放的菜单。看情况是否打包`admin`(后台管理),`spiders`(交易所数据抓取);
    ②打包成安装包的时候,要放入安装程序文件:`AutoAdminUpdate.exe`和`AutoAdminUpdate.exe.manifest`.

【发布问题】
    ①打包好的文件放置目标位置,通过后端系统中的源码`BackService/scripts/update_json_generator.py`执行生成相应的平台更新json源文件,
    放置于后端源码`BackService/conf/`文件夹下