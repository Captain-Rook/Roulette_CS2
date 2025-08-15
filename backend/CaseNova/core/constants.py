LENGTH_CHAR_FIELDS = 128

STEAM_PROFILE_URL = 'https://steamcommunity.com/profiles/'
SERVER_DOMAIN = 'http://127.0.0.1:8000' 
STEAM_OPENID_URL = 'https://steamcommunity.com/openid/login'
STEAM_GET_USER_INFO_URL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
FRONTEND_URL = 'http://localhost:5173'
# Статусы
STATUS_IN_INVENTORY = 'in_inventory'
STATUS_IN_PROCESS_TO_OUTPUT = 'in_process_to_output'
STATUS_OUTPUT_ERROR = 'output_error'
STATUS_SUCCESS_OUTPUT = 'succes_output'
STATUS_USED_IN_CONTRACT = 'used_in_contract'
STATUS_CHANGED = 'changed'
STATUS_USED_IN_UPGRADE = 'used_in_upgrade'
STATUS_SALED = 'saled'

# Значения для поля `action`
ACTION_SALED = "saled"
ACTION_USED_IN_UPGRADE = "used_in_upgrade"
ACTION_USED_IN_CONTRACT = "used_in_contract"
ACTION_DISPLAYED_IN_STEAM = "displayed_in_steam"
ACTION_CHANGED = "changed"
ACTION_NONE = "none"

# Значения для поля `source`
SOURCE_CASE = "case"
SOURCE_FREE_CASE = "free_case"
SOURCE_UPGRADE = "upgrade"
SOURCE_CONTRACT = "contract"
SOURCE_PRESENT = "present"
SOURCE_CHANGE = "change"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
