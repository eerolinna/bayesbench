import bayesbench

output_dir = "output"

knowledge_base = bayesbench.load_knowledge_base("kb_location")

outputs = bayesbench.load(output_dir=output_dir)

# Then do something with the results

# This could also just be a command line call
# python -m bayesbench.load --output_dir output_dir --knowledge_db kb_location
# This would load the results and drop you in a console
