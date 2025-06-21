import re
import argparse
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options, save_font
import logging

# 配置日志格式和级别
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)


def extract_chars_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        # 移除脚本、样式等不显示内容的标签及其内容
        html = re.sub(r'<(script|style|noscript|meta)[^>]*?>[\s\S]*?<\/\\1>', '', html, flags=re.IGNORECASE)
        # 移除所有HTML标签，保留纯文本
        text = re.sub(r'<[^>]+>', '', html)
        # 提取常见属性内容
        attrs = re.findall(r'(alt|title|placeholder|aria-label|data-content)\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
        for _, val in attrs:
            text += ' ' + val
        # 提取style属性中的content内容
        style_contents = re.findall(r'style\s*=\s*["\'][^"\']*content:\s*["\'](.*?)["\']', html, re.IGNORECASE)
        text += ''.join(style_contents)
        return set(text)


def extract_chars_from_js(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
        chars = set()
        # 匹配单双引号和模板字符串
        string_patterns = [
            r'"(.*?)"',  # 双引号字符串
            r"'(.*?)'",  # 单引号字符串
            r'`(.*?)`'    # 模板字符串
        ]
        for pattern in string_patterns:
            matches = re.findall(pattern, js_content, re.DOTALL)
            for match in matches:
                # 模板字符串去除${...}表达式
                if pattern == r'`(.*?)`':
                    match = re.sub(r'\${.*?}', '', match)
                chars.update(match)
        # 匹配JSX文本内容
        jsx_matches = re.findall(r'[>}]\t*([^<{]+?)\t*[<{]', js_content)
        for match in jsx_matches:
            chars.update(match)
        # 匹配console输出中的字符串
        log_matches = re.findall(r'console\.(log|warn|error|info)\(([^)]+)\)', js_content)
        for _, args in log_matches:
            # 分别提取双引号和单引号字符串
            arg_strings1 = re.findall(r'"(.*?)"', args)
            arg_strings2 = re.findall(r"'(.*?)'", args)
            for s in arg_strings1 + arg_strings2:
                chars.update(s)
        return chars


def collect_chars_from_directory(directory):
    all_chars = set()
    file_count = 0
    dir_path = Path(directory)
    for file_path in dir_path.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            try:
                if ext == '.html':
                    all_chars.update(extract_chars_from_html(str(file_path)))
                    file_count += 1
                elif ext in ('.js', '.jsx', '.ts', '.tsx'):
                    all_chars.update(extract_chars_from_js(str(file_path)))
                    file_count += 1
            except Exception as e:
                logging.warning(f'处理文件 {file_path} 时出错: {e}')
    logging.info(f'已处理 {file_count} 个文件')
    return all_chars


def create_font_subset(font_path, output_path, char_set):
    font = TTFont(font_path)
    options = Options()
    options.desubroutinize = True
    options.hinting = False
    options.legacy_cmap = False
    options.symbol_cmap = False
    unicode_set = set()
    for char in char_set:
        try:
            unicode_set.add(ord(char))
        except Exception as e:
            logging.warning(f'跳过无效字符: {char} - {e}')
    # 补充常用空白符，防止网页排版错乱
    basic_chars = {ord(c) for c in ' \n\t\r'}
    unicode_set |= basic_chars
    if unicode_set:
        subsetter = Subsetter(options=options)
        subsetter.populate(unicodes=unicode_set)
        subsetter.subset(font)
    save_font(font, output_path, options)
    font.close()


def main():
    '''
    命令行入口，参数说明：
    -d/--directory：待扫描的项目目录
    -f/--font：原始字体文件路径
    -o/--output：输出字体文件路径
    '''
    parser = argparse.ArgumentParser(description='扫描目录下所有.js和.html文件，提取所有显示字符并保留到字体文件')
    parser.add_argument('-d', '--directory', required=True, help='包含HTML/JS文件的目录路径')
    parser.add_argument('-f', '--font', required=True, help='原始字体文件路径 (TTF/OTF)')
    parser.add_argument('-o', '--output', required=True, help='输出字体文件路径')
    args = parser.parse_args()
    logging.info('收集网页文件中使用的字符...')
    char_set = collect_chars_from_directory(args.directory)
    logging.info(f'发现 {len(char_set)} 个唯一字符')
    logging.info('创建字体子集...')
    create_font_subset(args.font, args.output, char_set)
    orig_size = Path(args.font).stat().st_size
    new_size = Path(args.output).stat().st_size
    reduction = (1 - new_size / orig_size) * 100
    logging.info(f'压缩完成! 文件大小: {orig_size//1024}KB → {new_size//1024}KB')
    logging.info(f'减小了 {reduction:.1f}%')


if __name__ == '__main__':
    main()
