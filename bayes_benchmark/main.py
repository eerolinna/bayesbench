def enumerate_possibilities(knowledge_base):
    """
    Iterate over models
    Iterate over datasets for that model
    Iterate over methods (check if a method should be skipped for this model and data)
    Yield (model, dataset, method)

    Might also want to yield applicable diagnostics, or possibly those could be determined from the knowledge database at use site

    Have also a function that prints the iterated results to file. Then this file can be used for creating cluster runs: one run per (model, dataset, method)
    """
    pass

