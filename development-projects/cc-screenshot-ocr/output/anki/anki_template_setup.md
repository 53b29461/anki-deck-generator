
# CC練習問題用Ankiノートタイプ設定

## フィールド構成:
1. 問題文
2. 選択肢A
3. 選択肢B
4. 選択肢C
5. 選択肢D
6. 正解
7. 解説
8. Text (クローズ用)
9. タグ
10. ファイル名

## 表面テンプレート:
```html
<div style="text-align: left; font-size: 16px; line-height: 1.5;">
  <b>【CC練習問題】</b><br><br>
  {{問題文}}
</div>

<hr style="margin: 20px 0;">

<div style="text-align: left; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
  <b>選択肢:</b><br><br>
  <div style="margin: 8px 0;"><b>A:</b> {{選択肢A}}</div>
  <div style="margin: 8px 0;"><b>B:</b> {{選択肢B}}</div>
  <div style="margin: 8px 0;"><b>C:</b> {{選択肢C}}</div>
  <div style="margin: 8px 0;"><b>D:</b> {{選択肢D}}</div>
</div>

<hr style="margin: 20px 0;">

<div style="text-align: center; font-size: 18px;">
  <b>正解:</b> {{cloze:Text}}
</div>
```

## 裏面テンプレート:
```html
{{FrontSide}}

<hr style="margin: 20px 0; border-color: #007bff;">

<div style="text-align: left; background-color: #e8f4fd; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff;">
  <b style="color: #007bff;">【正解】</b><br>
  <b style="color: #28a745; font-size: 18px;">{{正解}}</b>
</div>

{{#解説}}
<div style="text-align: left; background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin-top: 15px;">
  <b style="color: #856404;">【解説】</b><br>
  {{解説}}
</div>
{{/解説}}

<div style="text-align: right; font-size: 12px; color: #6c757d; margin-top: 15px;">
  {{ファイル名}}
</div>
```

## CSS (スタイル):
```css
.card {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.cloze {
  font-weight: bold;
  color: #dc3545;
  background-color: #f8d7da;
  padding: 2px 6px;
  border-radius: 3px;
}
```
