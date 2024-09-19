import os
from llama_cpp import Llama
import gradio as gr
import random


def list_model_files():
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
    return [os.path.join(models_dir, f) for f in model_files]


# List available models
available_models = list_model_files()


def random_seed():
    return random.randint(1, 100000)


def load_model(model_path, gpu):
    global llm
    llm = Llama(model_path=model_path, n_gpu_layers=gpu)


def upsampling_prompt(quality_tags, mode_tags, length_tags, general_tags, max_token, temp, Seed):
    if llm is None:
        return "未加载模型"

    output = llm(
        f"quality: {quality_tags}\naspect ratio: 1.0\ntarget: <|{length_tags}|> <|{mode_tags}|>\ntag: {general_tags}",
        # Prompt
        max_tokens=max_token,
        echo=True,
        temperature=temp,
        seed=Seed,
    )
    return output['choices'][0]['text']


with gr.Blocks() as demo:
    gr.Markdown("""
    # TITPOP!
    写一段提示词，然后让AI帮你优化
    """)

    with gr.Row():
        with gr.Column():
            model_selector = gr.Dropdown(label="选择模型", choices=available_models)
            load_btn = gr.Button("加载模型")
            max_tokens = gr.Number(label="max_tokens", value=1024)
            n_gpu_layers = gr.Number(label="n_gpu_layers", value=-1)
            temprature = gr.Number(label="temperature", value=0.8)
            with gr.Row():
                Seed = gr.Number(label="种子", value=1)
                Seed_random = gr.Button("随机")

        with gr.Column():
            quality_tags = gr.Textbox(label="预期质量")
            mode_tags = gr.Dropdown(
                label="模式",
                choices=["None", "tag_to_long", "long_to_tag", "short_to_long", "short_to_tag", "tag_to_short_to_long",
                         "short_to_tag_to_long", "short_to_long_to_tag"],
            )
            length_tags = gr.Dropdown(
                label="目标长度",
                choices=["short", "long", "very long"],
            )
            general_tags = gr.Textbox(label="Tags")
            upsampling_btn = gr.Button("TITPOP!")
            output = gr.Textbox(label="结果", interactive=False)

    gr.Markdown("""
        ## 关于模型
        - 把模型放在`models`文件夹中
        - 只支持`.gguf`模型
        - 记得选择完后点击加载模型
        ## 关于参数
        - `max_tokens`：生成的最大长度
        - `n_gpu_layers`：使用GPU的层数。-1表示使用全部GPU，0表示使用CPU
        - `temperature`：温度。值越高，则生成结果越随机，值越低，则结果越保守
        - `种子`：随机种子
        ## 关于Tags
        #### 预期质量
        - 就是提示词里的质量标签，比如`masterpiece`这样的
        #### 模式
        - 控制模型生成的内容
        - `None`：Danbooru标签 
        - `tag_to_long`：长自然语言描述 
        - `long_to_tag`：长自然语言描述转Danbooru标签 
        - `short_to_long`：短自然语言描述转长自然语言描述 
        - `short_to_tag`：短自然语言描述转Danbooru标签 
        - `tag_to_short_to_long`：Danbooru标签转短自然语言描述再转长自然语言描述 
        - `short_to_tag_to_long`：短自然语言描述转Danbooru标签再转长自然语言描述 
        - `short_to_long_to_tag`：短自然语言描述转长自然语言描述再转Danbooru标签 
        #### 目标长度
        - 控制生成内容的长度
        #### Tags
        - 你在跑图时写的其他所有标签
        """)

    # button event
    upsampling_btn.click(
        fn=upsampling_prompt,
        inputs=[quality_tags, mode_tags, length_tags, general_tags, max_tokens, temprature, Seed],
        outputs=output)
    load_btn.click(
        fn=load_model,
        inputs=[model_selector, n_gpu_layers],
        outputs=None)
    Seed_random.click(
        fn=random_seed,
        inputs=None,
        outputs=Seed)

demo.launch()
