from django.db import models
from accounts.models import Users
import uuid



# 英単語登録テーブル
class Registered_english_words(models.Model):
    english_word = models.CharField(max_length=100)
    meaning_word = models.CharField(max_length=100)
    example_sentence = models.TextField(max_length=200)
    meaning_of_example_sentence = models.TextField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_addはオブジェクトが最初に作成されるとき、自動的にフィールドに現在の日付をセットします。
    update_at = models.DateTimeField(auto_now=True)  # auto_nowはオブジェクトが保存される度に自動的に現在の日付をセットします。
    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.english_word


    


# # クイズテーブル
# class Quizzes(models.Model):
#     # choice = models.CharField(max_length=100)
#     create_at = models.DateTimeField(auto_now_add=True)  # auto_now_addはオブジェクトが最初に作成されるとき、自動的にフィールドに現在の日付をセットします。
#     update_at = models.DateTimeField(auto_now=True)  # auto_nowはオブジェクトが保存される度に自動的に現在の日付をセットします。
#     # registerd_english_word_id = models.ForeignKey(
#     #     Registered_english_words, on_delete=models.CASCADE
#     # )
    
    
    
    
# 回答テーブル
class Answers(models.Model):
    quiz_set_id = models.UUIDField(default=uuid.uuid4, editable=False)
    choice = models.CharField(max_length=100, null=True)
    is_correct = models.BooleanField(null=True)  # 基本的に、引数には「default=True」を指定するらしいけど、、、
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_addはオブジェクトが最初に作成されるとき、自動的にフィールドに現在の日付をセットします。
    update_at = models.DateTimeField(auto_now=True)  # auto_nowはオブジェクトが保存される度に自動的に現在の日付をセットします。
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True) 
    registerd_english_word_id = models.ForeignKey(
        Registered_english_words, on_delete=models.CASCADE, null=True
    )
