# nmt3325 Repository (Cydia)

脱獄 iOS 向けの Cydia / APT リポジトリ。

**ソース URL:** `https://nmt3325.github.io/cydia/`

Cydia → ソース → 編集 → 追加 で上記 URL を入力。

## Packages
| Package | Version | 説明 |
|---|---|---|
| [icli6](https://github.com/nmt3325/icli6) (`dev.owngoal.icli6`) | 0.11.0-ios6.1 | iOS 6 (armv7) 向け [icli](https://github.com/owngoal-dev/icli) 。ターミナルから端末操作（OCR なし） |

## パッケージの追加・更新
```
cp foo.deb docs/debs/
python3 tools/update.py   # Packages / Packages.gz / Packages.bz2 / Release を再生成
git add -A && git commit -m 'update' && git push
```
不要になった古いバージョンの .deb は `docs/debs/` から削除してから `update.py` を実行。

GitHub Pages: `main` ブランチの `/docs` を公開。
 EOF
sed -i '' 's/^ EOF$//' README.md; cat > .gitignore <<'EOF'
.DS_Store
