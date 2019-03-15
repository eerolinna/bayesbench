import bayesbench
import json

knowledge_base = bayesbench.load_knowledge_base("kb_location")

new_kb = bayesbench.filter_knowledge_base(
    knowledge_base, methods=["stan_vi_fullrank", "stan_nuts"]
)  # TODO right now gold standards are implicit,

bayesbench.generate_arguments_file("arguments.json", knowledge_db=new_kb)
