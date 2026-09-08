# tool_notes

Short, honest notes on nine visual, document and collaboration tools, with the one
worked file each note needs to make its point. When the tool is worth the
setup, when it is not, and what will go wrong.

These were nine top-level folders, each presented as a module. None of them
is: the tools live on their own sites, and what a repository can usefully hold
about them is a page of judgement plus a small example, which is what each
folder now contains. They are here together so nobody mistakes a
screenshot for a template again.

| Note | Tool | What is actually in the folder |
|---|---|---|
| [`excalidraw_frameworks/`](excalidraw_frameworks/) | Excalidraw | Two editable `.excalidraw` diagrams, a MEL results chain and a district ecosystem map, with PNG previews |
| [`kumu_maps/`](kumu_maps/) | Kumu | One stakeholder map of a district health network as Kumu JSON, with a preview |
| [`observable_notebooks/`](observable_notebooks/) | Observable | One `.ojs` notebook plotting district coverage, its CSV, and a screenshot |
| [`open_data_editor/`](open_data_editor/) | RawGraphs, Datawrapper, Open Data Editor | A district indicators CSV shaped for those tools, and one chart made from it |
| [`flourish_charts/`](flourish_charts/) | Flourish | The iframe embed snippet, and a screenshot of a chart |
| [`powerbi_reports/`](powerbi_reports/) | Power BI | An adaptation note. No `.pbix` ships; the note links to Microsoft's sample |
| [`miro/`](miro/) | Miro | A human-centred design session outline and links. No board ships |
| [`excel_visuals/`](excel_visuals/) | Excel | Three chart templates as `.xlsx`: bullet, waterfall, Gantt |
| [`latex/`](latex/) | LaTeX | A report skeleton that compiles with `pdflatex`, and where it is worth the learning curve |

## The one judgement that applies to all seven

Each of these tools is quicker than code for the first version and slower than
code for the tenth. A Flourish chart takes twenty minutes to make and twenty
minutes to remake when the data changes; a script takes two hours the first
time and two seconds thereafter. So the deciding question is how many times the
output will change. A one-off workshop artefact belongs in Miro or Excalidraw.
A quarterly indicator chart belongs in `ggplot2` or `matplotlib`, and this
repository's `stata_snippets/`, `econometrics/` and FieldStack's
`visualisation/` are where to start.

The second judgement is where the file lives. Everything in Kumu, Flourish,
Observable and Miro lives on their servers under their terms. A district health
network map with named officials is data about people, and it should not sit on
a third-party server without someone having decided that it can. Excalidraw and
RawGraphs run in the browser without an account and keep nothing, which is why
they are the two of the seven that this repository recommends without a caveat.
