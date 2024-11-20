from tkinter import messagebox
import pygame
import tkinter as tk
import asyncio
import numpy as np
from scripts.GameController import *
from scripts.GlobalIndex import *
from scripts.SoundController import *

def showMessageBox(type, message):
    root = tk.Tk()
    root.withdraw() 
    messagebox.showwarning(type, message)
    root.destroy()

def textFormat(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, True, textColor)
    return newText

async def mainScreen(screen, font_path):
    isSound = True
    soundMenuPlay(isSound)

    while True:
        await asyncio.sleep(0)
        screen.fill((218, 241, 172))

        logo = pygame.image.load(logo_path)
        screen.blit(logo, (0,-125))

        button_ui = pygame.image.load(button_path)
        robot_icon = pygame.image.load(robot_icon_path)
        user_icon = pygame.image.load(user_icon_path)
        sound_icon = pygame.image.load(sound_icon_path)
        cross_icon = pygame.image.load(x_path)
        circle_icon = pygame.image.load(o_path)
        group_icon = pygame.image.load(icon_path)
        robot_icon = pygame.transform.scale(robot_icon,(64, 64))
        user_icon = pygame.transform.scale(user_icon,(64, 64))
        sound_icon = pygame.transform.scale(sound_icon,(64, 64))
        cross_icon = pygame.transform.scale(cross_icon,(64, 64))
        circle_icon = pygame.transform.scale(circle_icon,(64, 64))
        group_icon = pygame.transform.scale(group_icon,(32, 32))

        button_user = pygame.Rect(220, 260, 380, 90)
        text_user =textFormat("Hai người chơi", font_path, 40, (255,255,255)) 
        screen.blit(button_ui, (210, 255))
        screen.blit(user_icon, (230, 270))
        screen.blit(text_user, (300, 267))

        button_machine = pygame.Rect(220, 360, 380, 90)
        text_machine =textFormat("Chơi với máy", font_path, 40, (255,255,255)) 
        screen.blit(button_ui, (210, 355))
        screen.blit(robot_icon, (230, 370))
        screen.blit(text_machine, (320, 367))

        button_ui = pygame.transform.scale(button_ui,(180, 96))

        button_sound = pygame.Rect(220, 460, 170, 90)
        pygame.draw.rect(screen, (73, 97, 230), button_sound)
        screen.blit(button_ui, (215, 455))
        screen.blit(sound_icon, (230, 470))

        if isSound:
            screen.blit(circle_icon, (320, 470))
        else:
            screen.blit(cross_icon, (310, 470))

        button_quit = pygame.Rect(425, 460, 175, 90)
        text_quit =textFormat("Thoát", font_path, 40, (255,255,255)) 
        screen.blit(button_ui, (425, 455))
        screen.blit(text_quit, (457, 467))

        button_ui = pygame.transform.scale(button_ui,(64, 64))
        button_AI_combat = pygame.Rect(727, 530, 64, 64)
        screen.blit(button_ui, (727, 530))
        screen.blit(group_icon, (745, 548))
        
        mouse_X, mouse_Y = pygame.mouse.get_pos()
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    click = True
                
                # print(mouse_X, mouse_Y)
        
        if button_user.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)

                if client.isConnected():
                    client.deleteUser()

                username, opponent = PlayerCombat(screen, client, isSound)

                if username == None or opponent == None:
                    client.deleteUser()
                    continue

                soundClickPlay(isSound)
                soundBackGroundStop(isSound)
                soundGamePlay(isSound)

                dataInit = initGameScreen(screen)
                gameScreen(screen, dataInit, isSound, False, nameLenToIsCross(username, opponent) if( username != "" or opponent != "" )else True, None, [username, opponent] if( username != "" or opponent != "" )else None )

                
                
        if button_machine.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)

                soundBackGroundStop(isSound)
                soundGamePlay(isSound)

                isCross, algorithms = menuInit(screen, isSound)
                if isCross != None or algorithms != None:
                    dataInit = initGameScreen(screen)
                    gameScreen(screen, dataInit, isSound, True, isCross, algorithms, None)

        if button_sound.collidepoint((mouse_X, mouse_Y)):
            if click:
                isSound = False if isSound else True
                if isSound:
                    soundClickPlay(isSound)
                    soundMenuPlay(isSound)
                else:
                    soundBackGroundStop(isSound)
        if button_quit.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                pygame.quit()
        
        if button_AI_combat.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                
                algorithms_A, algorithms_B = menuAICombat(screen, isSound)

                if algorithms_A != None and algorithms_B != None:
                    soundClickPlay(isSound)
                    soundBackGroundStop(isSound)
                    soundGamePlay(isSound)

                    dataInit = initGameScreen(screen)
                    AICombatScreen(screen, dataInit, isSound, algorithms_A, algorithms_B)
                print(algorithms_A, algorithms_B)

        pygame.display.update()
        fpsClock.tick(FPS)

