# FontsCompress

根据网页项目实际使用的字符，自动扫描目录下所有 HTML/JS 文件，去除字体文件中未用字符，实现字体极致压缩。

## 功能特点

- 支持自动递归扫描目录下所有 `html`、`js`、`jsx`、`ts`、`tsx` 文件。
- 提取所有可见文本和常用属性内容。
- 仅保留字体文件中实际用到的字符，极致瘦身。

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
python FontCompress.py -d {项目目录} -f {原字体.ttf} -o {输出字体.ttf}
```

## 参数说明

- `-d, --directory`：包含 HTML/JS 文件的目录路径（必需）
- `-f, --font`：原始字体文件路径（TTF/OTF，必需）
- `-o, --output`：输出字体文件路径（可选，默认 Output.ttf）
- `-k, --keep`：额外需要保留的字符（如：`-k "￥①②ABC"`，可选）

> 程序会默认保留所有英文字母、数字和常用英文符号，无需手动指定。

## 注意事项

- 确保输入文件为 UTF-8 编码。
- 支持 TTF/OTF 格式字体。
- 建议在生产环境前充分测试压缩后字体。
