# FontsCompress

根据网页项目实际使用的字符，自动扫描目录下所有 HTML/JS 文件，去除字体文件中未用字符，实现字体极致压缩。

## 功能特点

- 支持自动递归扫描目录下所有 `.html`、`.js`、`.jsx` 文件
- 提取所有可见文本和常用属性内容
- 仅保留字体文件中实际用到的字符，极致瘦身
- 显示压缩前后文件大小和压缩比例

## 安装

1. 克隆此仓库：

```bash
git clone https://github.com/yourusername/FontsCompress.git
cd FontsCompress
```

2. 安装依赖：

```bash
pip install fonttools
```

## 使用方法

基本用法：

```bash
python font_compress.py -d 你的项目目录 -f 原字体.ttf -o 输出字体.ttf
```

例如：

```bash
python font_compress.py -d ./web_project -f ./fonts/example.ttf -o ./fonts/example.min.ttf
```

## 参数说明

- `-d, --directory`：包含 HTML/JS 文件的目录路径（必需）
- `-f, --font`：原始字体文件路径（TTF/OTF，必需）
- `-o, --output`：输出字体文件路径（必需）

## 注意事项

- 工具会自动递归扫描目录下所有 `.html`、`.js`、`.jsx`、`.ts`、`tsx` 文件。
- 确保输入文件为 UTF-8 编码。
- 支持 TTF/OTF 格式字体。
- 建议在生产环境前充分测试压缩后字体。
