"""Dummy GPU job: run nvidia-smi on each GPU in the cluster (one task per GPU)."""
import socket
import subprocess

import ray

ray.init()


@ray.remote(num_gpus=1)
def check_gpu():
    out = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    return f"{socket.gethostname()} -> {out}"


res = ray.cluster_resources()
n = int(res.get("GPU", 0))
print("cluster_resources:", res)
print(f"GPU_COUNT: {n}")
for line in ray.get([check_gpu.remote() for _ in range(max(n, 1))]):
    print("GPU_NODE:", line)
print("DONE")
