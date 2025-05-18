# CATIA 自动化助手程序说明
## 程序概述
该程序是一个基于 DeepSeek AI 大模型的 CATIA 自动化助手，用于将用户的自然语言指令转换为标准的 CATIA 操作命令。程序专注于处理 CATIA 相关的建模和设计指令，能够自动识别并过滤非 CATIA 相关的对话内容。

## 主要功能
1. 自然语言处理：将用户输入的中文指令转换为结构化的 CATIA 命令
2. 指令验证：自动验证指令是否为有效的 CATIA 操作
3. 模块支持：支持以下 CATIA 模块的操作
   - PartDesign（零件设计）
   - Sketcher（草图设计）
   - Assembly（装配设计）
   - Drafting（工程图设计）
## 技术特点
1. 使用 DeepSeek-R1-Distill-Qwen-1.5B 模型进行自然语言处理
2. 采用 JSON 格式进行命令结构化
3. 内置错误处理和异常管理
4. 可配置的 API 设置（通过 settings.ini）
## 配置要求
程序需要在 config/settings.ini 文件中配置以下参数：

- deepseek_url：DeepSeek API 的访问地址
- api_key：API 访问密钥
## 输出格式
程序将用户指令转换为标准的 JSON 格式：

```json
{
  "operation": "模块.命令",
  "parameters": {
    "参数1": 值,
    "参数2": 值,
    ...
  }
}
 ```

## 使用限制
1. 仅处理 CATIA 相关的建模和设计指令
2. 对于非 CATIA 相关的对话会返回相应的错误提示
3. 仅支持预定义的 CATIA 模块操作
## 错误处理
程序包含以下错误处理机制：

1. API 通信异常处理
2. 非 CATIA 指令过滤
3. 无效命令结构检测
4. 不支持模块验证
## 注意事项
1. 确保 config/settings.ini 配置文件正确设置
2. API 调用需要稳定的网络连接
3. 建议使用清晰、规范的 CATIA 操作描述以获得最佳效果