import asyncio
from .utils import runwareUtils as rwUtils
from comfy_execution.graph import ExecutionBlocker


class multiInference:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Task 1": (
                    "RUNWARETASK",
                    {
                        "tooltip": "Connect a Runware Task From Any Inference Node.",
                    },
                ),
            },
            "optional": {
                "Task 2": (
                    "RUNWARETASK",
                    {
                        "tooltip": "Connect a Runware Task From Any Inference Node.",
                    },
                ),
                "Task 3": (
                    "RUNWARETASK",
                    {
                        "tooltip": "Connect a Runware Task From Any Inference Node.",
                    },
                ),
                "Task 4": (
                    "RUNWARETASK",
                    {
                        "tooltip": "Connect a Runware Task From Any Inference Node.",
                    },
                ),
            },
        }

    DESCRIPTION = "Allows you to Run Multiple Inference Tasks in Parallel."
    FUNCTION = "multiInference"
    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = ("Result 1", "Result 2", "Result 3", "Result 4")
    CATEGORY = "Runware"

    def multiInference(self, **kwargs):
        tasksData = [kwargs.get(f"Task {i}", None) for i in range(1, 5)]
        validTasks = [task for task in tasksData if task is not None]

        if not validTasks:
            raise Exception("Error: No valid tasks provided for Multi Inference!")

        taskIncidents = {}

        async def runInference(taskData, taskIndex, oindex):
            try:
                print(f"[Debugging] Task {oindex + 1} UUID => {taskData[0]['taskUUID']}")
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(
                    None, rwUtils.inferenecRequest, taskData
                )
                images = rwUtils.convertImageB64List(result)
                return images
            except Exception as e:
                print(f"\n---- Runware Multi Inference Task {oindex + 1} Failed ----")
                print(f"Task-Type: {taskData[0]['taskType']}")
                print(f"Task-UUID: {taskData[0]['taskUUID']}")
                print(f"{e}")
                print(f"-------------------\n")
                taskIncidents[taskIndex] = e
                return ExecutionBlocker(None)

        async def main():
            coroutines = []
            valid_indices = [idx for idx, t in enumerate(tasksData) if t is not None]
            for i, config in enumerate(validTasks):
                original_index = valid_indices[i]
                coroutines.append(runInference(config, i, original_index))
            results = await asyncio.gather(*coroutines, return_exceptions=False)
            return results

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        finalResults = loop.run_until_complete(main())

        optResult = [ExecutionBlocker(None)] * 4
        rindex = 0
        workingTasks = 0

        for i, task_config in enumerate(tasksData):
            if task_config is not None:
                result = finalResults[rindex]
                if result is not None and not isinstance(result, ExecutionBlocker):
                    workingTasks += 1
                optResult[i] = result
                rindex += 1

        if workingTasks == 0 and len(validTasks) > 0:
            firstError = min(taskIncidents.keys())
            raise Exception(
                f"Error in Task {firstError + 1} => {taskIncidents[firstError]}"
            )

        return tuple(optResult)
