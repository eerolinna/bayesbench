cat arguments.json | parallel python -m bayesbench.run --args {} --output_dir output
