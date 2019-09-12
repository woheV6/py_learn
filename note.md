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