from utils import update_packages, get_argument_parser_action, MessageError

action = get_argument_parser_action()

if( action == "update" ):
    file_path = './package.json'

elif( action == "reset" ):
    file_path = './package.original.json'

else:
    raise MessageError( "Invalid Argument" )

update_packages( file_path=file_path )






