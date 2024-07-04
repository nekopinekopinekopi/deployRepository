from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, CreateView, DeleteView, UpdateView, ListView, 
)
from django.contrib.auth.decorators import login_required
from .forms import (
    VocabularyRegistForm, VocabularyUpdateForm, PloblemForm
)
from .models import Registered_english_words, Answers
from django.http import HttpResponse
import os
import random
import uuid




# homeページ表示
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('vocabularies', 'home.html')

    

# 英単語登録ページ
class VocabularyRegistView(LoginRequiredMixin, CreateView):
    form_class = VocabularyRegistForm
    template_name = os.path.join('vocabularies', 'vocabulary_regist.html')
    success_url = reverse_lazy('vocabularies:vocabulary_list')  # app_name定義してるからこうやって記述しなきゃだ！

    def form_valid(self, form):
        # 現在のユーザーを設定
        form.instance.user_id = self.request.user
        return super().form_valid(form)




from django.db.models import Q, F  # Qオブジェクトは、OR条件や、OR条件とAND条件を合わせてクエリを取得する際に活用できる。（ブクマしてます。）
from django.db.models.functions import Lower
# 英単語一覧ページ
class VocabularylistView(LoginRequiredMixin, ListView):
    model = Registered_english_words
    template_name = os.path.join('vocabularies', 'vocabulary_list.html')
    context_object_name = 'words'

    def get_queryset(self):
        query = self.request.GET.get('q')  # ユーザーが入力した検索クエリを'q'として取得。それをquery変数にぶち込む。
        order_by = self.request.GET.get('order_by', 'create_at')  # 作成日時順をデフォルトにする。

        if query:
            queryset = self.model.objects.filter(
                Q(user_id=self.request.user) &  # ログイン中のユーザー＆
                Q(english_word__startswith=query)  # english_wordカラムからqueryの前方一致のカラムで絞り込む
            )
        else:
            queryset =  self.model.objects.filter(user_id=self.request.user)

        if order_by == 'english_word':
            return queryset.order_by(Lower('english_word'))
        else:
            return queryset.order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 親クラスの get_context_data メソッドを呼び出し、既存のコンテキストデータを取得。
        context['query'] = self.request.GET.get('q', '')  # 'query'に、'q'が存在する場合は'q'を格納する。'q'が存在しない場合は、Noneを返すので、Noneのときの初期値として「''」を定めている。初期値を設定することで、検索クエリが空であってもエラーが発生せず、テンプレートが正常に動作するようになります。
        context['order_by'] = self.request.GET.get('order_by', 'create_at')  # 'query'に、'q'が存在する場合は'q'を格納する。'q'が存在しない場合は、Noneを返すので、Noneのときの初期値として「''」を定めている。初期値を設定することで、検索クエリが空であってもエラーが発生せず、テンプレートが正常に動作するようになります。
        context['no_results'] = not self.get_queryset().exists()  # クエリセットが空かどうかをチェック
        return context






# 英単語編集ページ
class VocabularyUpdateView(LoginRequiredMixin, UpdateView):
    model = Registered_english_words
    form_class = VocabularyUpdateForm
    template_name = os.path.join('vocabularies', 'vocabulary_update.html')
    success_url = reverse_lazy('vocabularies:vocabulary_list')  # app_name定義してるからこうやって記述しなきゃだ！

    def form_valid(self, form):
        # 現在のユーザーを設定
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    




# クイズ関連ページ
class QuizView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('vocabularies', 'quiz.html')





