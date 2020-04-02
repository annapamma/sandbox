#!/bin/bash
set -eo pipefail

paths=("mytest.groovy")

echo $paths \
| awk '{
for(i = 1; i <= NF; i++) {
test = gsub(/\.java|\.groovy/,"");
n = split($test, a, "/")
print "--tests \*" a[n]
}
}'
