# Simple 8 schools example

Run with

```bash
python -m bayesbench.iterate_yaml config.yaml | parallel python -m bayesbench.run --args {} --output-dir out --posterior-db posterior_db_location
```

Yaml config was generated with gen_yaml.py