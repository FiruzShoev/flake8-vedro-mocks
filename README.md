# flake8-vedro-mocks
Flake8 based linter for [Vedro](https://vedro.io/) framework and mocks

## Installation

```bash
pip install flake8-vedro
```

## Configuration
Flake8-vedro is flake8 plugin, so the configuration is the same as [flake8 configuration](https://flake8.pycqa.org/en/latest/user/configuration.html).

You can ignore rules via
- file `setup.cfg`: parameter `ignore`
```editorconfig
[flake8]
ignore = MCS001
```
- comment in code `#noqa: MCS001`

Some rules in linter should be configured:
```editorconfig
[flake8]
mock_name_pattern = (?=.*mock)(?!.*grpc)  # MCS001, # MCS002 
```

## Rules

###  Scenario Steps Rules
1. [MCS001. Mock call result should be saved as "self" attribute for further assertion](./flake8_vedro/rules/MCS001.md)
2. [MCS002. Mock call result should be asserted in "then" or "and" or "but" step](./flake8_vedro/rules/MCS002.md)
