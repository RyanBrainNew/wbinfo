#### 异常错误

1.requests版本过高，会导致使用代理vpn时候，出现check_hostname requires server_hostname错误。建议把requests版本降为2.20



#### TIPS

输出当前环境配置库信息等，打开源码，切换能运行的虚拟环境，在terminal中执行以下指令

```
pip freeze > requirments.txt
```

