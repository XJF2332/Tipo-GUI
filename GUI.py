import json
import os

print("Loading configs...")

with open(os.path.join('Locales', 'config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)
    lang = config['language']

with open(os.path.join('Locales', f'{lang}.json'), 'r', encoding='utf-8') as f:
    locale = json.load(f)

print(locale["locale_load_success"])

print(locale["import_libs"])

from llama_cpp import Llama
import gradio as gr
import random
import pyperclip
import re

llm = None

theme = gr.themes.Base(
    primary_hue="violet",
    secondary_hue="indigo",
    radius_size="sm",
).set(
    background_fill_primary='*neutral_50',
    border_color_accent='*neutral_50',
    color_accent_soft='*neutral_50',
    shadow_drop='none',
    shadow_drop_lg='none',
    shadow_inset='none',
    shadow_spread='none',
    shadow_spread_dark='none',
    layout_gap='*spacing_xl',
    checkbox_background_color='*primary_50',
    checkbox_background_color_focus='*primary_200'
)


def list_model_files():
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
    return [os.path.join(models_dir, f) for f in model_files]


def random_seed():
    return random.randint(1, 2**31-1)


def load_model(model_path, gpu, n_ctx):
    global llm
    llm = None
    llm = Llama(model_path=model_path, n_gpu_layers=gpu, n_ctx=n_ctx)
    return locale["load_model_success"].format(model_path=model_path)


def unload_model():
    global llm
    llm = None
    return locale["unload_model_success"]


def upsampling_prompt(quality_tags, mode_tags, length_tags, general_tags, max_token, temp, Seed, top_p, min_p, top_k):
    if llm is None:
        return locale["model_not_loaded"]

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
    # print(output)

    return output['choices'][0]['text']


def extract_and_format(model_out):
    fields_to_extract = ['quality', 'artist', 'tag', 'long', 'short', 'characters', 'meta', 'rating']

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
        value = extracted_data.get(field, '')
        if value:  # Only add the field if it has a value
            formatted_output += f"{value}\n\n"

    # Remove the last two newline characters to ensure no extra space at the end
    formatted_output = formatted_output.rstrip('\n')

    return formatted_output


def remove_words_by_regex(sentence, pattern):
    # 移除末尾的逗号和空格（如果有的话）
    patterns = pattern.rstrip(', ')
    # 将传入的正则表达式字符串分割成列表
    pattern_list = re.split(r',\s*', patterns)
    # 使用正则表达式分割句子
    words = re.split(r',\s*', sentence)
    # 初始化一个空列表来存放过滤后的词
    filtered_words = []
    # 遍历原始单词列表
    for word in words:
        # 检查当前单词是否与任一正则表达式匹配
        should_remove = False
        for pattern in pattern_list:
            if re.match(pattern, word):
                should_remove = True
                break
        # 如果当前单词不匹配任何正则表达式，则添加到过滤后的列表中
        if not should_remove:
            filtered_words.append(word)
    # 重新组合成字符串
    result = ', '.join(filtered_words)
    return result


def update_format_output(formatted_text, banned_tags):
    text = extract_and_format(formatted_text)
    if banned_tags:
        formatted = remove_words_by_regex(text, banned_tags)
    else:
        formatted = text
    format_output = gr.Textbox(value=formatted, interactive=False)
    return format_output


def copy_to_clipboard(output):
    try:
        pyperclip.copy(output)
        gr.Info(locale["copy_success"])
    except Exception as e:
        gr.Error(locale["copy_fail"])


print(locale["model_searching"])
# List available models
available_models = list_model_files()

print(locale["gradio_launching"])

with open(os.path.join('Locales', 'Tutorials', f'{lang}.md'), "r", encoding="utf-8") as tutorial:
    tutorial_content = tutorial.read()

with gr.Blocks(theme=theme) as demo:
    gr.Markdown("""
    # TITPOP
    """)

    with gr.Row():
        with gr.Column():
            with gr.Tab(locale["tab_generate"]):
                with gr.Row():
                    Seed = gr.Number(label=locale["seed"], value=-1)
                    Seed_random = gr.Button(locale["random_seed"])
                with gr.Row():
                    mode_tags = gr.Dropdown(
                        label=locale["mode"],
                        choices=["None", "tag_to_long", "long_to_tag", "short_to_long", "short_to_tag",
                                 "tag_to_short_to_long",
                                 "short_to_tag_to_long", "short_to_long_to_tag"],
                        value="None"
                    )
                    length_tags = gr.Dropdown(
                        label=locale["length"],
                        choices=["very_short", "short", "long", "very_long"],
                        value="short"
                    )
                with gr.Row():
                    quality_tags = gr.Textbox(label=locale["quality"])
                    banned_tags = gr.Textbox(label=locale["banned_tags"])
                general_tags = gr.Textbox(label=locale["general_tags"])

            with gr.Tab(locale["tab_settings"]):
                gr.Markdown(locale["model_settings"])
                model_selector = gr.Dropdown(label=locale["model_select"], choices=available_models)
                with gr.Row():
                    n_ctx = gr.Number(label="n_ctx", value=2048)
                    n_gpu_layers = gr.Number(label="n_gpu_layers", value=-1)
                with gr.Row():
                    unload_btn = gr.Button(locale["model_unload"])
                    load_btn = gr.Button(locale["model_load"],variant="primary")
                load_feedback = gr.Markdown("")
                gr.Markdown(locale["generate_settings"])
                with gr.Row():
                    top_p = gr.Number(label="top_p", value=0.95)
                    min_p = gr.Number(label="min_p", value=0.05)
                with gr.Row():
                    max_tokens = gr.Number(label="max_tokens", value=1024)
                    temprature = gr.Number(label="temperature", value=0.8)
                top_k = gr.Number(label="top_k", value=60)

            with gr.Tab(locale["tab_tutorial"]):
                gr.Markdown(tutorial_content)
        with gr.Column():
            with gr.Row():
                upsampling_btn = gr.Button("TITPOP!", variant="primary")
                copy_btn = gr.Button(locale["copy_to_clipboard"])
            with gr.Row():
                raw_output = gr.Textbox(label=locale["result"], interactive=False)
                formatted_output = gr.Textbox(label=locale["formatted_result"], interactive=False)
                raw_output.change(update_format_output, inputs=[raw_output, banned_tags], outputs=formatted_output)

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
    unload_btn.click(
        fn=unload_model,
        inputs=None,
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
        outputs=None
    )

demo.launch()