def PlayerCombat(screen, client, isSound):
    username = 'Tên người chơi'
    opponent = 'Tên đối thủ'
    canPlay = False
    canInputUsername = True
    canInputOpponent = True
    active_input = None

    font = pygame.font.Font(font_path, 30)

    while True:
        screen.fill((218, 241, 172))

        logo = pygame.image.load(logo_path)
        screen.blit(logo, (0,-125))

        button_ui = pygame.image.load(button_path)
        group_icon = pygame.image.load(icon_path)
        group_icon = pygame.transform.scale(group_icon,(32, 32))

        button_offline = pygame.Rect(220, 260, 380, 90)
        text_offline =textFormat("Chơi offline", font_path, 40, (255,255,255)) 
        screen.blit(button_ui, (210, 255))
        screen.blit(text_offline, (300, 267))

        screen.blit(button_ui, (5, 355))
        input_username_rect = pygame.Rect(25, 370, 360, 65)
        pygame.draw.rect(screen, (255, 255, 255), input_username_rect, 2)
        username_surface = font.render(username, True, (0, 0, 0))
        screen.blit(username_surface, (input_username_rect.x + 5, input_username_rect.y + 5))

        screen.blit(button_ui, (395, 355))
        input_opponent_rect = pygame.Rect(415, 370, 360, 65)
        pygame.draw.rect(screen, (255, 255, 255), input_opponent_rect, 2)
        opponent_surface = font.render(opponent, True, (0, 0, 0))
        screen.blit(opponent_surface, (input_opponent_rect.x + 5, input_opponent_rect.y + 5))

        button_login = pygame.Rect(15, 460, 380, 90)
        text_login =textFormat("Đăng nhập", font_path, 40, (255,255,255)) 
        screen.blit(button_ui, (5, 455))
        screen.blit(text_login, (95, 467))

        button_online = pygame.Rect(405, 460, 380, 90)
        text_online =textFormat("Chơi online", font_path, 40, (255,255,255)) 
        screen.blit(button_ui, (395, 455))
        screen.blit(text_online, (485, 467))

        button_ui = pygame.transform.scale(button_ui,(64, 64))
        button_back = pygame.Rect(727, 270, 64, 64)
        screen.blit(button_ui, (727, 270))
        screen.blit(group_icon, (745, 288))
        
        mouse_X, mouse_Y = pygame.mouse.get_pos()
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    if input_username_rect.collidepoint((mouse_X, mouse_Y)) and canInputUsername:
                        active_input = 'username'
                    elif input_opponent_rect.collidepoint((mouse_X, mouse_Y)) and canInputOpponent:
                        active_input = 'opponent'
                    else:
                        active_input = None
            if event.type == pygame.KEYDOWN:
                if active_input == 'username':
                    if event.key == pygame.K_BACKSPACE:
                        username = ''
                    else:
                        username += event.unicode
                elif active_input == 'opponent':
                    if event.key == pygame.K_BACKSPACE:
                        # opponent = opponent[:-1]
                        opponent = ''
                    else:
                        opponent += event.unicode
            # print(mouse_X, mouse_Y)
        
        if button_offline.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)

                return "", ""
        
        if button_login.collidepoint((mouse_X, mouse_Y)) and canInputUsername:
            if click:
                soundClickPlay(isSound)
                if username == 'Tên người chơi':
                    showMessageBox("Cảnh báo!", "Vui lòng nhập thông tin người chơi.")
                    continue
                elif username == '':
                    showMessageBox("Cảnh báo!", "Vui lòng nhập thông tin người chơi.")
                    continue
                

                if client.inputUsername(username) == False: 
                    showMessageBox("Cảnh báo!", "Vui lòng chỉnh sửa tên người chơi.")
                    continue

                canPlay = True
                canInputUsername = False
                showMessageBox("Thông báo", "Đăng nhập thành công hãy điền thông tin đối thủ.")
            
        if button_online.collidepoint((mouse_X, mouse_Y)) and canInputOpponent:
            if click:
                soundClickPlay(isSound)

                if opponent == 'Tên đối thủ':
                    showMessageBox("Cảnh báo!", "Vui lòng nhập thông tin đối thủ.")
                    continue
                elif opponent == '':
                    showMessageBox("Cảnh báo!", "Vui lòng nhập thông tin đối thủ.")
                    continue

                if canPlay:
                    if client.inputOpponent(opponent) == False:
                        showMessageBox("Cảnh báo!", "Vui lòng chỉnh sửa tên tối thủ.")
                        continue
                    
                    canInputOpponent = False
                    print(f"Người chơi {username} thách đấu {opponent}")
                    return username, opponent
                else:
                    showMessageBox("Cảnh báo!", "Vui lòng đăng nhập.")

        
        if button_back.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                
                return None, None

        pygame.display.update()
        fpsClock.tick(FPS)


