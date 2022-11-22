#!/bin/sh

echo "Star to init README"
cat <<EOF > README.md
# Ops CTL tool
*Generated by script*

[![Org](https://img.shields.io/static/v1?label=org&message=Truth%20%26%20Insurance%20Office&color=597ed9)](https://office.baoxian-sz.com)
![Author](https://img.shields.io/static/v1?label=author&message=v.stone@163.com&color=blue)
![License](https://img.shields.io/github/license/seoktaehyeon/opsctl)
[![python](https://img.shields.io/static/v1?label=Python&message=3.8&color=3776AB)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/opsctl.svg)](https://pypi.org/project/opsctl/)

### Install

\`\`\`bash
pip install opsctl
\`\`\`

### Upgrade

\`\`\`bash
pip install opsctl --upgrade
\`\`\`

### Test

\`\`\`bash
python setup.py install
cd test
pytest *
\`\`\`

EOF

echo "Complete to init"

echo "Update feature list"

output_feature=$(opsctl)
cat <<EOF_FEATURE >> README.md
### Feature

\`\`\`text
$output_feature
\`\`\`

EOF_FEATURE

echo "Complete to update"

cmd_list=$(echo "${output_feature}" | awk '{print $1}')
for cmd in $cmd_list
do
    if [ "$cmd" == "opsctl" ]; then
        continue
    elif [ "$cmd" == "version" ]; then
        continue
    fi
    echo "Update feature description for $cmd"
    cat << EOF >> README.md
- $(echo "$output_feature" | grep "^  $cmd" | awk -F "^  $cmd" '{print $NF}')

\`\`\`text
$(opsctl $cmd)
\`\`\`

EOF
    echo "Complete to update for $cmd"
done

echo "  "
echo "Complete README"