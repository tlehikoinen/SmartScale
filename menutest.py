class Menu:
    # Protyping menu system for 16*2 lcd screen with keypad
    # Construct different menus, keep hold of current,
    # return state, move to next, move to previous etc..
    #
    def __init__(self, menuItems):
        self.menuItems = menuItems
        self.currentState = State(0, menuItems[0])

    def printMenuItems(self):
        for item in self.menuItems:
            print(item)
    
    def printCurrentState(self):
        print("Item: " + self.currentState.item + " index: " + str(self.currentState.index))

    def getCurrentState(self):
        return self.currentState

    def moveToPreviousState(self):
        if self.currentState.index == 0:
            return
        self.currentState.index = self.currentState.index - 1
        self.currentState.item = self.menuItems[self.currentState.index]

    def moveToNextState(self):
        if self.currentState.index == len(self.menuItems) -1:
            return
        self.currentState.index = self.currentState.index + 1
        self.currentState.item = self.menuItems[self.currentState.index]
   
class State:
    def __init__(self, index, menuItem):
        self.index = index
        self.item = menuItem

def main():
    menuItems = ["first item", "second item", "third item"]
    menu = Menu(menuItems)
    while(True):
        menu.printCurrentState()
        selection = input("Up or down? U/D")
        if selection == 'U':
            menu.moveToNextState()
        elif selection == 'D':
            menu.moveToPreviousState()
        else:
            print('Wrong input')



if __name__ == "__main__":
    main()

