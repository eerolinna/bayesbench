# Outline

This file shows several Stan models and the outputs from those models in both the current output format and the possible new output format that includes slots for prior, prior predictive, posterior predictive and datapoint likelihood outputs.

# Model 1 (Eight schools)

This model includes posterior, posterior predictive and datapoint likelihood outputs.

```stan
data {
    int<lower=0> J;
    real y[J];
    real<lower=0> sigma[J];
}

parameters {
    real mu;
    real<lower=0> tau;
    real theta_tilde[J];
}

transformed parameters {
    real theta[J];
    for (j in 1:J)
        theta[j] = mu + tau * theta_tilde[j];
}

model {
    mu ~ normal(0, 5);
    tau ~ cauchy(0, 5);
    theta_tilde ~ normal(0, 1);
    y ~ normal(theta, sigma);
}

generated quantities {
    vector[J] log_lik;
    vector[J] y_hat;
    for (j in 1:J) {
        log_lik[j] = normal_lpdf(y[j] | theta[j], sigma[j]);
        y_hat[j] = normal_rng(theta[j], sigma[j]);
    }
}
```

## Current output format

```json
{
    "mu": ["..."],
    "tau": ["..."],
    "theta_tilde": ["..."],
    "theta": ["..."],
    "y_hat": ["..."],
    "log_lik": ["..."],
}
```

## New
```json
{
    "posterior": {
        "mu": ["..."],
        "tau": ["..."],
        "theta_tilde": ["..."],
        "theta": ["..."]
    },
    "prior": null,
    "prior_predictive": null,
    "posterior_predictive": {
        "y": ["..."]
    },
    "log_likelihood": ["..."]
}
```

## Model info json

```json
{
    "posterior_predictive": [{"original": "y_hat", "rename": "y"}],
    "log_likelihood": "log_lik"
}
```

# Model 2 (Binomial model)

This model includes posterior, prior and prior predictive outputs.

```stan
data {
  int<lower = 1> N;
  real<lower = 0> a;
  real<lower = 0> b;
  int<lower = 0> y;
}
parameters {
  real<lower = 0, upper = 1> pi;
}
model {
  target += beta_lpdf(pi | a, b);
  target += binomial_lpmf(y | N, pi);
}
generated quantities {
  real pi_ = beta_rng(a, b);
  int y_ = binomial_rng(N, pi_);
}
```

## Current output format

```json
{
    "pi": ["..."],
    "y_": ["..."],
    "pi_": ["..."],
}
```


## New

```json
{
    "posterior": {
        "pi": ["..."]
    },
    "prior": {
        "pi": ["..."],
    },
    "prior_predictive": {
        "y": ["..."]
    },
    "posterior_predictive": null,
    "log_lik": null
}
```

## Model info json

```json
{
    "prior": [{
        "original": "pi_",
        "rename": "pi"
    }],
    "prior_predictive": [{
        "original": "y_",
        "rename": "y"
    }]
}
```

# Benefits of new output format

We can more easily compare for example only predictive distributions

With the new representation running SBC becomes easy. Pseudocode:
```python
for prior_draw, prior_predictive_draw in zip(prior, prior_predictive):
    # with model 2 this overwrites `y` from data with `y` from prior predictive draw
    new_data = merge(original_data, prior_predictive_draw)

    output = run(model, new_data)

    ranks = compute_ranks(output, prior_draw)
```

For PyMC the outputs are essentially already in the new format. If we want to follow the old format then we need to figure out how to convert PyMC to it (which will be difficult)


# Comments

For Stan we need extra information to be able to transform the Stan output to the new representation. Currently the information is provided in model info json files.

We could also make it so that if the model follows certain conventions then the json info file is not needed.

- If there is a variable named `log_lik` then it is the log likelihood.
- If a variable has a trailing underscore it is assumed to be a prior or prior predictive draw. If there is a corresponding parameter without the underscore then it is prior, else it is prior predictive.
- If a parameter has trailing `_hat` or `_pred` then it is a posterior predictive draw that is named by removing `_hat` or `_pred`.


One potential problem is that we regenerate prior and prior predictive draws each time we run inference for the model. If we want to avoid this then we'd need to have two Stan models: A generative model that generates prior and prior predictive draws and a normal model.

With model 2 the generative model would be

```stan
data {
  int<lower = 1> N;
  real<lower = 0> a;
  real<lower = 0> b;
}
generated quantities {
  real pi = beta_rng(a, b);
  int y = binomial_rng(N, pi);
}
```

And the normal model would be

```stan
data {
  int<lower = 1> N;
  real<lower = 0> a;
  real<lower = 0> b;
  int<lower = 0> y;
}
parameters {
  real<lower = 0, upper = 1> pi;
}
model {
  target += beta_lpdf(pi | a, b);
  target += binomial_lpmf(y | N, pi);
}
```

Both of these approaches feel deficient when I know that for example PyMC can generate prior and prior predictive samples using just the equivalent of the "normal" model, however out of these the separate generative and regular model approach feels cleaner.

We might also want to have two separate outputs: one for prior and prior predictive outputs, one for posterior, posterior predictive and log_likelihood outputs.