# 問題ページ
@login_required
def problem_view(request):
    word = None
    session = request.session
    session['quiz_count'] = session.get('quiz_count', 0)  # 'quiz_count'という名前でセッションに登録する。初期値は0。
    session['quiz_set_id'] = session.get('quiz_set_id', str(uuid.uuid4()))  # UUIDを使用してユニークなIDを生成
    session['asked_words'] = session.get('asked_words', [])  # 出題済みの英単語リストを初期化


    if request.method == 'POST':  # ユーザーが選択肢を選んで、答えるボタンを押しました。
        word_id = session.get('word_id')  # GETメソッドで取り出したセッションデータと同一のセッションデータが入ってます。
        if word_id:
            word = get_object_or_404(Registered_english_words, id=word_id, user_id=request.user.id)  # Registered_english_wordsモデルの中から、セッションデータのidと、モデルのpkが等しいものをwordにぶちこむ。モデルの等しいpkが見つからなかった場合は404エラーを返す
        choices = session.get('choices', [])  # セッションからGETの時点で取得した選択肢をchoicesにぶち込んでる。
        form = PloblemForm(request.POST, word=word, choices=choices, user=request.user)  # インスタンス生成！したのでforms.pyの__init__メソッドを呼び出す。-> forms.pyで、辞書から取り出された'word'キーがword変数に格納される。-> そのword変数が、この行の[word=word]で格納される。

        if form.is_valid():
            selected_meaning = form.cleaned_data['meaning_word']  # ユーザーが選んだ選択肢をmeaning_wordに格納して,それをselected_meaningにぶち込んでる。
            is_correct = (selected_meaning == word.meaning_word)
            # 回答を保存
            Answers.objects.create(
                choice=selected_meaning,
                is_correct=is_correct,
                registerd_english_word_id=word,
                quiz_set_id=session['quiz_set_id'],
                user_id=request.user
            )
            
            # 出題済みの英単語リストに追加
            session['asked_words'].append(word.id)
            
            session['quiz_count'] += 1
            
            
            if session['quiz_count'] >= 3:
                session['quiz_count'] = 0
                session['asked_words'] = []  # 出題済みの英単語リストをリセット
                return redirect('vocabularies:answer_view')
            else:
                return redirect('vocabularies:problem_view') 
   
    else:
        user_words_count = Registered_english_words.objects.filter(user_id=request.user.id).count()
        if user_words_count < 3:
            return render(request, 'vocabularies/cannot.html')

        available_words = Registered_english_words.objects.filter(user_id=request.user.id).exclude(id__in=session['asked_words'])
        print(f"session['asked_words']: {session['asked_words']}")

        if available_words.exists():  # exists()は、ディレクトリやファイルが存在しているかを確認するメソッド
            word = available_words.order_by('?').first()  # 出題英単語（意味も）。ランダムに1つのRegistered_english_wordsオブジェクトを取得。order_by('?')は、データベースから取り出したデータをランダムな順序に並び替える働きを持っています。first()メソッドはクエリセットから最初の1件のレコード（オブジェクト）を取得する
            form = PloblemForm(word=word, user=request.user) 
            session['word_id'] = word.id  # wordで取り出された英単語のidがセッションデータに入ってました。
            session['choices'] = form.fields['meaning_word'].choices

    
    context = {
        'form': form,
        'word': word,
    }
    
    return render(request, 'vocabularies/problem.html', context)

        
        
@login_required
def answer_view(request):
    session = request.session
    quiz_set_id = session.get('quiz_set_id', 0)
    
    answers = Answers.objects.filter(user_id=request.user, quiz_set_id=quiz_set_id).order_by('create_at')
    session['quiz_set_id'] = str(uuid.uuid4())  # 新しいクイズセットIDを生成

    context = {
        'answers': answers,
    }
    
    return render(request, 'vocabularies/answer.html', context)  
    





# 回答結果ページ(ごめんこれなしにするかも)
class AnswerView(LoginRequiredMixin, DeleteView):
    pass



# 回答結果一覧ページ
class AnswerListView(LoginRequiredMixin, ListView):
    model = Answers
    template_name = os.path.join('vocabularies', 'answer_list.html')
    context_object_name = 'answers'

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'create_at')  # デフォルトは作成日時順
        is_correct = self.request.GET.get('is_correct')

        queryset = self.model.objects.filter(user_id=self.request.user)

        # 正誤で絞り込み
        if is_correct is not None:
            if is_correct.lower() == 'true':
                queryset = queryset.filter(is_correct=True)
            elif is_correct.lower() == 'false':
                queryset = queryset.filter(is_correct=False)

        # 並べ替えオプションを適用
        if order_by == 'english_word':
            return queryset.order_by(Lower('registerd_english_word_id__english_word'))
        else:
            return queryset.order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'create_at')
        context['is_correct'] = self.request.GET.get('is_correct', '')
        context['no_results'] = not self.get_queryset().exists()  # クエリセットが空かどうかをチェック
        return context        
        



    




# 英単語削除の動き
class VocabularyDeleteView(LoginRequiredMixin, DeleteView):
    model = Registered_english_words
    template_name = os.path.join('vocabularies', 'delete.html')
    success_url = reverse_lazy('vocabularies:vocabulary_list')  # app_name定義してるからこうやって記述しなきゃだ！
   
    