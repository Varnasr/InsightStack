# Kumu

One stakeholder map of a district health delivery network, as Kumu-importable
JSON, with a rendered preview.

| File | What it is |
|---|---|
| `district_health_network.json` | Elements (PHC, CHWs, ASHA supervisor, block officer, pregnant women as a group) and the connections between them, in the `elements` / `connections` shape Kumu imports |
| `district_health_network.png` | The rendered map |

Import at kumu.io: create a project, then Import, then choose the JSON. Kumu
lays it out; you adjust.

## When to use it

Stakeholder and influence mapping where the point is the *structure* of a
system rather than any number in it, and where the map will be presented and
talked through rather than analysed. Power and interest analysis, supervision chains,
who-talks-to-whom in a district health system.

## When not to

Anything where you need a network *statistic*. Kumu will show centrality as
node size but will not give you the number in a form you can put in a table or
compare across districts. For that, the data goes into `networkx` (see
`../../network_effects_sni/`) or R's `igraph`, and Kumu is at most the
presentation layer at the end.

## What goes wrong

**Named people on a third-party server.** A map of a district health system
with the block medical officer's name on it is personal data and it sits on
Kumu's servers under Kumu's terms. Free projects are public by default. Use
roles rather than names, or use a private project and decide who is allowed to
see it, before importing anything real.

**The JSON is easy to hand-write and easy to get subtly wrong.** A connection
whose `from` or `to` names an element that does not exist is silently dropped
on import, and the map looks fine with an edge missing. Generate the JSON from
a spreadsheet rather than typing it, and count the connections after import.
