# botRoy
> 基于NoneBot2 + Go-cqhttp 开发的个人机器人
> @Suroy

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `botroy/plugins` folder.
4. run your bot using `nb run` .

## Official Documentation
[Nonebot2](https://v2.nonebot.dev/) ，[Go-cqhttp](https://docs.go-cqhttp.org/)

## 主要功能

1. 疫情打卡自动通知到群消息
   + 自定义功能开关及提醒消息
   + 未完成，由于导员没有给权限，无法完成后续开发😲
   + 不出意外会在此基础上开发另外的功能
2. 晨报（感谢开源项目😋）
3. 服务器状态检测
4. 青年大学习相关通知功能
5. 茉莉机器人聊天对话功能

## 快速启动

1. 安装go-cqhttp，配置websocks
2. 安装NoneBot2
3. 克隆本仓库机器人
4. 安装定时任务插件 `nb plugin install nonebot_plugin_apscheduler`
5. 安装相关依赖库（建议选择性安装） `pip3 install -r requirement.txt`
6. 启动...


## 版本更新

### V1.0 ｜ 2022.1.16
> 适用：[**Nonebot2**] _v2.0.0beta.1_ 、[**go-cqhttp**] _v1.0.0-beta8-fix2_
> 

### V1.1 | 2022.1.17
> 新增青年大学习功能：统计、定时提醒、功能开关  
> 版本未发生改变


### V1.2.1 | 2022.2.5
> 修复底层Nonebot API错误  
> 新增茉莉机器人对话插件  

**测试版本** (修复也均以该版本报错修复)   
OS: Ubuntu 21.10 armv7l  
Nonebot V2.0.0-beta.1  
[go-cqhttp_linux_armv7.tar.gz](https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-beta8-fix2/go-cqhttp_linux_armv7.tar.gz)

[x] 待修复该系统下服务器状态监测插件  
[x] 待完善茉莉机器人群聊功能开关