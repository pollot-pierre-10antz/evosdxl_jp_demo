import gradio as gr
import time
import torch

from argparse import ArgumentParser, Namespace
from accelerate import Accelerator
from diffusers import DiffusionPipeline


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--public", action="store_true")
    parser.add_argument("--port", "-p", type=int)
    parser.add_argument("--id", type=str, default="10antz")
    parser.add_argument("--password", type=str, default="12345")
    parser.add_argument("--unload_model_interval", type=int, default=15, help="in minutes.")
    parser.add_argument("--model_path_or_url", type=str, default="stabilityai/japanese-stable-diffusion-xl")
    return parser.parse_args()


def get_devices(): 
    idle_device = torch.device("cpu")
    device = Accelerator().device
    device = device if "mps" not in device.__str__() else idle_device # mps device seems not supported
    return device, idle_device


if __name__ == "__main__":
    args = parse_arguments()
    
    # load model
    device, idle_device = get_devices()
    print(f"Active device: {device} | Idle device: {idle_device}")
    pipe = DiffusionPipeline.from_pretrained(args.model_path_or_url, trust_remote_code=True)
    t0 = time.monotonic()
    
    # app structure
    with gr.Blocks() as app:
        with gr.Row():
            with gr.Column():
                prompt = gr.TextArea(label="プロンプト", placeholder="例：兎は蛙と戦争している")
                negative_prompt = gr.TextArea(label="ネガティブ・プロンプト", placeholder="例：猿がいる\n（→猿に居ないでほしい）")
                inference_steps = gr.Slider(1, 200, step=1, value=50, label="生成によるステップ数")
                batch_size = gr.Slider(1, 4, step=1, value=1, label="画像の枚数/生成")
            with gr.Column():
                generated_images = gr.Gallery()
        with gr.Row():
            generate_button = gr.Button("生成する", variant="primary")
        
        def generate(prompt: str, negative_prompt: str, inference_steps: int, batch_size: int) -> list:
            global pipe, t0
            if pipe.device == idle_device:
                print("Move pipe to active device.")
                pipe.to(device)
            t0 = time.monotonic()
            return pipe(
                prompt=prompt, 
                negative_prompt=negative_prompt,
                height=1024,
                width=1024,
                num_inference_steps=inference_steps,
                num_images_per_prompt=batch_size,
            ).images
        
        generate_button.click(
            generate,
            inputs=[prompt, negative_prompt, inference_steps, batch_size],
            outputs=[generated_images],
        )
        
        def load_unload_manager():
            global pipe, t0
            if pipe.device == idle_device:
                return
            t1 = time.monotonic()
            if t1 - t0 >= args.unload_model_interval:
                pipe.to(idle_device)
                print(f"Pipe temporarily stored to {idle_device}")
                t0 = time.monotonic()
        
        timer = gr.Textbox(
            value=load_unload_manager, 
            every=args.unload_model_interval * 60, 
            visible=False, 
            interactive=False
        )
    
    # launch app        
    app.launch(
        share=args.public,
        auth=(args.id, args.password),
        server_port=args.port,
    )