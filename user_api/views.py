from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .shared import (
                    get_user_details, 
                    get_role_details, 
                    get_permission_details, 
                    get_permissions, 
                    delete_permission, 
                    delete_roles_permission
                    )
import json

def home(request):
    return render(request, 'home.html')

# /user/<userid>
def get_permissions_user(request, user_id):
    permission_data = get_permissions(user_id)
    
    if permission_data['status'] == "Success":
        return JsonResponse(permission_data["data"], status= 200, safe=False)
    elif permission_data['status'] == "Error":
        return JsonResponse(permission_data, status= 400, safe=False)

# /checkpermission/?userid=<user_id>&permissionid=<permission_id>
def check_user_permission(request):
    user_id = request.GET.get('userid')
    permission_id = request.GET.get('permissionid')

    if (not user_id):
        return JsonResponse({"message": "User Id is not provided"}, status= 400, safe=False)

    if (not permission_id):
        return JsonResponse({"message": "Permission ID is not provided"}, status= 400, safe=False)

    if (not get_permission_details(permission_id)):
        return JsonResponse({"message": "Permission ID is invalid"}, status= 404, safe=False)

    permission_data = get_permissions(user_id)
    
    if permission_data['status'] == "Success":
        for i in permission_data['data']:
            if i['id'] == permission_id:
                return JsonResponse({'message': True}, status= 200, safe=False)        
        return JsonResponse({"message": False}, status= 404, safe=False)

    elif permission_data['status'] == "Error":
        return JsonResponse(permission_data, status= 400, safe=False)

# /roles/<roleid> POST_PARAM:{"permissions":["perm5"]}
@csrf_exempt
def modify_role_permissions(request, role_id):
    message = ''
    status = 400

    try:
        body_data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({"message": "Invalid parameters passed"}, status= 400, safe=False)

    if 'permissions' not in body_data:
        return JsonResponse({"message": "permissions key is not passed"}, status= 400, safe=False)
    
    permission_ids = body_data['permissions']

    role_details = get_role_details(role_id)
    if not role_details:
        return JsonResponse({"message": "Invalid Role ID"}, status= 404, safe=False)

    for i in permission_ids:
        if get_permission_details(i) and not i in role_details['permissions']:
            role_details['permissions'].append(i)
            message = message + ' Permission ' + str(i) +' added.'
            status = 200

        else:
            message = message + ' Permission not added since permission ' + str(i) + ' is invalid or permission exists.'
    
    return JsonResponse({"message": message}, status=status, safe=False)

# /permissions/<permission_id> 
@csrf_exempt
def delete_permissions(request, permission_id):
    permission_data = delete_permission(permission_id)
    if permission_data:
        status = delete_roles_permission(permission_id)
        if status == "Success":
            return JsonResponse({'message': "Permission deleted"}, status= 200, safe=False)    
        elif status == "Error":
            return JsonResponse({'message': "Unexpected Error."}, status= 500, safe=False)
    else:
        return JsonResponse({'message': "Permission does not exist"}, status= 404, safe=False)

def error_404(request, page_not_found):
    return JsonResponse({'message': "Page does not exist"}, status= 404, safe=False)
