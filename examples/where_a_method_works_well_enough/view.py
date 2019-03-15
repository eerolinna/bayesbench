import bayesbench

output_dir = "output"

knowledge_base = bayesbench.load_knowledge_base("kb_location")

outputs = bayesbench.load(output_dir=output_dir)


# Here we assume that we can automatically detect if a method works well enough. Is this true or is human judgement also required?
result = bayesbench.determine_adequacy(
    outputs,
    "stan_vi_fullrank",
    knowledge_base=knowledge_base,  # gold standards are found from knowledge base
    fallback_comparison="stan_nuts",  # used if there's no gold standard available
)

print(result["good_enough"])  # List of models where VI was good enough
print(result["not_good_enough"])  # List of models where VI wasn't good enough
