"""
Minimal end-to-end loop: Claude writes the spec, this program renders it — no model call for HTML.

  pip install anthropic
  export ANTHROPIC_API_KEY=...   (and optionally TOJO_MODEL)
  python3 api_example.py "Consultants finish rounds by about 11..." --tag "@Point1"

In production, the app keeps the conversation history, prepends the persona/register/domain chunks,
and sends the canvas HTML to the canvas pane and the chat JSON to its own chat UI.
"""
import argparse, json, os, subprocess, sys
import diagnosis_html

MODEL = os.environ.get('TOJO_MODEL', 'claude-sonnet-5')

def system_prompt():
    out = subprocess.run([sys.executable, os.path.join(diagnosis_html.HERE, 'diagnosis_html.py'), 'prompt'], capture_output=True, text=True, check=True)
    base = os.environ.get('TOJO_BASE_PROMPT_FILE')          # 00-core, persona, register, 05, domain chunks…
    prefix = open(base, encoding='utf-8').read() + '\n\n' if base else ''
    return prefix + out.stdout

def ask(client, history, system):
    msg = client.messages.create(model=MODEL, max_tokens=4000, system=system, messages=history)
    raw = ''.join(b.text for b in msg.content if getattr(b, 'type', '') == 'text').strip()
    raw = raw.removeprefix('```json').removeprefix('```').removesuffix('```').strip()
    return raw

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('message'); ap.add_argument('--tag', default='')
    ap.add_argument('--out', default='turn.html'); a = ap.parse_args()
    import anthropic
    client = anthropic.Anthropic()
    system = system_prompt()
    user = (a.tag + ' ' if a.tag else '') + a.message
    history = [{'role': 'user', 'content': user}]
    for attempt in range(2):                       # one repair round, then give up loudly
        raw = ask(client, history, system)
        try:
            spec = json.loads(raw)
        except json.JSONDecodeError as ex:
            errs = ['response was not valid JSON: %s' % ex]
        else:
            errs, warns = diagnosis_html.validate(spec)
            if not errs:
                with open(a.out, 'w', encoding='utf-8') as f:
                    f.write(diagnosis_html.render_page(spec, 'canvas'))
                print(json.dumps(spec['chat'], indent=1, ensure_ascii=False))   # → app chat UI
                print('canvas →', a.out, '| warnings:', warns, file=sys.stderr)
                return
        history += [{'role': 'assistant', 'content': raw},
                    {'role': 'user', 'content': 'Your spec failed validation. Fix exactly these and resend the whole JSON object:\n- ' + '\n- '.join(errs)}]
    sys.exit('spec still invalid after repair: %s' % errs)

if __name__ == '__main__':
    main()
