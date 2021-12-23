from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

#APIキーの情報
key = "4f80f1a6320f0ce2a711f3c65051b70f"
secret = "7096be15d14916db"
wait_time = 1

#保存フォルダの指定
animalname = sys.argv[1]
savedir = "./" + animalname

flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    #検索ワード
    text = animalname,
    #何件取得するか
    per_page = 400,
    #検索するデータの種類
    media = 'photos',
    #関連順に並べる
    sort = 'relevance',
    #UIコンテンツは表示しない
    safe_serch = 1,
    #取得したいオプション値、URLとライセンス情報取得
    extras = 'url_q, licence'
)

#結果の表示
photos = result['photos']
# pprint(photos)

for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    # 同じ名前のファイルがあれば飛ばす
    if os.path.exists(filepath): continue
    # ダウンロードして保存
    urlretrieve(url_q, filepath)
    time.sleep(wait_time)
