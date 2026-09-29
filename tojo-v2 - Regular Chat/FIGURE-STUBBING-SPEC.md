# Tojo v2 — Figure Stubbing

The single largest saving in the package, and the one with no trade-off.

## 1. The problem

Every figure Tojo has already sent is re-sent, in full, on every subsequent turn,
for the rest of the conversation. At turn 15 of a bed-management session that is
25,200 tokens of old drawings — more than a quarter of the whole request. By turn
31 it is over 55,000.

The model does not need the SVG source of a picture it drew eleven turns ago. It
needs to know that the picture exists, what it showed, and how to refer back to
it. That is one line.

## 2. The stub

Full SVG stays in the transcript and the database, where the user's client
renders it. What goes into the model's context is:

```
[fig 26 · derivation-chain · dead bed time · wide]
```

Four fields, in this order, pipe-free and bracketed so it cannot be confused with
content:

| Field | What it carries | Why it is there |
|---|---|---|
| `fig <n>` | The figure's number in this conversation | So a later turn can name it — "as figure 26 showed" |
| `<form>` | The template it was built from, or `freehand` | So the model knows what shape the reader already has, and does not redraw the same shape for the same content |
| `<subject>` | Three to six words naming what it showed | The only part that carries meaning |
| `<ratio>` | `wide` or `tall` | Both files of a turn stub to one line, with both ratios named if they differ |

25,200 tokens become 420. The turn's own newly generated figures are never
stubbed — only figures from prior turns.

## 3. What the model can still do with a stub

**Refer back to it.** "The derivation in figure 26" is a legitimate reference and
the reader can see it.

**Avoid repeating it.** The no-replay rule and the don't-restate-the-graphic rule
both need to know what has already been shown. The stub carries exactly that.

**Build the progress view.** When someone asks what is left, the answer is drawn
from which parts have been covered — which the stub list records, in order.

**What it cannot do is re-read the drawing.** That is deliberate. If a turn
genuinely needs the values inside an earlier figure, those values came from the
hospital record or from a retrieved chunk, and both are still in context. A turn
that can only be answered by re-reading an old SVG is a turn whose numbers were
never recorded properly.

## 4. Rehydration

One case needs the full source back: the user asks for an earlier figure to be
**revised** rather than referred to — "can you redo figure 26 with the corrected
occupancy".

The backend rehydrates on an explicit signal, not on the model's guess:

1. The turn names a figure number and asks for a change to it.
2. The backend fetches that figure's **build call** — the form name and its slot
   values — not its rendered SVG.
3. The model edits the slots and the renderer rebuilds.

Fetching the build call rather than the SVG is what makes this cheap: the slots
of a derivation chain are a few hundred bytes, and the model never has to parse
its own past output back into meaning. For a freehand figure there is no build
call, so the SVG source is fetched — one more reason the escape rate is worth
measuring.

**Never rebuild from a delivered file.** A file that has already been sent
carries provenance metadata that can outweigh the drawing itself and makes every
size check meaningless. Keep the build call; regenerate from it.

## 5. The two-state exception

A fill-in-the-blank figure and its answered redraw are the same picture twice.
When the answers arrive, the redraw needs the blank's **geometry** — canvas size
and type scale — or the two will not share coordinates and the visual continuity
that is the entire point of the form is lost.

So a fill-in-the-blank figure's stub carries its geometry:

```
[fig 12 · fill-in-the-blank · four discharge timestamps · wide 880x528 base13]
```

That is the one case where a stub carries more than four fields, and it carries
the smallest thing that works: three numbers, not a drawing.

## 6. What this costs

Nothing measurable. There is no answer quality that depends on the model
re-reading its own past SVG source, and the one case that looked like an
exception — revising an earlier figure — is better served by the build call than
by the rendered file.

It is the cheapest item in the package: about a day of backend work for roughly
a quarter of the input tokens on a long conversation, and the saving grows with
conversation length, which is exactly where the cost was worst.

## 7. Instrumentation

Log per turn: figures stubbed, tokens saved, rehydrations requested, and whether
each rehydration used a build call or fell back to SVG source. The last of those
is the freehand escape rate seen from the other end, and it is the number that
says which form to build next.
