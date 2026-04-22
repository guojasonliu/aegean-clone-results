#!/usr/bin/env bash
set -euo pipefail

to_delete=()
while IFS= read -r -d '' path; do
	to_delete+=("$path")
done < <(
	find . -mindepth 1 \
		\( -path './.git' -o -path './.git/*' -o -name 'README.md' -o -name '*.py' -o -name '*.sh' \) -prune \
		-o -print0
)

if [ ${#to_delete[@]} -eq 0 ]; then
	echo "Nothing to delete."
	exit 0
fi

echo "The following will be removed:"
printf '  %q\n' "${to_delete[@]}"
echo

read -r -p "Proceed? [yes/no] " answer

case "$answer" in
	yes|y|Y|YES)
		rm -rf -- "${to_delete[@]}"
		echo "Deleted."
		;;
	*)
		echo "Aborted."
		;;
esac