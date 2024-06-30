from django import forms  # ModelFormもこれでいける
from .models import (
    Registered_english_words, 
)
import random
import re


# 英単語登録フォーム
class VocabularyRegistForm(forms.ModelForm):
    example_sentence = forms.CharField(label='例文',  widget=forms.Textarea)
    meaning_of_example_sentence = forms.CharField(label='例文の意味',  widget=forms.Textarea)

    class Meta:
        model = Registered_english_words
        exclude = ['create_at', 'update_at', 'user_id']
        labels = {
            'english_word': '英単語',
            'meaning_word': '意味',
        }


    def clean_english_word(self):
        english_word = self.cleaned_data.get('english_word')
        if not re.match(r'^[a-zA-Z]+$', english_word):
            raise forms.ValidationError('英単語はアルファベットのみ入力できます。')
        return english_word
        


# 英単語編集フォーム
class VocabularyUpdateForm(forms.ModelForm):
    example_sentence = forms.CharField(label='例文',  widget=forms.Textarea)
    meaning_of_example_sentence = forms.CharField(label='例文の意味',  widget=forms.Textarea)

    class Meta:
        model = Registered_english_words
        exclude = ['create_at', 'update_at', 'user_id']
        labels = {
            'english_word': '英単語',
            'meaning_word': '意味',
        }
        
    def clean_english_word(self):
        english_word = self.cleaned_data.get('english_word')
        if not re.match(r'^[a-zA-Z]+$', english_word):
            raise forms.ValidationError('英単語はアルファベットのみ入力できます。')
        return english_word



# クイズの選択肢
class PloblemForm(forms.Form):
    meaning_word = forms.ChoiceField(label="意味を選んでください", widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):  
        word = kwargs.pop('word', None)  
        choices = kwargs.pop('choices', None)
        user = kwargs.pop('user', None)
        super(PloblemForm, self).__init__(*args, **kwargs) 

        if choices:  # フォームのバインドを適切に行い、ユーザーの選択を正しく検証するためのコードだから、ちゃんと定義しとかないとダメなんだって（ほんとかな）
            self.fields['meaning_word'].choices = choices
        else:
            if user:
                all_meanings = list(Registered_english_words.objects.filter(user_id=user).values_list('meaning_word', flat=True).distinct())
                random.shuffle(all_meanings)
                selected_meanings = set()  # 既に選択された意味を保持するセット。セットを使うことで、重複する意味を防ぎます。

                if word and not self.is_bound:   # フォームが空（未バインド）で初期化される状態。= GETメソッド
                    # ランダムに2つの意味を選択
                    self.fields['meaning_word'].choices = []  # 空のリストでいまは選択肢に何も選ばれてません状態を宣言
                    for meaning in all_meanings:
                        if len(self.fields['meaning_word'].choices) < 2:  # リストが２つ要素を持つまでforループを回す。
                            self.fields['meaning_word'].choices.append((meaning, meaning))
                            selected_meanings.add(meaning)
                        else:
                            break   
                             
                    # 正しい意味を選択肢に追加
                    if word.meaning_word not in selected_meanings:  # 正しい意味(word.meaning_word)がselected_meaningsに含まれていない場合、Trueを返す。
                        self.fields['meaning_word'].choices.append((word.meaning_word, word.meaning_word))  # 正しい意味を追加
                        selected_meanings.add(word.meaning_word)  # 正しい意味を追加        
                        
                    # 選択肢の数を3つに調整
                    while len(self.fields['meaning_word'].choices) < 3:
                        for meaning in all_meanings:
                            if meaning not in selected_meanings:  # selected_meaningsに無いmeaningをall_meaningsから取り出す
                                self.fields['meaning_word'].choices.append((meaning, meaning))  # リストに追加する
                                selected_meanings.add(meaning)  # セットに追加
                                if len(self.fields['meaning_word'].choices) == 3:  # 要素がインデックス3番目（四つ目）がでてきたらブレイク。
                                    break        
                    random.shuffle(self.fields['meaning_word'].choices)  # 選択肢をシャッフル
                else:  # POSTメソッドのときはなにもしない
                    pass
    

