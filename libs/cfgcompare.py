"""
read commands,buttons etc from csv files each in its own dict() for each type

make a map that points
  each identifier to the dict that stores its attributes for its type
  lets call it known_identifiers

  
have a list of sections called sections
  each section stores identifiers for cvars and commands and buttons
  
  aliases and binds have their own sections and data structures
  
  alias structure is map alias -> aliascmds
  binds structure is map key -> bindingcmds
  
have a map that maps identifiers to sections


tokenize the two input configs

for each input config
  separate commands, cvars, buttons, aliases, binds by checking for them in 
    known_identifiers.
    store each identifier in a separate structure, depending on its type
    command structure needs
      placeholders for the settings of the two players
      identifier for command
    cvar structure
      placeholders for the settings of the two players
      identifier for command
    button structure
      placeholders for the settings of the two players (seen or not)
      identifier for command
    alias structure
      alias commands for each player
      alias identifier for each player
    binds structure
      binding for each player
      key bound for each player
  
  if an identifier is unknown
    we know if it's a bind or alias, put it in respective section
    binds are commands with 2 arguments, cmd is bind
    aliases are commands with 2 arguments, cmd is alias
    
    when 0 arguments, it's either a command or cvar with no argument(does nothing)
    when 1 arg, can be a command or cvar
    when 2 arg, nfi, cmd or cvar again
    in any case 
    put it in section of unknowns
    
avoid doing loops in the template, pass only ready data

in 2 columns - 1 for each player
  fill the sections below
  
we want to be able to display only fields where the data for the two
users is different. 

"""


import csv

from quakeconfig.libs.cfgtokenizer import CfgTokenizer, strip_quotes

cfgtokenizer = CfgTokenizer()


def tokenizeconfigs(cfg_a, cfg_b):
    tokens_a = []
    tokens_b = []

    if cfg_a is not None:
        cfg_a_string = cfg_a.read().decode('utf8', errors='replace')
        tokens_a = cfgtokenizer.tokenize(cfg_a_string)

    if cfg_b is not None:
        cfg_b_string = cfg_b.read().decode('utf8', errors='replace')
        tokens_b = cfgtokenizer.tokenize(cfg_b_string)

    return tokens_a, tokens_b