def menuInit(screen, isSound):
    algorithms = 1 # 1 Greedy/ 2 AlphaBeta/ 3 A*/ 4 UCS
    while True:
        screen.fill((218, 241, 172))
        option = pygame.image.load(menu_init_path)
        screen.blit(option, (-1, -1))

        button_exit = pygame.Rect(480, 500, 100, 60)
        button_o = pygame.Rect(270, 370, 110, 110)
        button_x = pygame.Rect(450, 370, 110, 110)

                
        button_ui = pygame.image.load(button_path)
        button_ui = pygame.transform.scale(button_ui,(180, 64))
        screen.blit(button_ui, (20, 300))
        screen.blit(button_ui, (20, 400))
        button_Greedy = pygame.Rect(20, 300, 180, 64)
        button_AS = pygame.Rect(20, 400, 180, 64)
        text_Greedy =textFormat("Greedy", font_path, 30, (255,255,255))
        text_AS =textFormat("A*", font_path, 30, (255,255,255))

        if algorithms == 1:
            text_Greedy =textFormat("Greedy", font_path, 30, (255,50,50))
        elif algorithms == 2:
            text_AS =textFormat("A*", font_path, 30, (255,50,50))

        screen.blit(text_Greedy, (45, 310))
        screen.blit(text_AS, (38, 410))

        mouse_X, mouse_Y = pygame.mouse.get_pos()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # data.saveData()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # print(mouse_X, mouse_Y)
                    click = True
        
        if button_Greedy.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                algorithms = 1
        if button_AS.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                algorithms = 2

        if button_x.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                return -1, algorithms
        if button_o.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                return 1, algorithms
        if button_exit.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                return None, None
                

        pygame.display.update()
        fpsClock.tick(FPS)


