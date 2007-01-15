#$ neutron_plugin 01

def handler_access_login(type, source, parameters):
	if type == 'public':
		smsg(type, source, 'Please login privately so others do not see the password.')
	elif type == 'private':
		jid = get_true_jid(source)
		if parameters.strip() == ADMIN_PASSWORD:
			change_access_temp(jid, 100)
			smsg(type, source, 'Access Granted')
		else:
			smsg(type, source, 'Access Denied')

def handler_access_logout(type, source, parameters):
	jid = get_true_jid(source)
	change_access_temp(jid, 0)
	smsg(type, source, 'Successfully Logged Out')

def handler_access_view_access(type, source, parameters):
	if not parameters.strip():
		smsg(type, source, str(user_level(source)))
	else:
		smsg(type, source, str(user_level(parameters)))

def handler_access_set_access(type, source, parameters):
	splitdata = string.split(parameters)
	if len(splitdata) == 2:
		change_access_temp(splitdata[0], splitdata[1])
		smsg(type, source, 'Temporary Access Change Successful')
	elif len(splitdata) == 3:
		change_access_perm(splitdata[0], splitdata[1])
		smsg(type, source, 'Permanent Access Change Successful')
	else:
		smsg(type, source, 'Invalid Syntax')


register_command_handler(handler_access_login, '!login', 0, 'Logs in as admin.', '!login <password>', ['!login mypassword'])
register_command_handler(handler_access_login, '!logout', 0, 'Logs out of admin.', '!logout', ['!logout'])
register_command_handler(handler_access_view_access, '!view_access', 0, 'Returns access level of specified JID. JID defaults to requester.', '!view_access [JID]', ['!view_access', '!view_access mikem@jabber.org'])
register_command_handler(handler_access_set_access, '!set_access', 100, 'Sets the access level of specified JID to specified level. If a third parameter is defined, the change will be permanent, otherwise it will reset when Neutron exits.', '!set_access <JID> <level#> [permanent]', ['!set_access mikem@jabber.org 100', '!set_access mikem@jabber.org 100 blabla'])
