import pygame
import pygame.gfxdraw
from utils import *
from gripper import Gripper

class Style:
    def __init__(self):
        return

class State:
    def __init__(self):
        return

class GUI:
    def __init__(self):

        self.fullSize = (1080,720)
        self.winSize = (640,480)

        self.gui = pygame.display.set_mode(self.winSize)
        done = False
        self.clock = pygame.time.Clock()

        ## COLORS AND FONTS ##
        self.style = Style()
        self.style.bg = (255,255,255)
        self.style.primary = (0,154,255)

        self.style.red = (255,75,75)
        self.style.blue = (0,48,255)

        self.style.grey = (120,120,120)
        self.style.black = (20,20,20)
        self.style.white = (255, 255, 255)

        self.style.good = (33,206,153)
        self.style.adequate = (255,162,0)
        self.style.bad = (255,75,75)

        self.style.primaryFont = './venus_rising_rg.ttf'
        self.style.secondaryFont = './Montserrat-Regular.ttf'
        self.style.secondaryFontBold = './Montserrat-Bold.ttf'

        ## GUI AND GRIPPER STATE ##
        self.state = State()
        self.state.closed = False
        self.state.fanSpeed = 50
        self.state.draggingFanSpeed = False

        ## INITIAL POSITIONS ##
        self.closeButtonRect = (75, 120, 200, 70)
        self.openButtonRect = (self.winSize[0]-275, 120, 200, 70)
        self.infoHeight = 220
        self.fanSpeedHeight = 350

        self.render()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.clickEvent(pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.state.draggingFanSpeed = False

            self.gui.fill(self.style.bg)
            self.render()
            self.renderInfo()

            pygame.display.flip()
            self.clock.tick(60)

    def render(self):
        self.renderButtons()
        self.renderLabels()
        self.renderSlider()

    def renderButtons(self):

        AAfilledRoundedRect(self.gui, self.style.primary, self.closeButtonRect, 0.3)
        if not self.state.closed:
            AAfilledRoundedRect(self.gui, self.style.bg, (self.closeButtonRect[0]+3,self.closeButtonRect[1]+3,self.closeButtonRect[2]-6,self.closeButtonRect[3]-6), 0.2)
        closeTxt = pygame.font.Font(self.style.secondaryFontBold, 30)
        closeTxtSurf, closeTxtRect = text_objects("CLOSE", closeTxt, (self.style.bg if self.state.closed else self.style.primary))
        closeTxtRect.center = (self.closeButtonRect[0] + self.closeButtonRect[2]/2, self.closeButtonRect[1] + self.closeButtonRect[3]/2)
        self.gui.blit(closeTxtSurf, closeTxtRect)

        AAfilledRoundedRect(self.gui, self.style.primary, self.openButtonRect, 0.3)
        if self.state.closed:
            AAfilledRoundedRect(self.gui, self.style.bg, (self.openButtonRect[0]+3,self.openButtonRect[1]+3,self.openButtonRect[2]-6,self.openButtonRect[3]-6), 0.2)
        openTxt = pygame.font.Font(self.style.secondaryFontBold, 30)
        openTxtSurf, openTxtRect = text_objects("OPEN", openTxt, (self.style.primary if self.state.closed else self.style.bg))
        openTxtRect.center = (self.openButtonRect[0] + self.openButtonRect[2]/2, self.openButtonRect[1] + self.openButtonRect[3]/2)
        self.gui.blit(openTxtSurf, openTxtRect)
        return

    def renderLabels(self):
        festoTxt = pygame.font.Font(self.style.primaryFont, 40)
        festoTxtSurf, festoTxtRect = text_objects("FESTO", festoTxt, self.style.primary)
        festoTxtRect.topleft = (20,20)
        self.gui.blit(festoTxtSurf, festoTxtRect)

        pygame.draw.line(self.gui, self.style.grey, (20,75), (self.winSize[0]-20,75), 2)

        widthTxt = pygame.font.Font(self.style.secondaryFont, 22)
        widthTxtSurf, widthTxtRect = text_objects("Width: ", widthTxt, self.style.black)
        widthTxtRect.topleft = (self.closeButtonRect[0],self.infoHeight)
        self.gui.blit(widthTxtSurf, widthTxtRect)
        self.widthLabelRect = widthTxtRect

        healthTxt = pygame.font.Font(self.style.secondaryFont, 22)
        healthTxtSurf, healthTxtRect = text_objects("Health: ", healthTxt, self.style.black)
        healthTxtRect.topleft = (self.openButtonRect[0],self.infoHeight)
        self.gui.blit(healthTxtSurf, healthTxtRect)
        self.healthLabelRect = healthTxtRect

        resistanceTxt = pygame.font.Font(self.style.secondaryFont, 22)
        resistanceTxtSurf, resistanceTxtRect = text_objects("Resistance: ", resistanceTxt, self.style.black)
        resistanceTxtRect.topleft = (self.closeButtonRect[0],self.infoHeight+40)
        self.gui.blit(resistanceTxtSurf, resistanceTxtRect)
        self.resistanceLabelRect = resistanceTxtRect

        currentTxt = pygame.font.Font(self.style.secondaryFont, 22)
        currentTxtSurf, currentTxtRect = text_objects("Current: ", currentTxt, self.style.black)
        currentTxtRect.topleft = (self.openButtonRect[0],self.infoHeight+40)
        self.gui.blit(currentTxtSurf, currentTxtRect)
        self.currentLabelRect = currentTxtRect

        fanSpeedLabel = pygame.font.Font(self.style.secondaryFont, 22)
        fanSpeedLabelSurf, fanSpeedLabelRect = text_objects("Fan Speed: ", fanSpeedLabel, self.style.black)
        fanSpeedLabelRect.topleft = (self.closeButtonRect[0],self.fanSpeedHeight)
        self.gui.blit(fanSpeedLabelSurf, fanSpeedLabelRect)
        self.fanSpeedLabelRect = fanSpeedLabelRect

        fanSpeedVal = pygame.font.Font(self.style.secondaryFont, 22)
        fanSpeedValSurf, fanSpeedValRect = text_objects(str(self.state.fanSpeed), fanSpeedVal, self.style.black)
        fanSpeedValRect.midright = (self.openButtonRect[0]+self.openButtonRect[2]-15, fanSpeedLabelRect.bottom+24)
        self.gui.blit(fanSpeedValSurf, fanSpeedValRect)

        fanSpeedUnit = pygame.font.Font(self.style.secondaryFont, 14)
        fanSpeedUnitSurf, fanSpeedUnitRect = text_objects("%", fanSpeedUnit, self.style.grey)
        fanSpeedUnitRect.bottomright = (self.openButtonRect[0]+self.openButtonRect[2], fanSpeedValRect.bottom-2)
        self.gui.blit(fanSpeedUnitSurf, fanSpeedUnitRect)
        return

    def renderSlider(self):
        sliderOuter = (self.closeButtonRect[0], self.fanSpeedLabelRect.bottom+20, \
                       self.openButtonRect[0] + self.openButtonRect[2] - self.closeButtonRect[0] - 50, 8)
        sliderInner = (sliderOuter[0]+2, sliderOuter[1]+2, sliderOuter[2]-4, sliderOuter[3]-4)
        AAfilledRoundedRect(self.gui, self.style.black, sliderOuter, 1)
        AAfilledRoundedRect(self.gui, self.style.white, sliderInner, 1)

        if self.state.draggingFanSpeed:
            self.state.fanSpeed = round(min(max((pygame.mouse.get_pos()[0]-sliderInner[0])/sliderInner[2],0),1)*100)
        self.sliderDragger = (sliderInner[0] + int(sliderInner[2]*self.state.fanSpeed/100), sliderOuter[1]+4, 7)

        if self.state.fanSpeed <= 50:
            pygame.draw.rect(self.gui, self.style.red, \
                             (self.sliderDragger[0], sliderInner[1], \
                              sliderInner[0]+(sliderInner[2]/2)-self.sliderDragger[0], sliderInner[3]))
        else:
            pygame.draw.rect(self.gui, self.style.blue, \
                             (sliderInner[0]+(sliderInner[2]/2), sliderInner[1], \
                              self.sliderDragger[0]-sliderInner[0]-(sliderInner[2]/2), sliderInner[3]))


        pygame.gfxdraw.circle(self.gui, self.sliderDragger[0], self.sliderDragger[1], self.sliderDragger[2], self.style.grey)
        pygame.draw.circle(self.gui, self.style.grey, (self.sliderDragger[0], self.sliderDragger[1]), self.sliderDragger[2]+1)
        return

    def renderInfo(self):
        width = gripper.getGripperWidth()
        health = gripper.getGripperHealth()
        resistance = gripper.getSMAResistance()
        current = gripper.getSMACurrent()

        widthVal = pygame.font.Font(self.style.secondaryFont, 16)
        widthValSurf, widthValRect = text_objects(str(width), widthVal, self.style.primary)
        widthValRect.bottomleft = (self.widthLabelRect.right+5,self.widthLabelRect.bottom)
        self.gui.blit(widthValSurf, widthValRect)
        widthUnit = pygame.font.Font(self.style.secondaryFont, 12)
        widthUnitSurf, widthUnitRect = text_objects(" mm", widthUnit, self.style.grey)
        widthUnitRect.bottomleft = (widthValRect.right+5,self.widthLabelRect.bottom)
        self.gui.blit(widthUnitSurf, widthUnitRect)

        healthVal = pygame.font.Font(self.style.secondaryFont, 16)
        if health == "Good":
            clr = self.style.good
        elif health == "Adequate":
            clr = self.style.adequate
        else:
            clr = self.style.bad
        healthValSurf, healthValRect = text_objects(health, healthVal, clr)
        healthValRect.bottomleft = (self.healthLabelRect.right+5,self.healthLabelRect.bottom)
        self.gui.blit(healthValSurf, healthValRect)

        resistanceVal = pygame.font.Font(self.style.secondaryFont, 16)
        resistanceValSurf, resistanceValRect = text_objects(str(resistance), resistanceVal, self.style.primary)
        resistanceValRect.bottomleft = (self.resistanceLabelRect.right+5,self.resistanceLabelRect.bottom)
        self.gui.blit(resistanceValSurf, resistanceValRect)
        resistanceUnit = pygame.font.Font(self.style.secondaryFont, 12)
        resistanceUnitSurf, resistanceUnitRect = text_objects(" Ohms", resistanceUnit, self.style.grey)
        resistanceUnitRect.bottomleft = (resistanceValRect.right+5,self.resistanceLabelRect.bottom)
        self.gui.blit(resistanceUnitSurf, resistanceUnitRect)

        currentVal = pygame.font.Font(self.style.secondaryFont, 16)
        currentValSurf, currentValRect = text_objects(str(current), currentVal, self.style.primary)
        currentValRect.bottomleft = (self.currentLabelRect.right+5,self.currentLabelRect.bottom)
        self.gui.blit(currentValSurf, currentValRect)
        currentUnit = pygame.font.Font(self.style.secondaryFont, 12)
        currentUnitSurf, currentUnitRect = text_objects(" Amps", currentUnit, self.style.grey)
        currentUnitRect.bottomleft = (currentValRect.right+5,self.currentLabelRect.bottom)
        self.gui.blit(currentUnitSurf, currentUnitRect)

    def clickEvent(self, pos):
        if clickCollisionRect(pos, self.closeButtonRect):
            self.state.closed = True
            gripper.closeGripper()
        elif clickCollisionRect(pos, self.openButtonRect):
            self.state.closed = False
            gripper.openGripper()
        if clickCollisionCircle(pos, self.sliderDragger):
            self.state.draggingFanSpeed = True
        self.render()

gripper = Gripper()

pygame.init()
NitimaticGui = GUI();
