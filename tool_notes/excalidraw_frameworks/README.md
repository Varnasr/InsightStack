# Excalidraw

Two editable diagrams and their previews. Open a `.excalidraw` file at
[excalidraw.com](https://excalidraw.com) (File, Open) or in the VS Code
extension; nothing is uploaded unless you choose to share.

| File | What it shows |
|---|---|
| `mel_framework.excalidraw` | A results chain: inputs, activities, outputs, outcomes, with the assumptions between each pair drawn as labelled links rather than left implicit |
| `ecosystem_map.excalidraw` | A district health delivery map: PHC, CHWs, block officer, ASHA supervisors, and who reports to whom |
| `*.png` | Previews, for a README or a slide when nobody needs to edit |

## When to use it

A workshop, where the diagram is being built in the room and the hand-drawn
look tells participants it is still a draft and they are allowed to move the
boxes. A theory of change at the stage where the causal claims are still being
argued about. Anything that will be redrawn three times in an afternoon.

## When not to

Anything that will be regenerated from data. A results chain whose boxes carry
indicator values is a chart, and it should be a chart, so the numbers update
when the data does. And anything going to a donor as a final document: export
to SVG and place it in the document rather than sending a screenshot, which
prints badly.

## What goes wrong

The hand-drawn font (Virgil) is not installed on the reader's machine, so a
PNG export looks right and an SVG opened elsewhere may not. Export PNG for
sharing, keep the `.excalidraw` for editing. And a file with a hundred elements
becomes slow to open in the browser; split a large ecosystem map by block.
