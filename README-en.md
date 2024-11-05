# TIPO GUI

[中文版看这里](README.md)

![img.png](img.png)

## GUI Version of KohakuBlueLeaf's `TIPO`

To view the model weights of `TIPO`, go to mirror site: [200M](https://hf-mirror.com/KBlueLeaf/TIPO-200M)、[500M](https://hf-mirror.com/KBlueLeaf/TIPO-500M)、[GGUF(QuantFactory)](https://hf-mirror.com/QuantFactory/TIPO-500M-GGUF)  
Or if you can, directly visit the original site: [200M](https://huggingface.co/KBlueLeaf/TIPO-200M)、[500M](https://huggingface.co/KBlueLeaf/TIPO-500M)、[GGUF(QuantFactory)](https://huggingface.co/QuantFactory/TIPO-500M-GGUF)  
[KohakuBlueleaf's GitHub Homepage](https://github.com/KohakuBlueleaf)  

Thank [Yi-1.5](https://github.com/01-ai/Yi-1.5) for translating this README to English.  
Thank [GLM4](https://chatglm.cn/main/alltoolsdetail?lang=zh) for providing some of the code (since I am really not good
at it, so I have to use AI)  

## Dependencies

It's better to use the GPU version of `llama-cpp-python` because the parameter `n_gpu_layers` won't work in CPU version.

```
llama-cpp-python
gradio
pyperclip
```

## How to Use

1. Download the `.gguf` file from the place mentioned above, and put it into the `models` folder in the same directory
   as the script.
2. Double-click the script, or run `python GUI.py` with `cmd`.
3. Go to the "Settings" page, select your model file, then click Load.
4. If you don't understand the parameters, you have two options: Don't touch them, or go to the "Tutorials" page for an
   explanation.
5. See below for generation settings, with the same two choices as above.
6. Go to the "Generate" page, select your mode, length, write your prompt, quality, then click "TIPO!".
7. Click "Copy to Clipboard" to copy the results.

## Localization

- Use `Language Config Manager.py` to manage language configurations.
- To add a new language, follow these steps:
    1. Create a new `.json` file in the `Locales` folder.
    2. I recommend you copy an existing language file and then translate it; save your file after translation is
       complete.
    3. In the `Tutorials` subfolder, create a new `.md` file.
    4. Copy an existing tutorial file, translate, and save.
    5. Open `Language Config Manager.py`, choose `2. Write new language config`, your language file name should appear
       in the options.
    6. Select your file, restart Webui, and you should see the language settings take effect.

---

If you crash when double-clicking the script, try running `python GUI.py` in `cmd`; anyway, I have no idea why since
this was all new to me.