def menuAICombat(screen, isSound):
    algorithms_A = 1
    algorithms_B = 1
    while True:
        screen.fill((218, 241, 172))
        logo = pygame.image.load(logo_path)
        screen.blit(logo, (0,-125))

        button_ui = pygame.image.load(button_path)
        group_icon = pygame.image.load(icon_path)
        group_icon = pygame.transform.scale(group_icon,(32, 32))
        button_ui = pygame.transform.scale(button_ui,(64, 64))
        button_AI_combat = pygame.Rect(727, 530, 64, 64)
        screen.blit(button_ui, (727, 530))
        screen.blit(group_icon, (745, 548))

        start_icon = pygame.image.load(start_icon_path)
        start_icon = pygame.transform.scale(start_icon,(32, 32))
        button_ui = pygame.transform.scale(button_ui,(64, 64))
        button_start_combat = pygame.Rect(727, 460, 64, 64)
        screen.blit(button_ui, (727, 460))
        screen.blit(start_icon, (745, 478))

        button_ui = pygame.transform.scale(button_ui,(180, 64))

        screen.blit(button_ui, (20, 340))
        screen.blit(button_ui, (20, 410))
        button_Greedy_A = pygame.Rect(20, 340, 180, 64)
        button_AS_A = pygame.Rect(20, 410, 180, 64)
        text_Greedy_A =textFormat("Greedy", font_path, 30, (255,255,255))
        text_AS_A =textFormat("A*", font_path, 30, (255,255,255))

        if algorithms_A == 1:
            text_Greedy_A =textFormat("Greedy", font_path, 30, (255,50,50))
        elif algorithms_A == 2:
            text_AS_A =textFormat("A*", font_path, 30, (255,50,50))

        screen.blit(text_Greedy_A, (45, 350))
        screen.blit(text_AS_A, (100, 420))

        text_menu =textFormat("VS", font_path, 200, (0,0,0))
        screen.blit(text_menu, (230, 215))
        text_menu =textFormat("AI-COMBAT", font_path, 30, (0,0,0))
        screen.blit(text_menu, (280, 470))

        screen.blit(button_ui, (520, 340))
        screen.blit(button_ui, (520, 410))
        button_Greedy_B = pygame.Rect(520, 340, 180, 64)
        button_AS_B = pygame.Rect(520, 410, 180, 64)
        text_Greedy_B =textFormat("Greedy", font_path, 30, (255,255,255))
        text_AS_B =textFormat("A*", font_path, 30, (255,255,255))

        if algorithms_B == 1:
            text_Greedy_B =textFormat("Greedy", font_path, 30, (255,50,50))
        elif algorithms_B == 2:
            text_AS_B =textFormat("A*", font_path, 30, (255,50,50))

        screen.blit(text_Greedy_B, (545, 350))
        screen.blit(text_AS_B, (600, 420))



        mouse_X, mouse_Y = pygame.mouse.get_pos()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # print(mouse_X, mouse_Y)
                    click = True
        
        if button_Greedy_A.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                algorithms_A = 1
        if button_AS_A.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                algorithms_A = 2
        
        if button_Greedy_B.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                algorithms_B = 1
        if button_AS_B.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                algorithms_B = 2

        if button_AI_combat.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                return None, None
        
        if button_start_combat.collidepoint((mouse_X, mouse_Y)):
            if click:
                soundClickPlay(isSound)
                return algorithms_A, algorithms_B
                

        pygame.display.update()
        fpsClock.tick(FPS)

def nameLenToIsCross(username, opponent):
    if username > opponent:
        return True
    elif username < opponent:
        return False
    else:
        if len(username) > len(opponent):
            return True
        elif len(username) < len(opponent):
            return False
        else:
            showMessageBox("Lỗi!", "Lỗi hệ thống khi so sánh tên người chơi.")
            pygame.quit()

def initGameScreen(screen):
    res = (WINDOW_HEIGHT/GRID_SIZE - 1)
    borders = int((WINDOW_HEIGHT - res * GRID_SIZE)/ 2)
    screen.fill((218, 241, 172))
    square = pygame.image.load(square_path)
    square = pygame.transform.scale(square,(res,res))
    cross = pygame.image.load(x_path)
    cross = pygame.transform.scale(cross,(int((2/3)*res),int((2/3)*res)))
    circle = pygame.image.load(o_path)
    circle = pygame.transform.scale(circle,(int((2/3)*res),int((2/3)*res)))
    suggest = pygame.image.load(x2_path)
    suggest = pygame.transform.scale(suggest,(int((2/3)*res),int((2/3)*res)))
    for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                screen.blit(square,(i*res+borders,j*res+borders))
    
    return [res, cross, circle, square, suggest]

