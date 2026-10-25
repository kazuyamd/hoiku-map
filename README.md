# 横浜 保育園空きマップ

公開ページ: https://kazuyamd.github.io/hoiku-map/

横浜市「保育所等の入所状況」の受入可能数・入所待ち人数を、年齢と距離で絞り込んで地図で見るページです。
毎月1〜3日の10:07（日本時間）にGitHub Actionsが市の最新CSVを取得し、`data.json` を自動更新します。

- `index.html` … 地図ページ（最初の基準地点は `const HOME=` の行。現在はJR関内駅）
- `data.json` … 表示データ（自動更新）
- `update.py` … 更新スクリプト（`python3 update.py geo.json data.json`）
- `geo.json` … 施設番号ごとの位置キャッシュ。新設の施設は `data.json` の `unlocated` に出るので、ここに追記すると地図に出ます
- `.github/workflows/update.yml` … 毎月の自動実行

データ出典：横浜市 保育所等の入所状況 / 地図：© OpenStreetMap contributors、国土地理院
