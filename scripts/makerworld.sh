#!/bin/zsh
# MakerWorld sem Cloudflare: metadados pela API pública, download pelo Safari já logado.
# uso: makerworld.sh info <designId>             -> lista perfis (instanceId | título | impressora | min | g)
#      makerworld.sh get  <instanceId> <saida.3mf>
# designId = número na URL /models/<designId>-...; o #profileId da URL costuma ser o próprio instanceId
# (confira na primeira coluna do `info`).
set -e
case $1 in
info)
  curl -s https://api.bambulab.com/v1/design-service/design/$2 | python3 -c '
import json,sys; d=json.load(sys.stdin); print(d.get("title"), "| licença:", d.get("license"))
for i in d.get("instances",[]):
    c=(i.get("extention") or {}).get("modelInfo",{}).get("compatibility",{})
    print(i["id"],"| profileId",i.get("profileId"),"|",i.get("title"),"|",c.get("devProductName"),"|",round((i.get("prediction") or 0)/60),"min |",i.get("weight"),"g")'
  ;;
get)
  json=$(osascript <<OSA
tell application "Safari"
  make new document with properties {URL:"https://makerworld.com/api/v1/design-service/instance/$2/f3mf?type=download"}
  delay 6
  set r to do JavaScript "document.body.innerText" in current tab of front window
  close front window
  return r
end tell
OSA
)
  url=$(echo "$json" | python3 -c 'import json,sys;print(json.load(sys.stdin)["url"])') || { echo "sem url (logado no Safari?): $json"; exit 1; }
  mkdir -p ${3:h}; curl -s -o $3 "$url"; ls -la $3
  ;;
esac
