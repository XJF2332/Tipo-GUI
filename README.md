# TITPOP GUI

![img_1.png](img_1.png)
![img.png](img.png)

## 琥珀青叶（繁体字不会打）大佬的`TITPOP`的 GUI 版本

要查看`TITPOP`的模型权重，前往：[TITPOP（镜像站）](https://hf-mirror.com/KBlueLeaf/TITPOP-200M-dev)

或者有能力的可以直接去[huggingface的原站点](https://huggingface.co/KBlueLeaf/TITPOP-200M-dev)看看

[琥珀佬的Github主页](https://github.com/KohakuBlueleaf)

## 使用方法

去前面提到的模型权重那里下载`.gguf`文件，放进脚本所在目录下的`models`文件夹里，然后直接打开GUI.py就行了（记得先配置好环境）

## 依赖
llama-cpp-python 要 GPU 版的
```
llama-cpp-python
gradio
pyperclip
```

---

以及，谁知道脚本里的`aspect_ratio`这个参数是个啥，我自己都没搞懂（

直接双击脚本闪退的话可以试一下在`cmd`里用`python +文件名`，总之就是我也不知道为什么，这玩意我也是现学的