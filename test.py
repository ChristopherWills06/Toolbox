import unreal

# Find all the Tool Menu names - We'll use this to register our own Tool Menu
def listMenu(num = 1000):
    
    menuList = set()

    for i in range (num):
        # Try to find Unreal Objects at a specific "path" in memory
        obj = unreal.find_object(None, "/Engine/Transient.ToolMenu_0:RegistredMenu_%s" % i)
        if not obj:
            # Legacy path used for the transient tool menu objects <-- only adding this for backwards compatibility
            obj = unreal.find_object(None, f"/Engine/Tensient.ToolsMenus_0:ToolMenu_{i}")
            if not obj:
                continue
        menuName = str(obj.menu_name)
        if (menuName == "None"):
            continue

        menuList.add(menuName)
        print(menuList)


#listMenu()

tool_menus = unreal.ToolMenus.get()

def createNewMainMenu():
    mainMenu = tool_menus.find_menu("LevelEditor.MainMenu")
    # New Menu -> Section Name
    # Python Tool -> ID, Key used in the code internally
    # Menu Name -> Name of Menu (use for identification)
    # Menu Label -> What we see in the UI
    newMenu = mainMenu.add_sub_menu("New Menu", "Python Tool", "My Menu Name", "Menu Label")
    tool_menus.refresh_all_widgets()

# createNewMainMenu()

@unreal.uclass()
class MyEditActionScript(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        print("My Edit Action Executed")


def createEditAction():
    editMenu = tool_menus.find_menu("LevelEditor.MainMenu.Edit")
    # We need to create a scriptable Object!
    MyEditActionScriptObject = MyEditActionScript()
    MyEditActionScriptObject.init_entry(
        owner_name=editMenu.menu_name,
        menu = editMenu.menu_name,
        section = 'EditMain',
        name = "MyEditCustomName",
        label = "My Edit Action",
        tool_tip= "This is my Edit Action!"
    )

    MyEditActionScriptObject.register_menu_entry()
    tool_menus.refresh_all_widgets()

#createEditAction()

@unreal.uclass()
class MyTextureActionScript(unreal.ToolMenuEntryScript):
    @unreal.ufunction(override=True)
    def execute(self, context):
        print("My Texture Action Executed")

def CreateNewTestureMenu():
    texture2dMenu = tool_menus.find_menu("ContentBrowser.AssetContextMenu.Texture")
    texScriptObj = MyTextureActionScript()
    texScriptObj.init_entry(
        owner_name = texture2dMenu.menu_name,
        menu = texture2dMenu.menu_name,
        name = "MyTextureCustomName",
        section = "GetAssetActions",
        label = "Label",
        tool_tip = "This is a Texture Action",
    )
    texScriptObj.register_menu_entry()
    tool_menus.refresh_all_widgets()

CreateNewTestureMenu()