import train, inference
import os


n = int(input('1)학습\n2)하나의 이미지 추론\n3)여러개 이미지 추론\n : '))

if n == 1:
    train.run()
elif n == 2:
    img_path = input('추론 이미지 경로 입력 : ')
    who = inference.run(img_path)
    print(who)
elif n == 3:
    path = "../static/login"
    person = []
    for i in range(1, 4):
        who = inference.run(path + "/hyemin" + str(i) + ".png")
        person.append(who)
    print("\n\n")
    print(person)
