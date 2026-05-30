# 俄罗斯方块 (Tetris)

使用 Python 和 [pygame](https://www.pygame.org/) 实现的经典俄罗斯方块小游戏。

## 功能特性

- 标准 10×20 游戏区域，七种经典方块（I、O、T、S、Z、J、L）
- 方块旋转，带简单 wall kick（贴墙时自动左右微调）
- 消行计分，等级随消行数提升，下落速度逐渐加快
- 侧边栏显示分数、等级、消行数及下一个方块预览
- 游戏结束后可按 `R` 重新开始

## 环境要求

- Python 3.9+
- pygame 2.5.0+

## 安装与运行

```bash
# 克隆仓库
git clone git@github.com:lsptest06demo-ui/demo_repo.git
cd demo_repo

# 创建并激活虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动游戏
python tetris.py
```

## 操作说明

| 按键 | 功能 |
|------|------|
| `←` `→` | 左右移动 |
| `↑` | 旋转方块 |
| `↓` | 软降（加速下落，+1 分） |
| `空格` | 硬降（瞬间落底，每格 +2 分） |
| `R` | 重新开始 |
| `Esc` | 退出游戏 |

## 计分规则

| 一次消除行数 | 得分 |
|-------------|------|
| 1 行 | 100 |
| 2 行 | 300 |
| 3 行 | 500 |
| 4 行 | 800 |

- 每消除 10 行，等级 +1，方块下落速度加快
- 软降每格 +1 分，硬降每格 +2 分

## 项目结构

```
.
├── tetris.py          # 游戏主程序
├── requirements.txt   # Python 依赖
└── README.md
```

## 许可证

见 [LICENSE](./LICENSE) 文件。
