from pipelayer.step import StepType

manifest_dict = {
    "name": "Pipeline",
    "step_type": StepType.PIPELINE,
    "start": 1611261876.182439,
    "end": 1611261880.49989,
    "duration": "P0DT0H0M4.317451S",
    "steps": [
        {
            "name": "FirstFilter",
            "step_type": StepType.FILTER,
            "start": 1611261880.498892,
            "end": 1611261880.498892,
            "duration": "P0DT0H0M0.000000S",
            "pre_process": None,
            "post_process": None
        },
        {
            "name": "second_filter",
            "step_type": StepType.FILTER,
            "start": 1611261880.498892,
            "end": 1611261880.498892,
            "duration": "P0DT0H0M0.000000S",
            "pre_process": None,
            "post_process": None
        },
        {
            "name": "[lambda data, context: json.dumps(data)]",
            "step_type": StepType.FILTER,
            "start": 1611261880.498892,
            "end": 1611261880.49989,
            "duration": "P0DT0H0M0.000998S",
            "pre_process": None,
            "post_process": None
        }
    ]
}
