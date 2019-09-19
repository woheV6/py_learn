# 安装python3
    - brew install python3
    - 下载的目录在/usr/local/Cellar/python
# 设置环境变量
  - open ~/.bash_profile
    ``` 
        # Setting PATH for Python 2.7
        PATH="/System/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"
        export PATH
        # Setting PATH for Python 3.7.4
        PATH="/usr/local/Cellar/python/3.7.4/bin:${PATH}"
    ```
   - open ~/.bashrc
    ```
        alias python2='/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7'
        alias python3='/usr/local/Cellar/python/3.7.4/bin/python3.7'
        alias python=python3
    ```
   - 让系统生效
     - source ~/.bash_profile     source ~/.bashrc
# 安装pipenv
- brew install pipenv

# api文档生成bao apidoc
# pipenv虚拟环境使用方法
1、打开cmd安装pipenv,

　　pip install pipenv

2、新建工程目录，项目目录，然后cmd进入工程目录

 

基本命令：

　　pipenv install                   创建虚拟环境

pipenv shell            　　 进入虚拟环境（如果不存在，则创建并进入虚拟环境） 

pipenv install flask　　   安装模块

pipenv uninstall flask       卸载模块

pipenv graph　　　　　查看模块之间的依赖关系

pip list　　　　　　　　查看虚拟环境所有模块

exit() 　　　　　　　　 退出虚拟环境

pip freeze > requirements.txt    　　　 导出虚拟环境所有依赖包名

pip install -r requirements.txt  　　 安装项目所依赖全部模块