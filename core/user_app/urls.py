from django.urls import path
from user_app import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from user_app.profile_views import views_profile
app_name = "user"

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("change_password/", views.change_password, name="change_pass"),
    path('change_password_success/', views.change_password_success, name='change_password_success'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="pages/password/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="pages/password/password_reset_form.html", success_url = reverse_lazy('user:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="pages/password/password_reset_complete.html"), name='password_reset_complete'),
    #####urls profiles##############
    path('profile/', views_profile.profile_home, name="profile"),
    path('account/',views_profile.account, name="account" )
]
