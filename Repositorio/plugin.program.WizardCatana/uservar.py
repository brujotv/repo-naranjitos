import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = '[B][LOWERCASE][CAPITALIZE][COLOR orange]Wizard Catana[/CAPITALIZE][/LOWERCASE][/B][/COLOR]'
EXCLUDES       = [ADDON_ID]
# Text File with build info in it.
BUILDFILE      = 'https://pastebin.com/raw/Q7b0sVER'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'https://pastebin.com/raw/0dJhT7ZM'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = '[COLOR orange]Video Aprendiendo Kodi[/COLOR]'
YOUTUBEFILE    = 'https://pastebin.com/raw/AdAm10DU'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'https://pastebin.com/raw/NUikuHcr'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'https://pastebin.com/raw/dvVtQqPP'
#########################################################

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'https://i.imgur.com/7fhM7xt.png'
ICONMAINT      = 'https://image.flaticon.com/icons/png/512/663/663543.png'
ICONAPK        = 'https://vltoolbox.com.cy/wp-content/uploads/2016/09/speedtest.png'
ICONADDONS     = 'http://icons.iconarchive.com/icons/martz90/circle/256/cydia-icon.png'
ICONYOUTUBE    = 'https://yt3.ggpht.com/a-/AAuE7mCPiqMLi2alhyshB58CRPgH0aZH-8p1NGCFtw=s288-mo-c-c0xffffffff-rj-k-no'
ICONSAVE       = 'http://'
ICONTRAKT      = 'http://'
ICONREAL       = 'http://'
ICONLOGIN      = 'http://'
ICONCONTACT    = 'https://telegram.im/img/catana'
ICONSETTINGS   = 'http://proyectatech.com/IT/img/ajustes.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'lime'
COLOR2         = 'violet'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I][COLOR '+COLOR2+']Catana[/COLOR][/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR][/I]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Version Actual:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Tema Actual:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Gracias por escoger Wizard Catana\r\n\r\nTodos nuestro Wizard en un solo Instalador.\r\nSimplemente lo mejor.'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'https://i.imgur.com/7fhM7xt.png'
CONTACTFANART  = 'http://'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'
# Url to wizard version
WIZARDFILE     = 'https://pastebin.com/raw/Q7b0sVER'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'
# Addon ID for the repository
REPOID         = ''
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = ''
# Url to folder zip is located in
REPOZIPURL     = ''
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'https://pastebin.com/raw/JiSsbCrA'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = 'Catana'
# url to image if using Image 500x50(Width can vary but height of image needs to be 50px)
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = ''
#########################################################