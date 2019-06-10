# Run by loading a config file
import bayesbench

outputs = bayesbench.run.run_many(config="config.yaml")

result = bayesbench.benchmark(outputs)

print(result)
