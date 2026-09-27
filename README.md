# Skills

我的专属个人技能库。

**作者**：小猫会发光

## 简介

本仓库用于存放个人自定义的技能（Skills）。每个技能是一个独立的目录，包含 `SKILL.md` 定义文件及其相关资源，可被支持 Skills 规范的工具按需加载调用。

## 目录结构

```
skills/
├── <skill-name>/
│   ├── SKILL.md        # 技能定义（YAML frontmatter + 指令）
│   └── ...             # 其他辅助文件（脚本、模板、参考文档等）
└── ...
```

## 添加新技能

1. 在 `skills/` 下创建以技能名命名的目录（小写、kebab-case）。
2. 在目录中创建 `SKILL.md`，头部包含 YAML frontmatter：

   ```markdown
   ---
   name: my-skill
   description: 一句话描述这个技能做什么、何时触发
   ---

   （技能的具体指令内容）
   ```

3. 按需添加脚本、模板等辅助文件。

## 许可证

[Apache-2.0](LICENSE)
