# User Management

## Routes

### GET

**/user/user_id** - Permissions related to a particular user

**/checkpermission/?userid=user_id&permissionid=permission_id** - Check if the permission provided exists for the user

### POST

**roles/role_id** - Add permissions to a role
Pass the permission as query parameter

```
{
  "permissions": ["perm1"]
}

```
### DELETE

**permissions/permission_id/** - Delete an existing permission
