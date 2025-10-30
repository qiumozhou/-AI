"""
下载Pikafish所需的NNUE文件
"""

import sys
import urllib.request
from pathlib import Path

# 设置UTF-8编码
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def download_nnue():
    """下载pikafish.nnue文件"""
    print("="*60)
    print("下载Pikafish NNUE评估文件")
    print("="*60)
    print()
    
    # NNUE文件URL（来自Pikafish官方仓库）
    nnue_url = "https://github.com/official-pikafish/Networks/releases/download/master-net/pikafish.nnue"
    
    # 保存路径
    engine_dir = Path("engine")
    engine_dir.mkdir(exist_ok=True)
    nnue_path = engine_dir / "pikafish.nnue"
    
    # 检查文件是否已存在
    if nnue_path.exists():
        size_mb = nnue_path.stat().st_size / (1024 * 1024)
        print(f"✓ NNUE文件已存在: {nnue_path}")
        print(f"  文件大小: {size_mb:.1f} MB")
        
        response = input("\n是否重新下载？(y/N): ").strip().lower()
        if response != 'y':
            print("跳过下载")
            return True
        print()
    
    print(f"下载URL: {nnue_url}")
    print(f"保存到: {nnue_path.absolute()}")
    print()
    print("开始下载（文件约45MB，请耐心等待）...")
    print()
    
    def show_progress(block_num, block_size, total_size):
        """显示下载进度"""
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(downloaded / total_size * 100, 100)
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            print(f"\r进度: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='')
    
    try:
        urllib.request.urlretrieve(nnue_url, nnue_path, reporthook=show_progress)
        print()  # 换行
        
        # 验证文件
        if nnue_path.exists():
            size_mb = nnue_path.stat().st_size / (1024 * 1024)
            print()
            print("="*60)
            print("✓ 下载成功！")
            print("="*60)
            print(f"文件: {nnue_path.absolute()}")
            print(f"大小: {size_mb:.1f} MB")
            print()
            print("现在可以正常使用Pikafish引擎分析了！")
            return True
        else:
            print("\n✗ 下载失败：文件不存在")
            return False
            
    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
        print()
        print("手动下载方法：")
        print("1. 访问: https://github.com/official-pikafish/Networks/releases")
        print("2. 下载 pikafish.nnue 文件")
        print(f"3. 放到: {nnue_path.absolute()}")
        return False

if __name__ == "__main__":
    success = download_nnue()
    
    if success:
        print("\n下一步:")
        print("  python test_engine.py  # 测试引擎是否正常")
        print("  python recognize_board.py images/1.png --analyze  # 完整测试")

