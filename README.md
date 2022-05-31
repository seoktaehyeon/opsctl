# Ops CTL tool

[![Org](https://img.shields.io/static/v1?label=org&message=Truth%20%26%20Insurance%20Office&color=597ed9)](https://office.baoxian-sz.com)
![Author](https://img.shields.io/static/v1?label=author&message=v.stone@163.com&color=blue)
![License](https://img.shields.io/github/license/seoktaehyeon/opsctl)
[![python](https://img.shields.io/static/v1?label=Python&message=3.8&color=3776AB)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/opsctl.svg)](https://pypi.org/project/opsctl/)

### Install

```bash
pip install opsctl
```

### Upgrade

```bash
pip install opsctl --upgrade
```

#### Feature

```bash
Usage:
opsctl
  tmpl2art  Render templates to articles
  env2json  Get environ variables to json file 
  env2yaml  Get environ variables to yaml file
  version	Show opsctl version
```

- render yaml templates

```bash
Usage:
opsctl tmpl2art
  --config	Key-Value config file path, file type is YAML
  --tmpl	Template dir path or template file path
  --output	Articles output path
```

- get env and output to a json file
  
```bash
Usage:
opsctl env2json
  --output  Output Json file path
```

- get env and output to a yaml file

```bash
Usage:
opsctl env2yaml
  --output  Output YAML file path
```
