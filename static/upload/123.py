import os
import commons
import log4j
# 定义字典，用于保存找到的开源组件及其版本号
used_components = {}
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".py"):
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                code_len = len(lines)
                source = f.read()
                tree = ast.parse(source)
                #将代码传换成代码树，用ast.walk遍历节点
                """
                这是一个多行注释
                123123
                123123
                """
                comment_lines = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)]
                num_comment_lines = len(comment_lines)
                stats = {
                    '代码总行数': code_len,
                    '代码注释行数': num_comment_lines,
                }


