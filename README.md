# tagordo

[![PyPI](https://img.shields.io/pypi/v/tagordo)](https://pypi.org/project/tagordo/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tagordo)
[![PyPI - License](https://img.shields.io/pypi/l/tagordo)](https://github.com/mathiazom/tagordo/blob/main/LICENSE)

Tiny python script to check if given checkpoints are up-to-date with a given cron schedule

## `tagordo`

Check if checkpoints in CHECKPOINTS_DIR are up-to-date with a given CRON_EXPRESSION schedule.

**Usage**:

```console
$ tagordo [OPTIONS] CRON_EXPRESSION CHECKPOINTS_DIR
```

**Arguments**:

* `CRON_EXPRESSION`: [required]
* `CHECKPOINTS_DIR`: [required]

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
