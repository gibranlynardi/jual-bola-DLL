import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': True, 
                'message': 'Login Berhasil', 
                'username': username
            }, status=200)
        else:
            return JsonResponse({
                'status': False, 
                'message': 'Username atau password salah'
            }, status=401)
    return JsonResponse({'status': False, 'message': 'Metode tidak diizinkan'}, status=405)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password1') 
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username sudah digunakan'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        return JsonResponse({'status': 'success', 'message': 'Akun berhasil dibuat'}, status=200)
        
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({'status': True, 'message': 'Logout berhasil'}, status=200)