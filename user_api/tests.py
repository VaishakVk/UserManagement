from django.test import TestCase
from django.utils.encoding import force_text

from .data.user import user as usr
from .data.roles import roles as rol
from .data.permissions import permissions as per

class UserPermissionTest(TestCase):       

    ## /user/<userid>

    ''' 
    TC01 - Successfully return user permissions
    '''
    def test_user_permission_success(self):
        message = [{"id": "perm1", "name": "Can check balance"}, {"id": "perm5", "name": "Can deposit"}]
        response = self.client.get('/user/user4/')
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content.decode('utf-8')), message)

    ''' 
    TC02 - Run a test with invalid user details
    '''
    def test_user_does_not_exist(self):
        message =  {"message": "User does not exist", "status": "Error"}
        response = self.client.get('/user/user10/')
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(str(response.content.decode('utf-8')),message)

    ''' 
    TC03 - Run a test case with user that do not have any roles tagged
    '''
    def test_user_doesnot_have_roles(self):
        response = self.client.get('/user/user3/')
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "User does not have any role", "status": "Error"})

    ## Invalid Path

    ''' 
    TC04 - Access an invalid path
    '''
    def test_invalid_path(self):
        response = self.client.get('/user-permission/')
        self.assertEquals(response.status_code, 404)

    ## /checkpermission/?userid=<user_id>&permissionid=<permission_id>

    ''' 
    TC05 - Permission passed does not exist for the user
    '''
    def test_check_user_permission_error(self):
        response = self.client.get('/checkpermission/?userid=user2&permissionid=perm5')
        self.assertEquals(response.status_code, 404)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": False})

    ''' 
    TC06 - Permission passsed is valid for the user
    '''
    def test_check_user_permission_success(self):
        response = self.client.get('/checkpermission/?userid=user2&permissionid=perm6')
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": True})

    ''' 
    TC07 - User not provided as part of the query
    '''
    def test_check_user_not_provided(self):
        response = self.client.get('/checkpermission/')
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "User Id is not provided"})

    ''' 
    TC08 - Permission not provided as part of the query
    '''
    def test_check_permission_not_provided(self):
        response = self.client.get('/checkpermission/?userid=user2')
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "Permission ID is not provided"})
    
    ''' 
    TC09 - Permission passed is invalid.
    '''
    def test_check_permission_invalid(self):
        response = self.client.get('/checkpermission/?userid=user2&permissionid=perm10')
        self.assertEquals(response.status_code, 404)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "Permission ID is invalid"})

    ## /roles/<roleid> POST_PARAM:{"permissions":["perm5"]}

    ''' 
    TC10 - No body passed as part of the payload
    '''
    def test_modify_roles_no_body_passed(self):
        response = self.client.post('/roles/role3/')
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "Invalid parameters passed"})
    
    ''' 
    TC11 - Body passed with invalid parameters
    '''
    def test_modify_roles_permissions_not_passed(self):
        response = self.client.post('/roles/role3/', {"permissionsdata":["perm5"]}, content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "permissions key is not passed"})

    ''' 
    TC12 - Role does not exist
    '''
    def test_modify_roles_role_not_exists(self):
        response = self.client.post('/roles/role31/', {"permissions":["perm5"]}, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "Invalid Role ID"})

    ''' 
    TC13 - Permissions are not added since permission already exist to the role or the permission is invalid
    '''
    def test_modify_roles_permission_not_added(self):
        for i in rol:
            if i['id'] == "role3":
                role_count_before = len(i['permissions'])

        message = " Permission not added since permission perm15 is invalid or permission exists. Permission not added since permission perm17 is invalid or permission exists."
        response = self.client.post('/roles/role3/', {"permissions":["perm15", "perm17"]}, content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": message})

        for i in rol:
            if i['id'] == "role3":
                role_count_after = len(i['permissions'])
        self.assertEquals(role_count_after, role_count_before)

    ''' 
    TC14 - Multiple permissions are provided as part of the payload. Only few of them are added successfully.
         - Others are not added since permission is invalid or the permission is already tagged to the role.
    '''
    def test_modify_roles_permission_partially_added(self):
        for i in rol:
            if i['id'] == "role3":
                role_count_before = len(i['permissions'])

        response = self.client.post('/roles/role3/', {"permissions":["perm5", "perm7"]}, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": " Permission perm5 added. Permission not added since permission perm7 is invalid or permission exists."})

        for i in rol:
            if i['id'] == "role3":
                role_count_after = len(i['permissions'])
        self.assertNotEquals(role_count_after, role_count_before)
    
    ''' 
    TC15 - Adding permission to a role
    '''
    def test_modify_roles_permission_added(self):
        for i in rol:
            if i['id'] == "role3":
                role_count_before = len(i['permissions'])

        response = self.client.post('/roles/role3/', {"permissions":["perm1"]}, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": " Permission perm1 added."})
        
        for i in rol:
            if i['id'] == "role3":
                role_count_after = len(i['permissions'])
        self.assertNotEquals(role_count_after, role_count_before)

    # /permissions/<permission_id>

    ''' 
    TC16 - Permission does not exist
    '''
    def test_permission_deleted_not_exists(self):
        response = self.client.delete('/permissions/perm51/')
        self.assertEquals(response.status_code, 404)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "Permission does not exist"})

    ''' 
    TC17 - Permission deleted successfully and roles are reflected with updated permissions
    '''
    def test_permission_deleted_success(self):
        perm_count_before = 0
        perm_count_after = 0
        role_perm_count_before = 0
        role_perm_count_after = 0
        
        for i in per:
            if i['id'] == 'perm6':
                perm_count_before += 1

        for i in rol:
            if 'perm6' in i['permissions']:
                role_perm_count_before += 1

        response = self.client.delete('/permissions/perm6/')
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {"message": "Permission deleted"})

        for i in per:
            if i['id'] == 'perm6':
                perm_count_after += 1

        for i in rol:
            if 'perm6' in i['permissions']:
                role_perm_count_after += 1
        
        self.assertNotEquals(role_perm_count_after, role_perm_count_before)
        self.assertNotEquals(perm_count_after, perm_count_before)

