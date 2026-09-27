# -*- coding: utf-8 -*-
"""Programmatic grader for feihua-wenxue iteration outputs.

Walks iteration-N/eval-*/<config>/run-1/outputs/output.txt, checks the hard
requirements, and writes grading.json into each run directory.
"""
import json
import os
import re
import sys

TOPICS = {
    "eval-1-overtime-jiaban": "加班",
    "eval-2-kaoyan-exam": "考研",
    "eval-3-casual-jianfei": "减肥",
}

BANNED_CLOSING = "听君一席话，如听一席话"
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F0FF]"
)


def check(eval_name, text):
    topic = TOPICS[eval_name]
    stripped = text.strip()
    compact = re.sub(r"\s", "", stripped)
    results = []

    count = compact.count(topic)
    results.append({
        "text": f"输出包含话题词「{topic}」",
        "passed": count >= 1,
        "evidence": f"话题词出现 {count} 次",
    })
    results.append({
        "text": f"话题词「{topic}」重复出现至少 3 次，形成套娃感",
        "passed": count >= 3,
        "evidence": f"话题词出现 {count} 次",
    })

    n = len(compact)
    results.append({
        "text": "全段字数在 50~200 字之间（以去除空白后的字符数为准）",
        "passed": 50 <= n <= 200,
        "evidence": f"去除空白后共 {n} 字",
    })

    sentences = [s for s in re.split(r"[。！？!?\n]", stripped) if s.strip()]
    last = sentences[-1].strip() if sentences else ""
    results.append({
        "text": f"结尾句点题：最后一句包含话题词「{topic}」",
        "passed": topic in last,
        "evidence": f"结尾句：「{last}」",
    })

    results.append({
        "text": "不包含固定套话「听君一席话，如听一席话」",
        "passed": BANNED_CLOSING not in compact,
        "evidence": "未出现该套话" if BANNED_CLOSING not in compact else "出现了该套话",
    })

    problems = []
    if "\n" in stripped:
        problems.append("包含换行（非一段式）")
    if re.search(r"(?m)^\s*(#{1,6}\s|[-*+]\s|\d+[.、)]\s)", stripped):
        problems.append("包含标题或列表标记")
    if EMOJI_RE.search(stripped):
        problems.append("包含 emoji")
    if "废话文学" in compact:
        problems.append("出现「废话文学」字样（疑似自我解释）")
    results.append({
        "text": "输出为一段式纯文本：无标题、列表、emoji，且不自我解释「这是废话文学」",
        "passed": not problems,
        "evidence": "；".join(problems) if problems else "单段纯文本，无格式标记/emoji/自我解释",
    })
    return results


def main(iteration_dir):
    for eval_name in TOPICS:
        eval_dir = os.path.join(iteration_dir, eval_name)
        if not os.path.isdir(eval_dir):
            continue
        for config in ("with_skill", "without_skill"):
            run_dir = os.path.join(eval_dir, config, "run-1")
            out = os.path.join(run_dir, "outputs", "output.txt")
            if not os.path.isfile(out):
                print(f"MISSING: {out}")
                continue
            with open(out, encoding="utf-8") as f:
                text = f.read()
            expectations = check(eval_name, text)
            passed = sum(1 for e in expectations if e["passed"])
            grading = {
                "expectations": expectations,
                "summary": {
                    "passed": passed,
                    "failed": len(expectations) - passed,
                    "total": len(expectations),
                    "pass_rate": round(passed / len(expectations), 2),
                },
            }
            grading_path = os.path.join(run_dir, "grading.json")
            with open(grading_path, "w", encoding="utf-8") as f:
                json.dump(grading, f, ensure_ascii=False, indent=2)
            print(f"{eval_name}/{config}: {passed}/{len(expectations)}")


if __name__ == "__main__":
    main(sys.argv[1])
