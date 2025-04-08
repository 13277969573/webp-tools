from PIL import Image, ImageDraw
import math
import os

def merge_images(image1_path, image2_path, output_path, final_width=960, target_size_kb=35):
    # 打开两张图片
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
    
    # 计算处理尺寸（保持原始宽高比）
    aspect_ratio = 16/9
    process_width = img1.width  # 使用原始宽度
    process_height = int(process_width / aspect_ratio)
    
    # 调整图片高度以适应16:9（如果需要的话）
    img1 = img1.resize((process_width, process_height))
    img2 = img2.resize((process_width, process_height))
    
    # 创建最终图片
    result = Image.new('RGBA', (process_width, process_height), (0, 0, 0, 0))
    
    # 定义斜线位置
    split_x = process_width // 2  # 中心点
    split_offset = int(process_width * 50/960)  # 按比例计算偏移
    
    # 计算偏移量（25%）
    offset = int(process_width * 0.25)
    
    # 创建遮罩
    mask = Image.new('L', (process_width, process_height), 0)
    draw_mask = ImageDraw.Draw(mask)
    
    # 绘制斜线遮罩
    draw_mask.polygon([
        (split_x, 0),          # 顶部中点
        (process_width, 0),    # 右上角
        (process_width, process_height),  # 右下角
        (split_x + split_offset, process_height)  # 底部中点偏右
    ], fill=255)
    
    # 创建临时画布来放置图片
    temp1 = Image.new('RGBA', (process_width, process_height), (0, 0, 0, 0))
    temp2 = Image.new('RGBA', (process_width, process_height), (0, 0, 0, 0))
    
    # 将图片放到对应位置（向左和向右偏移）
    temp1.paste(img1, (-offset, 0))  # 左图向左偏移
    temp2.paste(img2, (offset, 0))   # 右图向右偏移
    
    # 合成图片
    result = Image.composite(temp2, temp1, mask)
    
    # 添加白色分割线（增加线宽以适应高分辨率）
    draw = ImageDraw.Draw(result)
    line_width = max(3, int(process_width * 3/960))  # 根据分辨率调整线宽
    draw.line(
        [(split_x, 0), (split_x + split_offset, process_height)],
        fill='white',
        width=line_width
    )
    
    # 最后才调整到目标尺寸
    if process_width != final_width:
        final_height = int(final_width / aspect_ratio)
        result = result.resize((final_width, final_height), Image.Resampling.LANCZOS)

    # 二分法查找合适的质量参数
    quality_min, quality_max = 50, 95
    target_size = target_size_kb * 1024  # 转换为字节
    best_quality = quality_min
    
    while quality_min <= quality_max:
        current_quality = (quality_min + quality_max) // 2
        
        # 临时保存并检查文件大小
        temp_output = output_path + '.temp'
        result.save(temp_output, 'WEBP', quality=current_quality, method=6)
        current_size = os.path.getsize(temp_output)
        
        # 删除临时文件
        os.remove(temp_output)
        
        # 调整搜索范围
        if current_size > target_size:
            quality_max = current_quality - 1
        else:
            best_quality = current_quality
            quality_min = current_quality + 1
    
    # 使用找到的最佳质量参数保存
    result.save(output_path, 'WEBP', quality=best_quality, method=6)

# 使用示例
if __name__ == "__main__":
    merge_images(
        'image1.png',
        'image2.png',
        'output.webp',
        target_size_kb=35  # 目标大小为35KB
    ) 