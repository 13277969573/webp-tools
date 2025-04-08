   # Webp 工具箱

   一个简单易用的图片处理工具，提供图片合并和PNG转WEBP功能。

   ## 功能特点

   - **图片合并**：将两张16:9的PNG图片合并成一张，中间用斜线分割
   - **PNG转WEBP**：将PNG图片转换为WEBP格式，保证清晰度的同时优化文件大小
   - **简单易用**：图形界面操作，无需命令行
   - **高质量输出**：自动寻找最佳压缩参数
   - **配置记忆**：记住上次的保存位置

   ## 安装方法

   ### 方法一：下载可执行文件（Windows用户）

   1. 在 [Releases](https://github.com/你的用户名/webp-tools/releases) 页面下载最新版本的 `Webp工具箱.zip`
   2. 解压缩后双击 `Webp工具箱.exe` 运行

   ### 方法二：从源码运行

   1. 克隆仓库
      ```
      git clone https://github.com/你的用户名/webp-tools.git
      cd webp-tools
      ```

   2. 安装依赖
      ```
      pip install -r requirements.txt
      ```

   3. 运行程序
      ```
      python webp_tools.py
      ```

    4. 打包
      ```
      python -m PyInstaller build_exe.spec --clean --noconfirm
      ```

   ## 使用说明

   ### 图片合并

   1. 选择两张PNG格式的图片
   2. 设置保存位置和文件名
   3. 点击"合并图片"按钮
   4. 生成的图片将保存为WEBP格式

   ### PNG转WEBP

   1. 选择单个PNG文件或包含PNG文件的文件夹
   2. 设置保存位置
   3. 调整质量参数（默认80）
   4. 点击"转换为WEBP"按钮
   5. 转换后的图片将保存在指定位置

   ## 自行打包

   如果你想自己打包可执行文件：
