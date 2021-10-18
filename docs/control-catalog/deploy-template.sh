jq -rc '.catalog.groups[] | [.id, .title]' ../_data/tamus_catalog.json |
while IFS= read -r line; do
  family_code=$(echo "$line" | jq -rc '.[0]')
  family_title=$(echo "$line" | jq -rc '.[1]')

  cp family.template $family_code.html
  sed -i '' "s/---REPLACE TITLE---/$family_title/g" $family_code.html
done
