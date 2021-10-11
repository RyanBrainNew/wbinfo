#### 异常错误

1.requests版本过高，会导致使用代理vpn时候，出现check_hostname requires server_hostname错误。建议把requests版本降为2.20



#### TIPS

##### 1.输出配置文件

输出当前环境配置库信息等，打开源码，切换能运行的虚拟环境，在terminal中执行以下指令

```
pip list --format=freeze > requirements.txt
```

安装时，执行以下指令

```
pip install -r requirements.txt
或
pip3 install -r requirements.txt
```



##### 2.忽略某个文件变动

忽略文件命令：

```
git update-index --assume-unchanged 文件名
```

作用：忽略文件的改动，但是不加入.gitignore 文件中，这样可以达到仅在本地目录中忽略，不影响其他团队成员的工作。

取消忽略命令：

```
git update-index --no-assume-unchanged 文件名
```

作用：上一个命令的逆操作，重新追踪文件改动。
