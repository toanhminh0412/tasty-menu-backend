from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token

# User login
@csrf_exempt  # Use this because there is no CSRF token if user is not logged in
@require_http_methods(["POST"])  # Restrict this view to POST requests only
@ensure_csrf_cookie
def user_login(request):
    # Import the JSON module to parse the request body
    import json

    # Parse the request body to get the credentials
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Check if both email and password have been provided
    if not email or not password:
        return JsonResponse({'error': 'Email and password are required'}, status=400)

    # Authenticate the user
    user = authenticate(request, username=email, password=password)
    if user is not None:
        # Log the user in
        login(request, user)

        # Return a success response
        return JsonResponse({
            'success': 'User logged in successfully',
            'csrftoken': get_token(request),
            'sessionid': request.session.session_key,
        })
    else:
        # Return an error response if authentication fails
        return JsonResponse({'error': 'Wrong email or password. Please try again!'}, status=400)
    
# User signup
@csrf_exempt
@require_http_methods(["POST"])
@ensure_csrf_cookie
def user_signup(request):
    # Import the JSON module to parse the request body
    import json

    # Parse the request body to get the credentials
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Check if both email and password have been provided
    if not email or not password:
        return JsonResponse({'error': 'Email and password are required'}, status=400)

    from django.contrib.auth.models import User
    # Check if the user already exists
    if User.objects.filter(username=email).exists():
        return JsonResponse({'error': 'User already exists'}, status=400)

    # Create a new user
    user = User.objects.create_user(email, email, password)

    # Log the user in
    login(request, user)

    # Return a success response
    return JsonResponse({
        'success': 'User signed up and logged in successfully',
        'csrftoken': get_token(request),
        'sessionid': request.session.session_key,
    })
    
# User logout
@require_http_methods(["POST"])  # Restrict this view to POST requests only
def user_logout(request):
    # Log the user out
    logout(request)
    response = JsonResponse({"detail": "Logout successful"})

    # Optionally, invalidate the CSRF token by setting an expired value
    response.delete_cookie('csrftoken')  # This line is optional since CSRF is stateless

    # Invalidate the session cookie by setting it to expire
    response.delete_cookie('sessionid')

    return response