def gameScreen(screen, initData, isSound, isMachine, isCross, algorithms, online):
    gameOption(isMachine, isCross, algorithms)
    while True:
        isWin = gameStatus(screen, initData, isCross, isSound)
        if isWin:
            soundBackGroundStop(isSound)
            soundMenuPlay(isSound)
            return

        game_button = pygame.image.load(game_button_path)
        screen.blit(game_button, (0, 0))

        icon_machine  = pygame.image.load(user_icon_path)

        machine_A_icon = pygame.Rect(698, 498, 80, 80)
        pygame.draw.rect(screen, (255, 255, 255), machine_A_icon)
        machine_A_icon = pygame.transform.scale(icon_machine,(70, 70))
        screen.blit(machine_A_icon, (704, 504))

        rival_icon = pygame.Rect(700, 20, 78, 78)
        pygame.draw.rect(screen, (255, 255, 255), rival_icon)    

        if isMachine:
            rival_icon = pygame.image.load(robot_icon_path)
            if algorithms == 1:
                text_rival = "Greedy"
            elif algorithms == 2:
                text_rival = "A*"
        else:
            rival_icon = pygame.image.load(user_icon_path)
            text_rival = "Người chơi"

        if online != None:
            rival_icon = pygame.image.load(user_icon_path)
            if isCross:
                text_user  = online[0] 
                text_rival = online[1]
            else:
                text_rival = online[0]
                text_user  = online[1]

            if online[0] == "":
                text_user  = "Nhóm 2"
        else:
            text_user  = "Nhóm 2"

        text_user = textFormat(text_user, font_path, 30, (0,0,0)) 
        screen.blit(text_user, (620, 445))

        rival_icon = pygame.transform.scale(rival_icon,(70, 70))
        screen.blit(rival_icon, (704, 24))
        text_rival = textFormat(text_rival, font_path, 30, (0,0,0)) 
        screen.blit(text_rival, (617, 100))

        exit_button = pygame.Rect(740, 387, 38, 38)
        back_button = pygame.Rect(680, 387, 38, 38)
        suggest_button = pygame.Rect(680, 340, 38, 38)
        giveup_button = pygame.Rect(740, 340, 38, 38)


        buttonArray = [exit_button, back_button, suggest_button, giveup_button]

        inputStatus = evenInput(screen, initData, buttonArray, isCross, isSound, online)
        if exitButton(screen , initData, exit_button, inputStatus[0], isSound, online):
            soundBackGroundStop(isSound)
            soundMenuPlay(isSound)
            return
        
        pygame.display.update()
        fpsClock.tick(FPS)

def AICombatScreen(screen, initData, isSound, algorithms_A, algorithms_B):
    gameOption(False, -1, 0)
    while True:
        isWin = gameStatus(screen, initData, -1, isSound)
        if isWin:
            return

        game_button = pygame.image.load(game_button_AI_combat_path)
        screen.blit(game_button, (0, 0))

        if algorithms_A == 1:
            text_name_A = "Greedy"
        elif algorithms_A == 2:
            text_name_A = "A*"
        
        if algorithms_B == 1:
            text_name_B = "Greedy"
        elif algorithms_B == 2:
            text_name_B = "A*"
        
        icon_machine  = pygame.image.load(robot_icon_path)

        machine_A_icon = pygame.Rect(698, 498, 80, 80)
        pygame.draw.rect(screen, (255, 255, 255), machine_A_icon)
        machine_A_icon = pygame.transform.scale(icon_machine,(70, 70))
        screen.blit(machine_A_icon, (704, 504))
        text_machine_A = textFormat(text_name_A, font_path, 30, (0,0,0)) 
        screen.blit(text_machine_A, (617, 445))

        machine_B_icon = pygame.Rect(700, 20, 78, 78)
        pygame.draw.rect(screen, (255, 255, 255), machine_B_icon)
        machine_B_icon = pygame.transform.scale(icon_machine,(70, 70))
        screen.blit(machine_B_icon, (704, 24))
        text_machine_B = textFormat(text_name_B, font_path, 30, (0,0,0)) 
        screen.blit(text_machine_B, (617, 100))

        exit_button = pygame.Rect(740, 365, 100, 40)

        inputStatus = evenInputAICombat(screen, initData, algorithms_A, algorithms_B, isSound)
        if exitButton(screen , initData, exit_button, inputStatus[0], isSound, None):
            soundBackGroundStop(isSound)
            soundMenuPlay(isSound)
            return
        
        pygame.display.update()
        fpsClock.tick(FPS)