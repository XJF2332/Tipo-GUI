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
        return "No model loaded"

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
    with gr.Row():
        with gr.Column():
            model_selector = gr.Dropdown(label="Select Model", choices=available_models)
            load_btn = gr.Button("Load Model")
            max_tokens = gr.Number(label="max_tokens", value=1024)
            n_gpu_layers = gr.Number(label="n_gpu_layers", value=-1)
            temprature = gr.Number(label="temperature", value=0.8)
            with gr.Row():
                Seed = gr.Number(label="Seed", value=1)
                Seed_random = gr.Button("Random Seed")

        with gr.Column():
            quality_tags = gr.Textbox(label="quality tags")
            mode_tags = gr.Dropdown(
                label="mode tags",
                choices=["None", "tag_to_long", "long_to_tag", "short_to_long", "short_to_tag", "tag_to_short_to_long",
                         "short_to_tag_to_long", "short_to_long_to_tag"],
            )
            length_tags = gr.Dropdown(
                label="target tags",
                choices=["short", "long", "very long"],
            )
            general_tags = gr.Textbox(label="general tags")
            upsampling_btn = gr.Button("TITPOP!")
            output = gr.Textbox(label="output", interactive=False)

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
