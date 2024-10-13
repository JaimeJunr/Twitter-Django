from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.forms import AuthenticationForm

from .forms import UserRegisterForm, ProfileImageForm, CommentForm, CustomAuthenticationForm

from django.urls import reverse_lazy

from user.models import Like, User, Comment, Tweet, Follow


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Verifique se este caminho está correto
    form_class = CustomAuthenticationForm  # Use a forma personalizada para o login

    def get_success_url(self):
        # Obtém a URL 'next' da requisição, se disponível
        next_url = self.request.GET.get('next')

        # Verifica se a URL 'next' é segura antes de redirecionar
        if next_url and is_safe_url(url=next_url, allowed_hosts=self.request.get_host()):
            return next_url

        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, "Nome de usuário ou senha inválidos.")
        return super().form_invalid(form)


@method_decorator(csrf_protect, name='dispatch')
def custom_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona após o login
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")

    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    user = request.user  # Assume que você está autenticado
    
    # Verificando se está na aba "Para você" ou "Seguindo"
    following = request.GET.get("following", "false").lower() == "true"
    
    if following:
        following_users = user.followings.values_list("following_id", flat=True)
        tweets = Tweet.objects.filter(user__in=following_users).order_by("-created_at")
    
        
    else:
        # Mostra tweets recomendados para você
        tweets = Tweet.objects.all().order_by("-created_at")
        
    liked_tweet_ids = list(
        Like.objects.filter(user=user).values_list("tweet_id", flat=True)
    )
    
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Tweet.objects.create(user=user, content=content)
            messages.success(request, "Tweet criado com sucesso!")
            return redirect("home")
    

    context = {
        "tweets": tweets,
        "liked_tweet_ids": liked_tweet_ids,
        "fallowing": following 
    }

    return render(request, "home.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(request, "Usuário registrado com sucesso!")
            return redirect("login")
        else:
            messages.error(request, "Erro ao cadastrar usuário: %s" % form.errors)
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
@require_POST
def retweet(request, tweet_id):
    original_tweet = get_object_or_404(Tweet, id=tweet_id)
    user = request.user
    content = request.POST.get("content", "").strip()
    

    already_retweeted = Tweet.objects.filter(
        user=user, original_tweet=original_tweet, is_retweet=True
    ).exists()

    if already_retweeted:
        HttpResponseBadRequest("Você já retweetou este tweet.")
    else:
        
        retweet = Tweet.objects.create(user=user, original_tweet=original_tweet, is_retweet=True, retweet_content=content)

 
        messages.success(request, "Retweet feito com sucesso!")
        print(Tweet.retweet_count())
    
    return JsonResponse({"retweetCount": 0})


@login_required
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Verifica se o usuário já curtiu o comentário
    liked = Like.objects.filter(user=user, comment=comment).exists()

    if liked:
        Like.objects.filter(user=user, comment=comment).delete()
        liked = False
    else:
        # Se não, adiciona o like
        Like.objects.create(user=user, comment=comment)
        liked = True

    total_likes = comment.likes.count()  # Conta os likes no comentário
    return JsonResponse({"liked": liked, "likes": total_likes})

@login_required
@require_POST
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    user = request.user

    # Verificar se o usuário já curtiu o tweet
    liked = Like.objects.filter(user=user, tweet=tweet).exists()

    if liked:
        Like.objects.filter(user=user, tweet=tweet).delete()
        liked = False
    else:
        # Caso contrário, adicionar o like
        Like.objects.create(user=user, tweet=tweet)
        liked = True

    total_likes = tweet.tweet_likes.count()  # Contar o total de likes
    return JsonResponse({"liked": liked, "likes": total_likes})


@login_required
def perfil_view(request):
    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Imagem de perfil atualizada com sucesso!")
            return redirect("perfil")  # Redireciona para a página de perfil3
        else:
            messages.error(request, "Erro ao atualizar a imagem de perfil.")
    else:
        form = ProfileImageForm(instance=request.user)

    return render(request, "perfil.html", {"form": form})


from django.views.generic import DetailView

class ProfileView(DetailView):
    model = User
    template_name = "user_profile.html"
    context_object_name = "user_profile"
    pk_url_kwarg = "user_id"
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        tweets = Tweet.objects.filter(user=user).order_by("-created_at")
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
        follower_count = user.followers.count()
        following_count = user.followings.count()

        context = {
            "user_profile": user,
            "tweets": tweets,
            "is_following": is_following,
            "follower_count": follower_count,
            "following_count": following_count,
        }
        return render(request, "user_profile.html", context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context["tweets"] = Tweet.objects.filter(user=user_profile).order_by("-created_at")
        context["is_following"] = Follow.objects.filter(follower=self.request.user, following=user_profile).exists()
        context["follower_count"] = user_profile.followers.count()
        context["following_count"] = user_profile.followings.count()
        return context


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if request.user == user_to_follow:
        messages.warning(request, "Você não pode seguir a si mesmo.")
        return redirect("user_profile", user_id=user_to_follow.id)

    with transaction.atomic():  # Garante que ambas as operações sejam atômicas
        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=user_to_follow
        )

        if created:
            messages.success(request, f"Você começou a seguir {user_to_follow.username}.")
        else:
            follow.delete()
            messages.success(request, f"Você deixou de seguir {user_to_follow.username}.")

    return redirect("user_profile", user_id=user_to_follow.id)


def get_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comments = Comment.objects.filter(tweet=tweet, parent_comment__isnull=True).order_by("created_at")  # Exibe apenas comentários de nível superior
    
    liked_tweet_ids = list(
        Like.objects.filter(user=request.user).values_list("tweet_id", flat=True)
    )

    context = {
        "tweet": tweet,
        "comments": comments,
        "liked_tweet_ids": liked_tweet_ids,
    }

    return render(request, "tweet.html", context)


@login_required
def comment_tweet(request, tweet_id, parent_comment_id=None):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    parent_comment = get_object_or_404(Comment, id=parent_comment_id) if parent_comment_id else None
    
    
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(
                commit=False
            )
            comment.tweet = tweet  # Associa o tweet ao comentário
            comment.user = request.user  # Associa o usuário autenticado ao comentário
            comment.parent_comment = parent_comment  # Associa o comentário pai
            comment.save()  # Salva o comentário no banco de dados

            messages.success(request, "Comentário adicionado com sucesso!")
            return redirect(
                "tweet", tweet_id=tweet.id
            )  # Redireciona para a página do tweet

        else:
            # Mensagem de erro se o formulário for inválido
            messages.error(
                request, "Erro ao adicionar comentário. Por favor, tente novamente."
            )

    return redirect("tweet", tweet_id=tweet.id)


@login_required
def suggested_users(request):
    user = request.user
    following_ids = user.followings.values_list("following_id", flat=True)
    suggestions = User.objects.exclude(id__in=following_ids).exclude(id=user.id)[:5]  # Sugestões limitadas a 5

    context = {
        "suggestions": suggestions,
    }

    return render(request, "suggested_users.html", context)