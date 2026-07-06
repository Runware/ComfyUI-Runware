# ComfyUI-Runware

Every Runware model as a ComfyUI node: image, video, audio, 3D, and text, all
running in the cloud. No local GPU and no per-model setup. The whole catalog
shows up in your node menu, and each node's widgets are the model's real parameters.

**Full guide: https://runware.ai/docs/platform/comfyui**

## Install

**ComfyUI Manager** (recommended): open the Custom Nodes Manager, search
**Runware**, install, and restart.

**Manual:**
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Runware/ComfyUI-Runware
pip install -r ComfyUI-Runware/requirements.txt
```
Restart ComfyUI.

## API key

Create a key in the [dashboard](https://runware.ai/api-keys), then provide it one of these ways:

- **ComfyUI Settings → Runware API key**: paste it in the UI, no terminal needed.
- **`RUNWARE_API_KEY`** environment variable: overrides the Settings field, useful for servers.
- **Runware CLI**: run `runware auth login` once and the nodes reuse the stored key.

## Quick start

1. Double-click the canvas and search a model by name (e.g. `FLUX.2 [dev]`), or browse `Runware/Image`.
2. Type your `positivePrompt` and set the dimensions.
3. Wire the node's **IMAGE** output into **Preview Image** or **Save Image**.
4. Queue. The request runs on Runware and comes back as a native `IMAGE`.

## What's in the pack

- **One node per model**, grouped `Runware/<Modality>/<creator>`. Widgets are the model's real parameters, with correct ranges, defaults, and dropdowns.
- **Native outputs**: image, upscale, and background-removal return `IMAGE`; audio returns `AUDIO`; video returns `VIDEO`; 3D and other files save to your output folder and return a path; text returns a string.
- **Native inputs**: reference and seed images are `IMAGE`, inpainting masks are `MASK`; audio, video, and document inputs take a URL, path, or UUID.
- **Builder nodes** (`Runware/Params`) keep model nodes clean. Stackable features (LoRA, ControlNet, IP-Adapter, Embeddings, and more) each wire into a model's typed socket, and you chain the stackable ones to combine them.
- **Custom checkpoints**: `Runware/Custom models` has a node per architecture (SDXL, SD 1.5, FLUX, Pony, and more) for community fine-tunes.
- **New models, day one**: `Runware (custom)` takes any model AIR and `taskType` as JSON and returns raw JSON. Pair it with `Runware Get` to pull a field out of the response (e.g. `0.imageURL`).
- **Run info** on the title bar: each run shows its cost and, when a content check ran, the NSFW result (e.g. `$0.00078 · NSFW: no`).

The [full guide](https://runware.ai/docs/platform/comfyui) covers every builder, custom models, parameter behavior, and troubleshooting.

## Links

- [Documentation](https://runware.ai/docs/platform/comfyui)
- [Discord](https://discord.gg/aJ4UzvBqNU)
