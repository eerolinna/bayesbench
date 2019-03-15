import bayesbench
import json

bayesbench.generate_arguments_file("arguments.json", knowledge_db="kb_location")

# alternatively this could just be a command line call
# python -m bayesbench.generate_arguments_file arguments.txt --knowledge_db kb_location
