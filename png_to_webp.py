from PIL import Image
import os
import sys
from pathlib import Path

def convert_png_to_webp(input_path, output_path=None, min_quality=80):
    """
    将PNG图片转换为WEBP格式，优先保证清晰度
    
    参数:
        input_path: 输入PNG文件路径或目录
        output_path: 输出路径（可选）
        min_quality: 最低质量限制（默认80，范围0-100）
    """
    try:
        # 如果输入是目录，则批量处理
        if os.path.isdir(input_path):
            input_dir = Path(input_path)
            # 如果没有指定输出路径，则在输入目录创建webp子目录
            output_dir = Path(output_path) if output_path else input_dir / 'webp'
            
            # 确保输出目录存在
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise Exception(f"无法创建输出目录 {output_dir}: {str(e)}")
            
            # 处理目录中的所有PNG文件
            success_count = 0
            error_count = 0
            for png_file in input_dir.glob('*.png'):
                try:
                    webp_file = output_dir / f"{png_file.stem}.webp"
                    convert_single_file(png_file, webp_file, min_quality)
                    success_count += 1
                except Exception as e:
                    print(f"转换失败 {png_file.name}: {str(e)}")
                    error_count += 1
            
            if error_count > 0:
                print(f"\n转换完成: {success_count}个成功, {error_count}个失败")
            return
                
        else:
            # 处理单个文件
            input_file = Path(input_path)
            if not input_file.exists():
                raise Exception(f"找不到输入文件: {input_path}")
            
            if output_path:
                output_dir = Path(output_path)
                # 确保输出目录存在
                try:
                    output_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    raise Exception(f"无法创建输出目录 {output_dir}: {str(e)}")
                output_file = output_dir / f"{input_file.stem}.webp"
            else:
                output_file = input_file.with_suffix('.webp')
            
            convert_single_file(input_file, output_file, min_quality)
            
    except Exception as e:
        raise Exception(f"转换失败: {str(e)}")

def convert_single_file(input_file, output_file, min_quality):
    """转换单个文件"""
    try:
        # 打开PNG图片
        with Image.open(input_file) as img:
            # 如果图片是RGBA模式但没有透明通道，转换为RGB
            if img.mode == 'RGBA' and not has_transparency(img):
                img = img.convert('RGB')
            
            # 获取原始文件大小
            original_size = os.path.getsize(input_file)
            
            # 使用二分查找寻找最佳质量参数
            quality_min = min_quality
            quality_max = 100
            best_quality = quality_max
            best_size = float('inf')
            
            # 确保输出文件的父目录存在
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            while quality_min <= quality_max:
                current_quality = (quality_min + quality_max) // 2
                
                # 临时保存并检查文件大小
                temp_output = str(output_file) + '.temp'
                img.save(temp_output, 'WEBP', 
                        quality=current_quality, 
                        method=6,  # 最佳压缩方法
                        lossless=False)  # 使用有损压缩
                
                current_size = os.path.getsize(temp_output)
                
                # 如果当前结果更好，保存它
                if current_size < best_size:
                    best_size = current_size
                    best_quality = current_quality
                    # 重命名临时文件为最终文件
                    try:
                        if os.path.exists(output_file):
                            os.remove(output_file)
                        os.rename(temp_output, output_file)
                    except Exception:
                        if os.path.exists(temp_output):
                            os.remove(temp_output)
                        raise
                else:
                    if os.path.exists(temp_output):
                        os.remove(temp_output)
                
                # 调整搜索范围
                if current_size > original_size * 0.5:  # 如果文件大于原文件的50%
                    quality_max = current_quality - 1
                else:
                    quality_min = current_quality + 1
            
            compression_ratio = (best_size / original_size) * 100
            print(f"转换完成: {input_file}")
            print(f"原始大小: {original_size/1024:.1f}KB")
            print(f"转换后大小: {best_size/1024:.1f}KB")
            print(f"压缩率: {compression_ratio:.1f}%")
            print(f"使用的质量参数: {best_quality}")
            print("-" * 50)
            
    except Exception as e:
        raise Exception(f"处理文件失败: {str(e)}")

def has_transparency(img):
    """检查图片是否包含透明通道"""
    if img.mode == 'RGBA':
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 转换单个文件: python png_to_webp.py input.png [output.webp]")
        print("2. 转换整个目录: python png_to_webp.py input_directory [output_directory]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_png_to_webp(input_path, output_path)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1) 