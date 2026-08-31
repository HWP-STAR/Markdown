import os
import shutil
from pathlib import Path

class FileOrganizer:
    # 定义文件分类规则
    FILE_CATEGORIES = {
        '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'],
        '文档': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.md'],
        '视频': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
        '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        '代码': ['.py', '.java', '.cpp', '.c', '.html', '.css', '.js', '.json', '.xml'],
        '安装包': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
        '其他': []  # 未分类的文件
    }
    
    def __init__(self, target_directory):
        """
        初始化文件整理器
        
        Args:
            target_directory: 需要整理的目标目录路径
        """
        self.target_directory = Path(target_directory)
        if not self.target_directory.exists():
            raise ValueError(f"目录 {target_directory} 不存在")
    
    def get_file_category(self, file_path):
        """
        根据文件扩展名获取文件类别
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件类别名称
        """
        extension = file_path.suffix.lower()
        
        for category, extensions in self.FILE_CATEGORIES.items():
            if extension in extensions:
                return category
        
        return '其他'
    
    def organize_files(self, dry_run=False):
        """
        整理文件
        
        Args:
            dry_run: 如果为True，只显示将要执行的操作，不实际移动文件
        """
        print(f"开始整理目录: {self.target_directory}")
        print("-" * 50)
        
        # 统计信息
        stats = {category: 0 for category in self.FILE_CATEGORIES.keys()}
        stats['总文件数'] = 0
        moved_files = 0
        skipped_files = 0
        
        # 遍历目录中的所有文件
        for item in self.target_directory.iterdir():
            if item.is_file():  # 只处理文件，不处理文件夹
                stats['总文件数'] += 1
                
                # 获取文件类别
                category = self.get_file_category(item)
                stats[category] = stats.get(category, 0) + 1
                
                # 创建目标文件夹
                category_folder = self.target_directory / category
                
                # 如果文件已经在对应的分类文件夹中，跳过
                if item.parent == category_folder:
                    print(f"跳过: {item.name} (已在分类文件夹中)")
                    skipped_files += 1
                    continue
                
                # 目标文件路径
                destination = category_folder / item.name
                
                # 处理文件名冲突
                if destination.exists():
                    base_name = item.stem
                    extension = item.suffix
                    counter = 1
                    while destination.exists():
                        new_name = f"{base_name}_{counter}{extension}"
                        destination = category_folder / new_name
                        counter += 1
                
                # 执行移动操作
                if dry_run:
                    print(f"[模拟] 将 {item.name} -> {category}/{destination.name}")
                else:
                    # 创建目标文件夹
                    category_folder.mkdir(exist_ok=True)
                    # 移动文件
                    shutil.move(str(item), str(destination))
                    print(f"已移动: {item.name} -> {category}/{destination.name}")
                    moved_files += 1
        
        # 显示统计信息
        print("\n" + "=" * 50)
        print("整理完成！统计信息:")
        print("-" * 50)
        for category, count in stats.items():
            if category != '总文件数':
                print(f"{category}: {count} 个文件")
        print(f"总文件数: {stats['总文件数']} 个")
        print(f"实际移动: {moved_files} 个文件")
        print(f"跳过文件: {skipped_files} 个文件")
        
        if dry_run:
            print("\n提示: 这是模拟运行，实际文件未被移动")
            print("要执行实际操作，请设置 dry_run=False")

# 使用示例
if __name__ == "__main__":
    # 要整理的目录路径
    directory_path = "/home/my_llm/Downloads"  # 修改为你的目录
    
    try:
        # 创建整理器实例
        organizer = FileOrganizer(directory_path)
        
        # 先模拟运行，查看效果
        print("=== 模拟运行 ===")
        organizer.organize_files(dry_run=True)
        
        # 确认后实际执行
        print("\n" + "=" * 50)
        response = input("是否执行实际整理？(y/n): ")
        if response.lower() == 'y':
            organizer.organize_files(dry_run=False)
        else:
            print("已取消操作")
            
    except Exception as e:
        print(f"错误: {e}")
