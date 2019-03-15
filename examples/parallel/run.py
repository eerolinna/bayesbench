import bayesbench

args, output_dir = bayesbench.load_command_line_args()

bayesbench.run(knowledge_db="kb_location", output_dir=output_dir, **args)

# This file could be replaced with a command line call, something like
# python -m bayesbench.run --args args_in_json --output_dir output
