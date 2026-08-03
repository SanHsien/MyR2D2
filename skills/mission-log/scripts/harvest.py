#!/usr/bin/env python3
# harvest.py — mission-log 零 token 收割器(原型 v0)
# 從 ~/.claude/projects/*/*.jsonl 抽出指定日期(當地時區)的活動骨架。
# 純標準庫、不呼叫任何模型;可整檔經 ssh 餵給遠端 python3(單檔自包含)。
# 用法: python3 harvest.py [--date YYYY-MM-DD] [--dir DIR] [--format md|jsonl]
import json, sys, os, glob, argparse, datetime

def parse_ts(s):
    try:
        return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone()
    except Exception:
        return None

def user_text(msg):
    """抽出「真人打的字」:排除 tool_result/系統注入(<開頭)/指令包裝。"""
    c = msg.get('content')
    texts = []
    if isinstance(c, str):
        texts = [c]
    elif isinstance(c, list):
        texts = [b.get('text', '') for b in c if isinstance(b, dict) and b.get('type') == 'text']
    for t in texts:
        t = t.strip()
        if t and not t.startswith('<') and not t.startswith('Caveat:'):
            return t
    return None

def harvest(projects_dir, day):
    day_start = datetime.datetime.combine(day, datetime.time.min).astimezone()
    day_end = day_start + datetime.timedelta(days=1)
    sessions = {}
    # mtime 粗篩:整檔最後修改早於當天開始的不可能含當天資料
    for tx in glob.glob(os.path.join(projects_dir, '*', '*.jsonl')):
        try:
            if datetime.datetime.fromtimestamp(os.path.getmtime(tx)).astimezone() < day_start:
                continue
        except OSError:
            continue
        proj = os.path.basename(os.path.dirname(tx))
        sid = os.path.basename(tx)[:8]
        key = (proj, sid)
        with open(tx, errors='replace') as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                ts = parse_ts(obj.get('timestamp') or '')
                if not ts or not (day_start <= ts < day_end):
                    continue
                s = sessions.setdefault(key, {
                    'project': proj.split('-')[-1] or proj, 'session': sid,
                    'first': ts, 'last': ts, 'turns': 0, 'tokens': 0,
                    'tools': {}, 'models': set(), 'prompts': [], 'branch': None, '_cwd': None})
                s['first'] = min(s['first'], ts); s['last'] = max(s['last'], ts)
                if obj.get('cwd') and not s['_cwd']:
                    s['_cwd'] = obj['cwd']
                    s['project'] = os.path.basename(obj['cwd'].rstrip('/')) or s['project']
                if obj.get('gitBranch') and not s['branch']:
                    s['branch'] = obj['gitBranch']
                m = obj.get('message')
                if not isinstance(m, dict):
                    continue
                if obj.get('type') == 'user' and not obj.get('isMeta'):
                    t = user_text(m)
                    if t:
                        s['prompts'].append(t[:70])
                u = m.get('usage')
                if isinstance(u, dict):
                    s['turns'] += 1
                    s['tokens'] += u.get('input_tokens', 0) + u.get('output_tokens', 0) + u.get('cache_creation_input_tokens', 0)
                if m.get('model') and m['model'] != '<synthetic>':
                    s['models'].add(m['model'])
                c = m.get('content')
                if isinstance(c, list):
                    for b in c:
                        if isinstance(b, dict) and b.get('type') == 'tool_use':
                            s['tools'][b['name']] = s['tools'].get(b['name'], 0) + 1
    return sorted(sessions.values(), key=lambda s: s['first'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=None)
    ap.add_argument('--dir', default=os.path.expanduser('~/.claude/projects'))
    ap.add_argument('--format', choices=['md', 'jsonl'], default='md')
    a = ap.parse_args()
    day = datetime.date.fromisoformat(a.date) if a.date else (datetime.date.today() - datetime.timedelta(days=1))
    rows = harvest(a.dir, day)
    host = os.uname().nodename.split('.')[0]
    if a.format == 'jsonl':
        for s in rows:
            out = dict(s, first=s['first'].strftime('%H:%M'), last=s['last'].strftime('%H:%M'),
                       models=sorted(s['models']), host=host,
                       tools=dict(sorted(s['tools'].items(), key=lambda x: -x[1])[:6]),
                       prompts=s['prompts'][:5] + (['…+%d' % (len(s['prompts']) - 5)] if len(s['prompts']) > 5 else []))
            print(json.dumps(out, ensure_ascii=False, default=str))
        return
    print(f"## {day} @ {host} — {len(rows)} 個活躍 session")
    for s in rows:
        tools = ' '.join(f"{k}×{v}" for k, v in sorted(s['tools'].items(), key=lambda x: -x[1])[:4])
        models = ','.join(m.split('-')[1] for m in sorted(s['models']))
        print(f"\n### {s['first'].strftime('%H:%M')}–{s['last'].strftime('%H:%M')}  {s['project']}"
              f"{'@' + s['branch'] if s['branch'] else ''}  ({s['turns']} turns, {s['tokens']:,} tok, {models})")
        print(f"  工具: {tools or '（無）'}")
        for p in s['prompts'][:5]:
            print(f"  › {p}")
        if len(s['prompts']) > 5:
            print(f"  › …共 {len(s['prompts'])} 句")

if __name__ == '__main__':
    main()
