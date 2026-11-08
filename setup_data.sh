#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

SRC="data/gitlab-handbook"
if [ ! -d "$SRC" ]; then
  mkdir -p data
  git clone --depth 1 https://gitlab.com/gitlab-com/content-sites/handbook.git "$SRC"
fi

rm -rf data/corpus
mkdir -p data/corpus
for d in people-group people-policies total-rewards hiring communication leadership finance legal; do
  cp -R "$SRC/content/handbook/$d" "data/corpus/$d"
done

rm -rf data/corpus/legal/legacy data/corpus/legal/subscription-agreement
rm -f data/corpus/legal/reseller-agreement.md data/corpus/legal/esg/fy23-esg-report.md
find data/corpus -type d -name readmes -exec rm -rf {} + 2>/dev/null || true

echo "Corpus tayyar: $(find data/corpus -name '*.md' | wc -l | tr -d ' ') markdown files"
