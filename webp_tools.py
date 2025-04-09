import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import json

from merge_images import merge_images
from png_to_webp import convert_png_to_webp

class WebpTools:
    def __init__(self, root):
        self.root = root
        self.root.title("Webp 工具箱")
        
        # 加载上次的保存路径
        self.config_file = Path.home() / '.webp_tools_config.json'
        self.load_config()
        
        # 设置窗口大小和位置
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # 创建选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        # 创建两个选项卡页面
        self.merge_frame = ttk.Frame(self.notebook)
        self.convert_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.merge_frame, text="图片合并")
        self.notebook.add(self.convert_frame, text="PNG转WEBP")
        
        self.setup_merge_tab()
        self.setup_convert_tab()
        
        # 关闭窗口时保存配置
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self):
        self.config = {
            'merge_output_dir': str(Path.home()),
            'convert_output_dir': str(Path.home())
        }
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
        except Exception:
            pass
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def setup_merge_tab(self):
        # 第一张图片选择
        ttk.Label(self.merge_frame, text="第一张图片:").pack(pady=5)
        self.image1_frame = ttk.Frame(self.merge_frame)
        self.image1_frame.pack(fill='x', padx=20)
        self.image1_path = tk.StringVar()
        ttk.Entry(self.image1_frame, textvariable=self.image1_path).pack(side='left', expand=True, fill='x')
        ttk.Button(self.image1_frame, text="选择文件", command=lambda: self.select_file(self.image1_path)).pack(side='right', padx=5)
        
        # 第二张图片选择
        ttk.Label(self.merge_frame, text="第二张图片:").pack(pady=5)
        self.image2_frame = ttk.Frame(self.merge_frame)
        self.image2_frame.pack(fill='x', padx=20)
        self.image2_path = tk.StringVar()
        ttk.Entry(self.image2_frame, textvariable=self.image2_path).pack(side='left', expand=True, fill='x')
        ttk.Button(self.image2_frame, text="选择文件", command=lambda: self.select_file(self.image2_path)).pack(side='right', padx=5)
        
        # 输出路径选择
        ttk.Label(self.merge_frame, text="保存位置:").pack(pady=5)
        self.merge_output_frame = ttk.Frame(self.merge_frame)
        self.merge_output_frame.pack(fill='x', padx=20)
        
        # 分成两行：第一行是目录，第二行是文件名
        self.merge_output_dir = tk.StringVar(value=self.config['merge_output_dir'])
        dir_frame = ttk.Frame(self.merge_output_frame)
        dir_frame.pack(fill='x', pady=2)
        ttk.Entry(dir_frame, textvariable=self.merge_output_dir).pack(side='left', expand=True, fill='x')
        ttk.Button(dir_frame, text="选择目录", command=self.select_merge_directory).pack(side='right', padx=5)
        
        self.merge_filename = tk.StringVar(value="merged.webp")
        file_frame = ttk.Frame(self.merge_output_frame)
        file_frame.pack(fill='x', pady=2)
        ttk.Entry(file_frame, textvariable=self.merge_filename).pack(side='left', expand=True, fill='x')
        ttk.Label(file_frame, text=".webp").pack(side='right')
        
        # 合并按钮
        ttk.Button(self.merge_frame, text="合并图片", command=self.merge_images).pack(pady=20)
    
    def setup_convert_tab(self):
        # PNG文件选择
        ttk.Label(self.convert_frame, text="选择PNG文件或文件夹:").pack(pady=5)
        self.png_frame = ttk.Frame(self.convert_frame)
        self.png_frame.pack(fill='x', padx=20)
        self.png_path = tk.StringVar()
        ttk.Entry(self.png_frame, textvariable=self.png_path).pack(side='left', expand=True, fill='x')
        ttk.Button(self.png_frame, text="选择文件/文件夹", command=self.select_png).pack(side='right', padx=5)
        
        # 输出路径选择
        ttk.Label(self.convert_frame, text="保存位置:").pack(pady=5)
        self.convert_output_frame = ttk.Frame(self.convert_frame)
        self.convert_output_frame.pack(fill='x', padx=20)
        self.convert_output_path = tk.StringVar(value=self.config['convert_output_dir'])
        ttk.Entry(self.convert_output_frame, textvariable=self.convert_output_path).pack(side='left', expand=True, fill='x')
        ttk.Button(self.convert_output_frame, text="选择位置", command=self.select_convert_directory).pack(side='right', padx=5)
        
        # 质量设置
        ttk.Label(self.convert_frame, text="最低质量 (1-100):").pack(pady=5)
        self.quality = tk.StringVar(value="80")
        ttk.Entry(self.convert_frame, textvariable=self.quality, width=10).pack()
        
        # 添加裁剪比率设置
        crop_frame = ttk.Frame(self.convert_frame)
        crop_frame.pack(pady=5)
        ttk.Label(crop_frame, text="裁剪比率 (1/n):").pack(side='left')
        self.crop_ratio = tk.StringVar(value="4")
        ttk.Entry(crop_frame, textvariable=self.crop_ratio, width=5).pack(side='left', padx=5)
        
        # 添加裁剪选项
        self.create_cropped = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.convert_frame, 
            text="同时创建中心裁剪版本", 
            variable=self.create_cropped
        ).pack(pady=5)
        
        # 转换按钮
        ttk.Button(self.convert_frame, text="转换为WEBP", command=self.convert_to_webp).pack(pady=20)
    
    def select_file(self, path_var):
        filename = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if filename:
            path_var.set(filename)
    
    def select_png(self):
        path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")]) or \
               filedialog.askdirectory()
        if path:
            self.png_path.set(path)
    
    def select_merge_directory(self):
        directory = filedialog.askdirectory(initialdir=self.merge_output_dir.get())
        if directory:
            self.merge_output_dir.set(directory)
            self.config['merge_output_dir'] = directory
    
    def select_convert_directory(self):
        directory = filedialog.askdirectory(initialdir=self.convert_output_path.get())
        if directory:
            self.convert_output_path.set(directory)
            self.config['convert_output_dir'] = directory
    
    def merge_images(self):
        try:
            if not all([self.image1_path.get(), self.image2_path.get()]):
                messagebox.showerror("错误", "请选择两张输入图片!")
                return
            
            if not self.merge_filename.get().strip():
                messagebox.showerror("错误", "请输入输出文件名!")
                return
            
            # 构建完整的输出路径
            output_path = Path(self.merge_output_dir.get()) / f"{self.merge_filename.get()}.webp"
            
            merge_images(
                self.image1_path.get(),
                self.image2_path.get(),
                str(output_path)
            )
            messagebox.showinfo("成功", f"图片合并完成!\n保存在: {output_path}")
        except Exception as e:
            messagebox.showerror("错误", f"合并失败: {str(e)}")
    
    def convert_to_webp(self):
        try:
            if not self.png_path.get():
                messagebox.showerror("错误", "请选择PNG文件或文件夹!")
                return
            
            quality = int(self.quality.get())
            if not (1 <= quality <= 100):
                messagebox.showerror("错误", "质量值必须在1-100之间!")
                return
            
            # 验证裁剪比率
            try:
                crop_ratio = int(self.crop_ratio.get())
                if crop_ratio < 2:
                    messagebox.showerror("错误", "裁剪比率必须大于或等于2!")
                    return
            except ValueError:
                messagebox.showerror("错误", "裁剪比率必须是整数!")
                return
            
            convert_png_to_webp(
                self.png_path.get(),
                self.convert_output_path.get(),
                quality,
                self.create_cropped.get(),
                crop_ratio
            )
            
            # 构建成功消息
            success_msg = "转换完成!"
            if self.create_cropped.get():
                success_msg += f"\n同时创建了中心裁剪版本 (原图的 1/{crop_ratio} 大小)"
            
            messagebox.showinfo("成功", success_msg)
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
    
    def on_closing(self):
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebpTools(root)
    root.mainloop() 