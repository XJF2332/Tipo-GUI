print("正在加载库...")

import os
from llama_cpp import Llama
import gradio as gr
import random
import pyperclip


def list_model_files():
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
    return [os.path.join(models_dir, f) for f in model_files]


def random_seed():
    return random.randint(1, 100000)


def load_model(model_path, gpu, n_ctx):
    global llm
    llm = Llama(model_path=model_path, n_gpu_layers=gpu, n_ctx=n_ctx)
    return f"模型 {model_path} 已加载"


def upsampling_prompt(quality_tags, mode_tags, length_tags, general_tags, max_token, temp, Seed, top_p, min_p, top_k):
    if llm is None:
        return "未加载模型"

    output = llm(
        f"quality: {quality_tags}\naspect ratio: 1.0\ntarget: <|{length_tags}|> <|{mode_tags}|>\ntag: {general_tags}",
        # Prompt
        max_tokens=max_token,
        echo=True,
        temperature=temp,
        seed=Seed,
        top_p=top_p,
        min_p=min_p,
        top_k=top_k
    )

    # for testing
    print(output)

    return output['choices'][0]['text']


def extract_and_format(model_out):
    fields_to_extract = ['quality', 'tag', 'long', 'short', 'artist', 'characters', 'meta', 'rating']

    def extract_fields(model_output):
        extracted_data = {}

        for line in model_output.split('\n'):
            for field in fields_to_extract:
                if line.startswith(field + ':'):
                    extracted_data[field] = line[len(field) + 1:].strip()

        return extracted_data

    extracted_data = extract_fields(model_out)
    formatted_output = ""

    for field in fields_to_extract:
        # Add the field and its value or an empty line if the field is missing
        formatted_output += f"{extracted_data.get(field, '')}\n\n"

    return formatted_output


def update_format_output(formatted_text):
    text = extract_and_format(formatted_text)
    format_output = gr.Textbox(value=text, interactive=False)
    return format_output

def copy_to_clipboard(output):
    pyperclip.copy(output)
    return "已复制到剪贴板"


print("正在查找模型...")
# List available models
available_models = list_model_files()

print("正在启动 Gradio UI...")

with gr.Blocks() as iface:
    gr.Markdown("""
    # TITPOP
    """)

    with gr.Tab("生成"):
        with gr.Row():
            Seed = gr.Number(label="种子", value=1)
            Seed_random = gr.Button("随机")
        with gr.Row():
            mode_tags = gr.Dropdown(
                label="模式",
                choices=["None", "tag_to_long", "long_to_tag", "short_to_long", "short_to_tag", "tag_to_short_to_long",
                         "short_to_tag_to_long", "short_to_long_to_tag"],
                value="None"
            )
            length_tags = gr.Dropdown(
                label="目标长度",
                choices=["very_short", "short", "long", "very_long"],
                value="short"
            )
        with gr.Row():
            quality_tags = gr.Textbox(label="预期质量")
            general_tags = gr.Textbox(label="Tags")
        upsampling_btn = gr.Button("TITPOP!")
        with gr.Row():
            copy_btn = gr.Button("复制到剪贴板")
            copy_info = gr.Textbox(show_label=False, interactive=False)
        with gr.Row():
            raw_output = gr.Textbox(label="结果", interactive=False)
            formatted_output = gr.Textbox(label="格式化结果", interactive=False)
            raw_output.change(update_format_output, inputs=raw_output, outputs=formatted_output)

    with gr.Tab("设置"):
        gr.Markdown("模型设置")
        model_selector = gr.Dropdown(label="选择模型", choices=available_models)
        with gr.Row():
            n_ctx = gr.Number(label="n_ctx", value=2048)
            n_gpu_layers = gr.Number(label="n_gpu_layers", value=-1)
        load_btn = gr.Button("加载模型")
        load_feedback = gr.Markdown("")
        gr.Markdown("生成设置")
        with gr.Row():
            top_p = gr.Number(label="top_p", value=0.95)
            min_p = gr.Number(label="min_p", value=0.05)
        with gr.Row():
            max_tokens = gr.Number(label="max_tokens", value=1024)
            temprature = gr.Number(label="temperature", value=0.8)
        top_k = gr.Number(label="top_k", value=60)

    with gr.Tab("教程"):
        gr.Markdown("""
            ## 关于模型
            - 把模型放在`models`文件夹中
            - 只支持`.gguf`模型
            - 记得选择完后点击加载模型
            ## 关于参数
            - `max_tokens`：生成的最大长度（虽然是默认1024，但其实128也是够用的）
            - `n_gpu_layers`：使用GPU的层数。-1表示使用全部GPU，0表示使用CPU（模型只有200M，所以其实只用CPU也不见得多慢，而且还可以给SD省一点显存）
            - `temperature`：温度。值越高，则生成结果越随机，值越低，则结果越保守
            - `n_ctx`：上下文长度。这个值越大，模型能记住的信息越多，但也会导致显存占用增加
            - `top_p`、`min_p`、`top_k`：我也不知道是啥，所以建议保持默认（
            - `种子`：这个不需要解释吧(≧∀≦)ゞ
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
            ## 关于输出
            ### 结果
            - 模型生成的文本
            - 并不是原始结果，只是经过了处理的原始结果，不能直接用来出图，但可以获得比格式化结果更多的信息
            - 如果要查看原始结果，取消注释`#for testing`的代码，然后在控制台查看原始结果
            ### 格式化结果
            - 模型生成的文本，经过格式化处理，可以直接用来出图
            """)

    # button event
    upsampling_btn.click(
        fn=upsampling_prompt,
        inputs=[quality_tags, mode_tags, length_tags, general_tags, max_tokens, temprature, Seed, top_p, min_p, top_k],
        outputs=raw_output
    )
    load_btn.click(
        fn=load_model,
        inputs=[model_selector, n_gpu_layers, n_ctx],
        outputs=load_feedback
    )
    Seed_random.click(
        fn=random_seed,
        inputs=None,
        outputs=Seed
    )
    copy_btn.click(
        fn=copy_to_clipboard,
        inputs=formatted_output,
        outputs=copy_info
    )

iface.launch()
