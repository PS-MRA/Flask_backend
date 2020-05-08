
WS_URL = "ws://192.168.43.188:7681"
SCREENSHOTS_PATH = "screenshots/"
BOT_LOG_FILE_NAME = "botlog.csv"
PUZZLE_JSON_3 = "/Users/mohammedansari/word_treat/scripts/puzzles_3.json"
PUZZLE_JSON_MAIN = PUZZLE_JSON_3
DAILY_PUZZLE_JSON = "wordjam_daily_puzzles.json"
DICTIONARY_FILE = "dictionary.txt"
MAGIC_BUTTON_NAME = "magicButton"
RECORD_ACTIONS = True
BATCH_UPDATE_LENGTH = 1

MAX_FAILED_STEPS = 5


# xpaths
FB_LOGIN_WEBVIEW_ANDROID = "//*[contains(@resource-id,'login_form')]"






SCREEN_NAMES = {
        1: "home",
        2: "puzzle",
        3: "country_complete",
        4: "outro",
        5: "w2e_1",
        6: "puz_pack",
        7: "dailyBonus",
        8: "country",
        9: "msgCenter",
        10: "letsConnect",
        11: "mfs",
        12: "store",
        13: "inviteAndWin",
        14: "rate_us",
        15: "how_to_play",
        16: "inviteOthers",
        17: "free_coins",
        18: "moreCoins",
        19: "settings",
        20: "eoc",
        21: "w2eOops",
        22: "w2eMore",
        23: "fbLogout",
        24: "spinner",
        25: "oos",
        26: "ooc_spinner",
        27: "fbConnect",
        28: "freeCoinsReferral",
        29: "ooc_invite",
        30: "ooc_w2e",
        31: "ooc_gift_ask",
        32: "ooc_connect",
        33: "invite_success",
        34: "ooc_share",
        35: "exit_confirm",
        36: "notifPermissions",
        37: "feedback",
        38: "notif_test",
        39: "no_ads",
        40: "support",
        41: "buildUpdate",
        42: "store",
        43: "quest_center",
        44: "how_to_play_bonus",
        45: "nativeAd",
        46: "store",
        47: "Adwall",
        48: "push_notif",
        49: "gdpr",
        50: "transBg",
        51: "ooc_offerwall",
        52: "starter_pack",
        53: "dictionary",
        54: "linear_progression",
        56: "subscription_popup",
        57: "subs_joining_bonus",
        58: "subs_free_trial",
        59: "subs_renewal_popup",
        60: "subs_offline_popup",
        61: "introduce_streak",
        62: "subs_no_ads",
        63: "ooc_subs",
        64: "subs_burst_hint",
        65: "soft_launch",
        66: "minimap",
        68: "mailSupport",
        69: "dailyCalendar",
        73: "wordWarsRequest",
        74: "collection_screen",
        75: "collection_reward",
        76: "daily_puzzle",
        77: "how_to_play_daily",
        78: "xpromo_after_w2e",
        79: "coin_grant_after_w2e",
        80: "leaderboard",
        81: "how_to_play_lb",
        82: "contact_book",
        83: "sb_reply",
        84: "vip_outro",
        85: "vip_map",
        86: "vip_puzzle",
        87: "vip_rewards",
        88: "vip_info",
        89: "install_bubble_pop",
        90: "piggy_bank",
        91: "piggy_how_to_play",
        92: "piggy_success_screen",
        93: "user_feedback_popup",
        94: "earn_free",
        95: "earn_coins_reward",
        96: "loading",
        97: "subs_clears",
        98: "subs_vip_eoc",
        99: "profile_avatar",
        100: "profile",
        101: "profile_premium_popup",
        102: "profile_edit",
        103: "profile_edit_confirm",
        104: "badges_popup",
        105: "anim_bg",
        106: "profile_badges",
        107: "star_map",
        108: "htp_digraph",
        109: "subs_upgrade",
        110: "co_op_rules",
        111: "daily_quest",
        112: "bubble_pop_iap"
    }








'''
SCREEN_NAMES = {
        1: "home",
        2: "puzzle",
        3: "country_complete",
        4: "outro",
        5: "w2e_1",
        6: "puz_pack",
        7: "dailyBonus",
        8: "country",
        9: "msgCenter",
        10: "letsConnect",
        11: "mfs",
        12: "inviteAndWin",
        13: "rate_us",
        14: "how_to_play",
        15: "free_coins",
        16: "moreCoins",
        17: "settings",
        18: "eoc",
        19: "fbLogout",
        20: "spinner",
        21: "oos",
        22: "fbConnect",
        23: "freeCoinsReferral",
        24: "ooc_w2e",
        25: "invite_success",
        26: "exit_confirm",
        27: "notifPermissions",
        28: "feedback",
        29: "notif_test",
        30: "no_ads",
        31: "support",
        32: "buildUpdate",
        33: "quest_center",
        34: "new_store",
        35: "oov_offerwall",
        36: "ooc_offerwall",
        37: "how_to_play_dc",
        38: "how_to_play_bonus",
        39: "redirect_push_notif",
        40: "more_games",
        41: "dc_already_completed",
        42: "dc_complete",
        43: "gdpr",
        44: "collection_screen",
        45: "earn_coins",
        46: "milestone_zoom",
        47: "new_store_v2",
        48: "leaderboard",
        49: "how_to_play_event",
        50: "event_start",
        51: "event_complete",
        52: "xpromo_after_w2e",
        53: "coin_grant_after_w2e",
        54: "introducing_streak",
        55: "dictionary",
        56: "collection_reward",
        57: "mailSupport",
        58: "dailyCalendar",
        59: "soft_launch",
        60: "contact_book",
        61: "store",
        62: "purchase_complete",
        63: "linear_progression",
        64: "minimap",
        65: "install_bubble_pop",
        66: "purchase_complete_2",
        67: "how_to_play_event_leagues",
    }
'''

GAME_BACK_SPRITE_NAME = "#back_new.png"

ACTIONS_IN_SCREEN = {
    "puzzle" : ["solve_bonus_words", "solve_puzzle"],
    "daily_puzzle": ["solve_daily_puzzle"],
}

class RECORD_LOG_POSITON:
    CURRENT_SCREEN = 4
    STEP_ID = 0
    ACTION = 1
    PARAMS = 2
    ACTION_TYPE = 3
    TIMESTAMP = 5
    GAME_DATA = 6
