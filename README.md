# plot-montage
vhdrやチャネル名を指定して，モンタージュの画像作成．

# Requirements
- python
- pillow
- pandas
- numpy
- mne (vhdrから読む場合)

# 使い方
下記のようにすると，`vhdr`ファイルからチャネルを読み込み，`vEOG`と`hEOG`チャネルを無視した脳波チャネルのモンタージュ画像を`ホームフォルダ/Documents/montage.png`として保存します．
```shell
python main.py --vhdr PATH_TO_VHDR_FILE --eog vEOG hEOG --fontsize 125 --radius_ch 150 --file ~/Documents/montage.png
```