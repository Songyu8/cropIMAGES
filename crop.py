import fire
import numpy as np
import cv2
import os
from tqdm import tqdm
import random


def crop(**kwargs):

    folder_path = kwargs.get('path')
    save_path=kwargs.get('save_path')


    for filename in tqdm(os.listdir(folder_path),desc='crop'):
        file_path = os.path.join(folder_path, filename)

        # 检查文件是否为图像文件（可以根据需要添加其他图像文件格式的检查）
        if file_path.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        # 读取图像文件
            image = cv2.imread(file_path)

        
        # 随机生成四个布尔值
        bool_values = [random.choice([True, False]) for _ in range(4)]

        top_left = np.array([[image.shape[1]//random.choice([3,4,5,6]), 0], [image.shape[1], 0], 
                                [image.shape[1], image.shape[0]],[0, image.shape[0]],[0, image.shape[0]//random.choice([3,4,5,6])]])
        
        top_right = np.array([[0, 0], [image.shape[1]-image.shape[1]//random.choice([3,4,5,6]), 0], 
                                [image.shape[1], image.shape[0]//random.choice([3,4,5,6])],[image.shape[1], image.shape[0]],[0, image.shape[0]]])

        bottom_left = np.array([[0, 0], [image.shape[1], 0], 
                                [image.shape[1], image.shape[0]],[image.shape[1]//random.choice([3,4,5,6]), image.shape[0]],[0, image.shape[0]-image.shape[0]//random.choice([3,4,5,6])]])

        bottom_right = np.array([[0, 0], [image.shape[1], 0], 
                                [image.shape[1], image.shape[0]-image.shape[0]//random.choice([3,4,5,6])],[image.shape[1]-image.shape[1]//random.choice([3,4,5,6]), image.shape[0]],[0, image.shape[0]]])
        

        mask_tuple = (top_left, top_right, bottom_left, bottom_right)

        masked_image=np.zeros(image.shape[:2], dtype=np.uint8)


        # 确保至少有一个True
        if not any(bool_values):
            bool_values[random.randint(0, 3)] = True


        for i in range(4):


            if bool_values[i]==True:

                # 创建遮罩图像
                mask = np.zeros(image.shape[:2], dtype=np.uint8)

                # 定义不规则区域的顶点坐标
                points = mask_tuple[i]

                # 在遮罩图像上填充不规则多边形
                cv2.fillPoly(mask, [points], 255)

                # 将遮罩应用于原始图像
                masked_image = cv2.bitwise_and(image, image,mask=mask)

                # 在裁剪部分使用灰色填充
                masked_image[mask == 0] = [0, 0, 0]

                image=masked_image


        os.makedirs(save_path, exist_ok=True)



        cv2.imwrite(os.path.join(save_path,os.path.basename(file_path)[:-4]+'.jpg'),masked_image)





if __name__=='__main__':
    import fire
    fire.Fire(crop)