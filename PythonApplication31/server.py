import socket
import pickle
import random
host = socket.gethostbyname(socket.gethostname())       #приймає айпі з якого ти сидишь в данний момент
port = 58121 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port)) #зв'язує socket з host, port
print(host, port)
serversocket.listen(2)       #чекає поки не запуститься 2 клієнти
arr = [400,400,400,400,0,0]  #1-розташування л.ракетки, 2-пр.ракетки, 3,4-розташування м'ячика, 5,6-початкові данні рахунку
connection = []
ball_y_speed = 1
ball_x_speed = 1



def process_positions(array, player_1, player_2):
    global ball_y_speed, ball_x_speed


    '''PADDLE MOVING'''
    if player_1[0] == True: 
        array[0]-=1            #рух лівої планки вниз
    else:
        array[0] = array[0]
    if player_1[1] == True:
        array[0]+=1            #рух лівої планки вверх
    else:
        array[0] = array[0]

    if player_2[0] == True:
        array[1]-=1            #рух правої планки вниз
    else:
        array[1] = array[1]
    if player_2[1] == True:
        array[1]+=1            #рух правої планки вверх
    else:
        array[1] = array[1]

    if array[0]<0:
        array[0] = 0           #встановлює обмеження для лівої планки
    elif array[0] > 540:
        array[0] = 540          

    if array[1]<0:
        array[1] = 0           #встановлює обмеження для правої планки
    elif array[1] > 540:
        array[1] = 540

    '''PADDLE MOVING'''

    '''BALL MOVING'''
    array[2] += round(ball_y_speed)
    array[3] += round(ball_x_speed)

    negative_speed = [-0.85, -0.9, -0.95, -1]
    positive_speed = [-1, -1.05, -1.1, -1.15, -1.2]

    if array[2] > 595:  #відбиваєтьмя від низу
        if ball_y_speed >= 1:
            ball_y_speed *= random.choice(negative_speed)
        elif ball_y_speed < 1:
            ball_y_speed *= random.choice(positive_speed)
    if array[2] < 0:   #відбиваєтьмя від верху
        if ball_y_speed >= 1:
            ball_y_speed *= random.choice(negative_speed)
        elif ball_y_speed < 1:
            ball_y_speed *= random.choice(positive_speed)
    if array[3]>795:  #якщо м'як торкається правої стінки
        if ball_x_speed >= 1:
            ball_x_speed *= random.choice(negative_speed)
        elif ball_x_speed < 1:
            ball_x_speed *= random.choice(positive_speed)
        array[4] += 1  #додавання голів
    if array[3]<0:   #якщо м'як торкається лівої стінки
        if ball_x_speed >= 1:
            ball_x_speed *= random.choice(negative_speed)
        elif ball_x_speed < 1:
            ball_x_speed *= random.choice(positive_speed)
        array[5] += 1  #додавання голів

    '''BALL MOVING'''


    '''PADDLE DETECTION'''
    if array[3]<20 and (array[0]<array[2] and array[0]+60>array[2]): #для відбивання м'яча від лівої планки
        ball_x_speed *=-1
    if array[3]>780 and (array[1]<array[2] and array[1]+60>array[2]): #для відбивання м'яча від правої планки
        ball_x_speed *=-1


    return array

def waiting_for_connections():
    while len(connection)<2:
        conn, addr = serversocket.accept() #встановлює з'єднання з клієнтом
        connection.append(conn)
        

def recieve_information(): 
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info


while True:
    waiting_for_connections()

    data_arr = pickle.dumps(arr)
    print(data_arr) 
    connection[0].send(data_arr)
    connection[1].send(data_arr)

    player1, player2 = recieve_information()

    arr = process_positions(arr,player1, player2)
