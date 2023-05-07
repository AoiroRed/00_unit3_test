# 摆烂

一个对拍器，会对 jar 目录下的所有 `.jar` 文件进行对拍。

`json` 想必大家都能看懂（

将其复制一份并改名为 `config.json` 就能用啦。

其中 mode 有三种模式：

- `"rand"` 随机生成数据
- `"retest"` 回归测试
- `"input"` 自定义输入，默认输入文件为 `input.txt`

stop 有两种选项：

- `"first"` 在找到第一个错误后停止
- `"never"` 不自动停止

gen_setting 中 type 设置为指令名或对应类名可进行对应强测

`mrok` 摆了。
