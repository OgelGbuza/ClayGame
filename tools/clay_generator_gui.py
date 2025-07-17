"""Claymation image generator GUI.

This tool can create clay-style images using either a local Stable Diffusion
model (via the diffusers library) or the OpenAI DALL·E API. It is meant as a
helper for producing new sprites for the game."""

import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import torch
    from diffusers import StableDiffusionPipeline
except ImportError:  # pragma: no cover - optional
    StableDiffusionPipeline = None

try:
    import openai
    import requests
    from PIL import Image, ImageTk
except ImportError:  # pragma: no cover - optional
    openai = None
    Image = None

DEVICE = "cuda" if StableDiffusionPipeline and torch.cuda.is_available() else "cpu"
_sd_pipe = None


def load_sd():
    global _sd_pipe
    if _sd_pipe is None and StableDiffusionPipeline is not None:
        _sd_pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
        )
        _sd_pipe.to(DEVICE)
    return _sd_pipe


def sd_image(prompt: str, steps: int):
    pipe = load_sd()
    if pipe is None:
        raise RuntimeError("Stable Diffusion not available")
    full_prompt = (
        "Claymation-style, handcrafted stop-motion aesthetic, " + prompt
    )
    return pipe(full_prompt, num_inference_steps=steps).images[0]


def dalle_image(prompt: str):
    if openai is None:
        raise RuntimeError("OpenAI package not available")
    full_prompt = (
        "Claymation-style, handcrafted stop-motion aesthetic, " + prompt
    )
    resp = openai.Image.create(prompt=full_prompt, n=1, size="512x512")
    url = resp["data"][0]["url"]
    img = Image.open(requests.get(url, stream=True).raw)
    return img


class GeneratorApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Clay Generator")

        tk.Label(master, text="Prompt:").pack()
        self.prompt = tk.Text(master, height=3, width=40)
        self.prompt.pack()

        self.model = tk.StringVar(value="sd")
        frame = tk.Frame(master)
        frame.pack()
        tk.Radiobutton(frame, text="Stable Diffusion", variable=self.model, value="sd").pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="DALL·E", variable=self.model, value="dalle").pack(side=tk.LEFT)

        tk.Label(master, text="Steps (SD only)").pack()
        self.steps = tk.Scale(master, from_=10, to=100, orient="horizontal")
        self.steps.set(50)
        self.steps.pack()

        tk.Button(master, text="Generate", command=self.generate).pack(pady=5)
        self.canvas = tk.Canvas(master, width=256, height=256, bg="gray")
        self.canvas.pack()
        self.save_btn = tk.Button(master, text="Save", state=tk.DISABLED, command=self.save)
        self.save_btn.pack(pady=5)
        self.image = None

    def generate(self):
        prompt = self.prompt.get("1.0", tk.END).strip()
        try:
            if self.model.get() == "sd":
                self.image = sd_image(prompt, self.steps.get())
            else:
                self.image = dalle_image(prompt)
        except Exception as exc:  # pragma: no cover - runtime depends on libs
            messagebox.showerror("Error", str(exc))
            return

        img = self.image.copy()
        img.thumbnail((256, 256))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(128, 128, image=self.tk_img)
        self.canvas.image = self.tk_img
        self.save_btn.config(state=tk.NORMAL)

    def save(self):
        if self.image is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if path:
            self.image.save(path)
            messagebox.showinfo("Saved", f"Image saved to {path}")


def main():
    root = tk.Tk()
    GeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
