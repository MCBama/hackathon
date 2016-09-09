def login_mobile(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      login(request, user)
      return redirect('/map_view/')
    else:
      return HttpResponseNotFound('User not active')
  else:
    return HttpResponseNotFound("User doesn't exist")
