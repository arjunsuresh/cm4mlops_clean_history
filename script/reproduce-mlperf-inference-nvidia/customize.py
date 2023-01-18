from cmind import utils
import os
import shutil

def preprocess(i):

    os_info = i['os_info']

    if os_info['platform'] == 'windows':
        return {'return':1, 'error': 'Windows is not supported in this script yet'}
    env = i['env']

    if 'CM_MODEL' not in env:
        return {'return': 1, 'error': 'Please select a variation specifying the model to run'}
    if 'CM_MLPERF_DEVICE' not in env:
        return {'return': 1, 'error': 'Please select a variation specifying the device to run on'}

    cmds = []

    if env['CM_MODEL'] == "resnet50":
        target_data_path = os.path.join(env['MLPERF_SCRATCH_PATH'], 'data', 'imagenet')
        if not os.path.exists(target_data_path):
            cmds.append(f"ln -s {env['CM_DATASET_IMAGENET_PATH']} {target_data_path}")

        model_path = os.path.join(env['MLPERF_SCRATCH_PATH'], 'models', 'ResNet50', 'resnet50_v1.onnx')
        if not os.path.exists(model_path):
            cmds.append("make download_model BENCHMARKS='resnet50'")
        cmds.append("make preprocess_data BENCHMARKS='resnet50'")
        scenario=env['CM_MLPERF_LOADGEN_SCENARIO'].lower()
        if env['CM_MLPERF_LOADGEN_MODE'] == "accuracy":
            test_mode = "AccuracyOnly"
        elif env['CM_MLPERF_LOADGEN_MODE'] == "performance":
            test_mode = "PerformanceOnly"
        cmds.append(f"make run RUN_ARGS=' --benchmarks=resnet50 --scenarios={scenario} --test_mode={test_mode}'")

    env['RUN_CMD'] = " && ".join(cmds)
#    print(env)

    return {'return':0}

def postprocess(i):

    env = i['env']
    return {'return':0}