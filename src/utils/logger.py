import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import threading


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HISTORY_DIR = os.path.join(BASE_DIR, "data", "history")
GOLDEN_CASES_FILE = os.path.join(BASE_DIR, "data", "golden_cases.json")


@dataclass
class ContentLog:
    timestamp: str
    raw_text: str
    logic_summary: Dict[str, Any]
    zhihu_output: str
    xhs_output: str
    wechat_output: str


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def save_content_log(
    raw_text: str,
    logic_data: Dict[str, Any],
    zhihu_output: str,
    xhs_output: str,
    wechat_output: str
) -> str:
    ensure_dir(HISTORY_DIR)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"content_{timestamp}.json"
    filepath = os.path.join(HISTORY_DIR, filename)
    
    logic_summary = {
        "main_theme": logic_data.get("main_theme", ""),
        "key_points": logic_data.get("key_points", []),
        "target_audience": logic_data.get("target_audience", ""),
        "tone": logic_data.get("tone", ""),
        "structure": logic_data.get("structure", {})
    }
    
    content_log = ContentLog(
        timestamp=timestamp,
        raw_text=raw_text,
        logic_summary=logic_summary,
        zhihu_output=zhihu_output,
        xhs_output=xhs_output,
        wechat_output=wechat_output
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(content_log), f, ensure_ascii=False, indent=2)
    
    return filepath


def load_golden_cases() -> Dict[str, list]:
    if os.path.exists(GOLDEN_CASES_FILE):
        with open(GOLDEN_CASES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "zhihu": [],
        "xhs": [],
        "wechat": []
    }


def save_golden_case(
    platform: str,
    raw_text: str,
    generated_output: str,
    feedback: Optional[str] = None
) -> str:
    ensure_dir(os.path.dirname(GOLDEN_CASES_FILE))
    
    golden_cases = load_golden_cases()
    
    case = {
        "timestamp": datetime.now().isoformat(),
        "raw_text": raw_text,
        "generated_output": generated_output,
        "feedback": feedback
    }
    
    if platform not in golden_cases:
        golden_cases[platform] = []
    
    golden_cases[platform].append(case)
    
    with open(GOLDEN_CASES_FILE, "w", encoding="utf-8") as f:
        json.dump(golden_cases, f, ensure_ascii=False, indent=2)
    
    return GOLDEN_CASES_FILE


def get_golden_cases_by_platform(platform: str) -> list:
    golden_cases = load_golden_cases()
    return golden_cases.get(platform, [])


def get_all_golden_cases() -> Dict[str, list]:
    return load_golden_cases()
