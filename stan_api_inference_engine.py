# Currently this function name must be `inference`
def inference(model, data, diagnostics, seed, extra_fitting_args):
    """Here the model is stan API for model so we can access log likelihood and its gradients and the parameterization of the model

    Right now this takes multiple arguments but we can also have it take one argument (`config`) that contains everything needed

    TODO: this should fill default values with explicit values. Thus this should return not only the inference result but also the explicit fitting_args used
    """
    pass


def validate_args(args):
    # We can use something like JSON schema for validating these

    # This could probably be optional, at least for user-defined custom inference methods. If the user doesn't include validation function then the inputs just won't be validated beforehand.
    pass