class Data:

    def __init__(self, data_dir):

        prem_cmds_file = data_dir + \
            'Quake Live Console Guide - Premium Server Commands.csv'
        cvars_file = data_dir + \
            'Quake Live Console Guide - ConsolVariables.csv'
        ccmds_file = data_dir + 'Quake Live Console Guide - ConsolCommands.csv'
        btn_file = data_dir + 'Quake Live Console Guide - ButtonCommands.csv'

        """
        cvar or cmd -> 
            list of attribute_name:value pairs
        """
        cmds = dict()

        # first item is name of the section, the rest are cvars in it
        sections = [
            [
                'mouse', 'sensitivity', 'cl_mouseaccel', 'cl_mousesenscap', 'in_mouse', 'm_cpi', 'm_yaw', 'm_pitch', 'm_filter', 'cl_mouseacceloffset', 'cl_mouseaccelstyle', 'cl_mouseaccelpower', 'm_forward', 'm_side', 'in_restart'
            ],
            [
                'zoom', 'cg_fov', 'cg_zoomfov', 'cg_zoomSensitivity', 'cg_zoomToggle', 'cg_zoomScaling', 'cg_zoomOutOnDeath'
            ],
            [
                'player', 'name', 'model', 'handicap'
            ],
            [
                'enemy', 'cg_enemyUpperColor', 'cg_enemyLowerColor', 'cg_enemyHeadColor', 'cg_forceEnemyModel', 'cg_forceEnemyWeaponColor', 'cg_playerLean', 'cg_shadows', 'cg_impactsparks', 'cg_impactsparkslifetime', 'cg_impactsparkssize', 'cg_impactSparksVelocity', 'cg_deadBodyColor', 'cg_drawAttacker', 'r_ambientscale', 'cg_allowtaunt', 'cg_gibs'
            ],
            [
                'team', 'cg_forceTeamModel', 'cg_forceTeamSkin', 'cg_forceTeamWeaponColor', 'cg_teamheadcolor', 'cg_teamuppercolor', 'cg_teamlowercolor', 'cg_teamcolor'
            ],
            [
                'chat', 'cg_teamChatBeep', 'cg_chatbeep', 'cg_teamchatsonly', 'cg_chathistorylength', 'cl_allowConsoleChat'
            ],
            [
                # not in db   ,'net_noipx'
                'network', 'cl_timenudge', 'cl_autoTimeNudge', 'rate', 'cl_maxpackets', 'net_noudp', 'cl_packetdup', 'cg_smoothClients', 'cg_predictItems', 'cg_nopredict', 'cg_predictItems'
            ],
            [
                'hud', 'cg_drawfps', 'cg_drawfragmessages', 'cg_drawfriend', 'cg_drawteamoverlay', 'cg_selfOnTeamOverlay', 'cg_drawteamoverlayopacity', 'cg_drawteamoverlayx', 'cg_drawteamoverlayy', 'cg_weaponBar', 'cg_drawfullweaponbar', 'cg_drawitempickups', 'cg_drawrewards', 'cg_drawpregamemessages', 'cg_useItemMessage', 'cg_useItemWarning', 'cg_hudfiles', 'cg_lowAmmoWarningPercentile', 'cg_lowAmmoWeaponBarWarning', 'cg_scoreplums', 'cg_viewsize'
            ],
            [
                'graphics', 'r_picmip', 'r_contrast', 'r_gamma', 'r_texturemode', 'r_fullbright', 'r_vertexlight', 'r_ignorehwgamma', 'r_lodbias', 'r_lodscale', 'r_mapoverbrightbits', 'r_mapoverbrightcap', 'r_intensity', 'r_lightmap', 'r_dynamiclight', 'r_fastsky', 'r_fastskycolor', 'cg_bob', 'cg_flagstyle', 'cg_itemfx', 'cg_simpleitems', 'cg_simpleitemsradius', 'cg_lagometer', 'cg_speedometer', 'cg_leveltimerdirection', 'cg_kickscale', 'cg_screendamage', 'cg_screenDamageAlpha', 'cg_screendamage_self', 'cg_screendamage_team', 'cg_screenDamageAlpha_Team', 'cg_marks', 'cg_waterWarp'
            ],
            [
                'bloom (more graphics)', 'r_enablebloom', 'r_enablepostprocess', 'r_bloomactive', 'r_bloombrightthreshold', 'r_bloomintensity', 'r_bloompasses', 'r_bloomsaturation', 'r_bloomsceneintensity', 'r_bloomscenesaturation', 'r_bloomblurradius', 'r_bloomblurfalloff', 'r_bloomblurscale'
            ],
            [
                'sound', 'cg_hitbeep', 'cg_killbeep', 's_volume', 's_doppler', 's_ambient', 'cg_stereoSeparation', 's_mixPreStep', 's_musicvolume', 'com_soundMegs', 's_mixahead', 'cg_buzzersound', 'cg_lowAmmoWarningSound', 'cg_playteamvo', 'cg_rewardsvo'
            ],
            [
                'crosshair', 'cg_drawcrosshair', 'cg_drawcrosshairnames', 'cg_crosshairsize', 'cg_crosshairhitstyle', 'cg_crosshairhitcolor', 'cg_crosshaircolor', 'cg_crosshairpulse', 'cg_crosshairhittime', 'cg_drawcrosshairnamesopacity', 'cg_drawCrosshairTeamHealth', 'cg_crosshairbrightness'
            ],
            [
                'gun', 'cg_switchOnEmpty', 'cg_switchToEmpty', 'cg_drawgun', 'cg_gunZ', 'cg_gunY', 'cg_gunX', 'cg_bubbletrail', 'cg_muzzleflash'
            ],
            [
                'lightning gun', 'cg_lightningStyle', 'cg_lightningImpact', 'cg_lightningimpactcap', 'cg_trueLightning'
            ],
            [
                'railgun', 'color1', 'color2', 'cg_railTrailTime', 'cg_railStyle', 'r_railSegmentLength', 'r_railCoreWidth', 'r_railWidth', 'cg_predictlocalrailshots'
            ],
            [
                'rocket launcher', 'cg_smokeRadius_RL'
            ],
            [
                'shotgun', 'cg_trueshotgun', 'cg_smoke_SG'
            ],
            [
                'grenade launcher', 'cg_smokeRadius_GL', 'cg_weaponColor_grenade'
            ],
            [
                'demo', 'cg_autoaction', 'cl_demorecordmessage'
            ],
            [
                'console', 'con_background', 'con_height', 'con_opacity', 'con_scale', 'con_speed', 'con_timestamps'
            ],
            [
                'game client', 'r_mode', 'r_customheight', 'r_customwidth', 'r_windowedmode', 'r_fullscreen', 'com_maxfps', 'com_idleSleep', 'password', 'winkey_disable'
            ]
        ]

        # normalize all vars to lower
        for section in sections:
            for idx in range(1, len(section)):
                cvar = section[idx]
                section[idx] = cvar.lower()

        # create map cvar -> section_name for fast inclusion testing
        sections_map = dict()
        for section in sections:
            section_name = section[0]
            for cvar in section[1:]:
                sections_map[cvar.lower()] = section_name

        with open(prem_cmds_file, newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for cmd, permissions, summary, description in reader:
                cmds[cmd.lower()] = {
                    'type': 'prem_cmd', 'permissions': permissions, 'summary': summary, 'description': description}

        with open(cvars_file, newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for cvar, flags, default_val, usage, description, skip in reader:
                if flags == default_val == usage == description == '':
                    continue

                cmds[cvar.lower()] = {
                    'type': 'cvar', 'flags': flags, 'default value': default_val, 'usage': usage, 'description': description}

        with open(ccmds_file, newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for ccmd, flags, default_val, usage, description in reader:

                if flags == default_val == usage == description == '':
                    continue

                cmds[ccmd.lower()] = {'type': 'ccmd', 'flags': flags,
                                      'default value': default_val, 'usage': usage,
                                      'description': description}
                pass

        with open(btn_file, newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for btn, description in reader:
                cmds[btn.lower()] = {'type': 'btn', 'description': description}

        for section in sections:
            cvars = section[1:]
            for cvar in cvars:
                assert cvar.lower() in cmds, 'section cvar ({}) is missing in cmds'.format(
                    cvar)
        self.cmds = cmds
        self.sections = sections
        self.sections_map = sections_map

    def cfgcompare(self, cfg_a, cfg_b, showdiff):
        tokens_a, tokens_b = tokenizeconfigs(cfg_a, cfg_b)
        return self.gen_reports(tokens_a, tokens_b, showdiff)

    def isbind(self, tok):
        return len(tok) == 3 and tok[0].lower() == 'bind'

    def addbind(self, tok, report_binds, is_player_a):
        key = strip_quotes(tok[1].lower())
        binding = strip_quotes(tok[2])
        if is_player_a:  # create bind
            report_binds[key] = [binding, None]
        else:  # not player a
            if key in report_binds:  # bind already exists, fill player B value
                report_binds[key][1] = binding
            else:  # create bind for player B
                report_binds[key] = [None, binding]

    def isalias(self, tok):
        return len(tok) == 3 and tok[0].lower() == 'alias'

    def issection(self, tok):
        return tok[0].lower() in self.sections_map

    def addsection(self, tok, report_section, is_player_a):
        identifier = strip_quotes(tok[0].lower())
        arg = '<found in config>'
        if len(tok) >= 2:
            arg = strip_quotes(tok[1])

        attrs = self.cmds[identifier]

        if identifier not in report_section:
            report_section[identifier] = {
                'attrs': attrs, 'player A': None, 'player B': None}

        if is_player_a:
            report_section[identifier].update({'player A': arg})
        else:
            report_section[identifier].update({'player B': arg})

    def addunknown(self, tok, report, is_player_a):
        # 0 to many args
        identifier = strip_quotes(tok[0].lower())

        args = tok[1:]
        if len(args) == 0:
            args.append('<found in config>')

        if identifier not in report:
            report[identifier] = [None, None]

        if is_player_a:
            report[identifier][0] = args
        else:
            report[identifier][1] = args

    def isknown(self, tok):
        return tok[0].lower() in self.cmds

    def gen_reports(self, tokens_a, tokens_b, showdiff):

        report_binds = dict()
        report_aliases = dict()
        report_section = dict()
        report_uncat = dict()
        report_unknown = dict()

        for tokens in [tokens_a, tokens_b]:
            for tok in tokens:
                if self.isbind(tok):
                    self.addbind(tok, report_binds, id(tokens) == id(tokens_a))
                elif self.isalias(tok):
                    # same structure so we can use the same function
                    self.addbind(
                        tok, report_aliases, id(tokens) == id(tokens_a))
                elif self.issection(tok):
                    self.addsection(
                        tok, report_section, id(tokens) == id(tokens_a))
                elif self.isknown(tok):
                    self.addsection(
                        tok, report_uncat, id(tokens) == id(tokens_a))
                else:
                    # same structure so same function as binds
                    self.addunknown(
                        tok, report_unknown, id(tokens) == id(tokens_a))

        if showdiff:  # eliminate duplicates
            tmp_binds = dict(report_binds)
            for key in tmp_binds:
                vals = tmp_binds[key]
                if vals[0] == vals[1]:
                    del report_binds[key]

            tmp_alias = dict(report_aliases)
            for key in tmp_alias:
                vals = tmp_alias[key]
                if vals[0] == vals[1]:
                    del report_aliases[key]

            tmp_section = dict(report_section)
            for key in tmp_section:
                playerA = tmp_section[key]['player A']
                playerB = tmp_section[key]['player B']
                if playerA == playerB:
                    del report_section[key]

            tmp_uncat = dict(report_uncat)
            for key in tmp_uncat:
                playerA = tmp_uncat[key]['player A']
                playerB = tmp_uncat[key]['player B']
                if playerA == playerB:
                    del report_uncat[key]

            tmp_unknown = dict(report_unknown)
            for key in tmp_unknown:
                playerA = tmp_unknown[key][0]
                playerB = tmp_unknown[key][1]
                if playerA == playerB:
                    del report_unknown[key]

        return (self.sections, 
            self.sections_map, 
            report_binds, 
            report_aliases, 
            report_section, 
            report_uncat, 
            report_unknown)
