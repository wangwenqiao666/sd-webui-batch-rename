import gradio as gr
import os
import shutil
from modules import scripts


class Script(scripts.Script):
    def title(self):
        return "Batch Rename Images"

    def ui(self, is_img2img):
        open_folder = gr.components.Textbox(lines=1, label="Enter folder path")
        save_folder = gr.components.Textbox(lines=1, label="Save folder path")
        prefix = gr.components.Textbox(lines=1, label="Enter file name prefix")
        digits = gr.components.Textbox(lines=1, label="Reserved file number")
        rename_button = gr.Button(label="Rename image")
        output_text = gr.components.Textbox()
        rename_button.click(
            self.run,
            inputs=[open_folder, save_folder, prefix, digits],
            outputs=[output_text],
        )
        return [open_folder, save_folder, prefix, digits, rename_button, output_text]

    def run(self, open_folder: str, save_folder: str, prefix: str, digits: str):
        print(f"open_folder:{open_folder}, save_folder:{save_folder}, prefix:{prefix}, digits:{digits}" )
        if not os.path.isdir(open_folder):
            return "The open folder path is not a valid directory."
        if not os.path.isdir(save_folder):
            return "The save folder path is not a valid directory."
        try:
            digits = int(digits)
        except ValueError:
            return "Digits value must be an integer."

        # check if save folder has any files and delete them
        for filename in os.listdir(save_folder):
            file_path = os.path.join(save_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                return "Failed to delete %s. Reason: %s" % (file_path, e)

        i = 1
        for filename in os.listdir(open_folder):
            name, ext = os.path.splitext(filename)
            if ext.lower() in [".jpg", ".jpeg", ".png"]:
                src = open_folder + "/" + filename
                dst = save_folder + "/" + prefix + str(i).zfill(digits) + ext
                shutil.copy2(src, dst)
                i += 1
        return "All file names have been successfully changed!"
