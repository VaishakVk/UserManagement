from .data.user import user as usr
from .data.roles import roles as rol
from .data.permissions import permissions as per

# Get User details when user ID is passed as parameter
def get_user_details(user_id):
    for i in usr:
        if i['id'] == user_id:
            return i
    return None

# Get Role details when role ID is passed as parameter
def get_role_details(role_id):
    for i in rol:
        if i['id'] == role_id:
            return i
    return None

# Get Permission details where permission ID is passed as parameter
def get_permission_details(permission_id):
    for i in per:
        if i['id'] == permission_id:
            return i
    return None

# Returns a list with permissions of a user
def get_permissions(user_id):
    user_details = get_user_details(user_id)  
    permission_id_dict = {}
    permissions = []

    if(user_details):

        if len(user_details['roles']) == 0:
            return {"message": "User does not have any role", "status": "Error"}
        
        for role in user_details['roles']:    
            user_role_details = get_role_details(role)
            if(user_role_details):
                for permission in user_role_details['permissions']:
                    permission_detail = get_permission_details(permission)
                    
                    # Dictionary is created to store all the permissions that have been added.
                    # This is to enure that duplicate permissions are not stored.
                    if permission_detail and permission_detail['id'] not in permission_id_dict:
                        permission_id_dict[permission_detail['id']] = 1
                        permissions.append(permission_detail)
            
        return {"data": permissions, "status": "Success"}
    else:
        return {"message": "User does not exist", "status": "Error"}

# Delete permission from permission object
def delete_permission(permission_id):
    try:
        for i in range(len(per)):
            if per[i]['id'] == permission_id:
                del_permission = per[i]
                del per[i]
                return del_permission
        return None
    except:
        return None

# Delete permission from roles object
def delete_roles_permission(permission_id):
    status = "Success"
    try: 
        for i in rol:
            for j in range(len(i['permissions'])):
                if i['permissions'][j] == permission_id:
                    del i['permissions'][j]
                    break
        
        return status            
    except:
        return "Error"
