from django.shortcuts import render

def show_main(request):
    context = {
        'nama_toko' : 'Jual Bola DLL',
        'nama_pembuat' : 'Gibran Tegar Ramadhan Putra Lynardi',
        'kelas_pbp' : 'PBP D'
    }

    return render(request, "main.html", context)
