# ComfyUI-Runware

Every Runware model as a ComfyUI node: image, video, audio, 3D, and text. The
whole catalog stays current as new models launch, and each node's parameters
match the live model exactly.

## Install

**ComfyUI Manager** (recommended): search **Runware** and install.

**Manual:**
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Runware/ComfyUI-Runware
pip install -r ComfyUI-Runware/requirements.txt
```
Restart ComfyUI.

## API key

Use any of these (the environment variable wins if more than one is set):

- **ComfyUI Settings → Runware API key**: paste your key in the UI, no terminal needed.
- **`RUNWARE_API_KEY`** in the environment ComfyUI runs in.
- **[Runware CLI](https://runware.ai/docs/platform/cli)**: run `runware auth login`
  once and the nodes reuse the stored key.

## Use

Search the node menu for **Runware**. One node per model, grouped
`Runware/<Modality>/<creator>`. Set the parameters, wire the output, and queue:

- **Image** models output a native ComfyUI IMAGE.
- **Audio / video** models output native ComfyUI AUDIO / VIDEO (chain them straight
  into preview or save nodes); **3D** and other files download to your output folder
  and return a path.
- **Reference / seed images** are IMAGE inputs and **inpainting masks** are MASK
  inputs; audio/video inputs take a URL or path.
- **Builder nodes keep model nodes clean** (`Runware/Params`). Stackable features
  live in their own nodes instead of crowding every model node: `LoRA`, `ControlNet`,
  `IP-Adapter`, `Embeddings`, `Refiner`, feature blocks (`PuLID`, `PhotoMaker`,
  `Watermark`, `Ultralytics`, `Accelerator Options`), and reference inputs. Each feature
  is a distinct socket type, so you wire a builder into the model's matching typed socket
  (`lora`, `controlNet`, ...) and chain the stackable ones to combine them. The model node
  only shows the features a generation actually uses.
- **Builders scope themselves to the model they wire into.** LoRA, Embeddings, and Refiner
  have an editable **model** field plus a **search catalog** button that opens a live
  catalog search to fill the AIR. ControlNet and IP-Adapter instead scope their **model**
  field to the model/architecture node they reach (through any builders in between): it
  becomes a dropdown of exactly the models that node accepts, or a free AIR field until it
  reaches one. The Speech, reference, Accelerator Options, and Outpaint builders scope
  their **fields** the same way: each shows only what that model supports and hides the
  rest (Speech's `voice`/`language` become that model's own lists, Accelerator Options
  shows only its caching strategies, Outpaint drops `blur` where unsupported).
- **Model-specific config flattens onto the model node** as dotted fields under a
  **Settings** section: `safety.checkContent`, `providerSettings.google.webSearch`
  (only your model's provider is shown).
- **Widgets are grouped into sections** (inputs, core, settings, output). Where a model
  has no fixed default for a setting, the node leaves it to the model rather than guess:
  a number like `steps` or `CFGScale` shows a **set** toggle that reveals its field only
  when you opt in, and a dropdown like `scheduler` carries a `(default)` option. Leave
  these to use the model's own default, or set them to take control. Dimensions and
  `seed` always show a value. A cohesive settings group reveals behind one toggle too:
  `safety`, `toolChoice`, and `advancedFeatures` each hide their fields (e.g.
  `safety.checkContent` / `safety.mode`) until you enable the group.
- Niche per-model params (and anything not auto-typed) go into the raw
  `advanced_json` input.
- **Runware Upload Image** / **Runware Load Image (URL)**: upload an image once for
  a reusable UUID, or pull any image URL (including a Runware result) into the graph
  as an IMAGE.
- After a run, each model, architecture, and custom node shows its cost and, when the
  model ran a content check, the NSFW result along its title bar (e.g. `$0.00078  ·  NSFW: no`).
- **Runware (custom)**: a generic node for any model AIR + taskType, for models
  newer than your installed version. It makes no assumption about modality: you give
  it the request as JSON (`request_json`) and it returns the raw response as
  `result_json`. Feed media in as UUIDs/URLs (see **Runware Upload Image**).
- **Runware Get**: pulls a field out of a `result_json` by dot-path (e.g.
  `0.imageURL`, `0.videoURL`, `0.outputs.files.0.url`; leave it empty to grab the
  first URL). The `STRING` it outputs goes to **Runware Load Image (URL)** to preview
  an image, or to a Save/Preview node for any other result.

Browse models and get an API key at [runware.ai](https://runware.ai/docs).
