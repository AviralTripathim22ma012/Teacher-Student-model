# -*- coding: utf-8 -*-
"""minor_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wg8VQ6LsLO-HXgYztgbzvzJiJNRj3szo

**IMPORTING REQUIRED LIBERARIES**
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torchvision

!pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu111/torch_stable.html

"""**DEFINING THE TEACHER MODEL**"""

import torch
import torch.nn as nn

class TeacherModel(nn.Module):
    def __init__(self):
        super(TeacherModel, self).__init__()
        
        # Define the convolutional layers
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=8, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=10, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=10, out_channels=12, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(in_channels=12, out_channels=14, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(in_channels=14, out_channels=16, kernel_size=3, padding=1)
        self.conv6 = nn.Conv2d(in_channels=16, out_channels=18, kernel_size=3, padding=1)
        self.conv7 = nn.Conv2d(in_channels=18, out_channels=20, kernel_size=3, padding=1)
        self.conv8 = nn.Conv2d(in_channels=20, out_channels=22, kernel_size=3, padding=1)
        self.conv9 = nn.Conv2d(in_channels=22, out_channels=24, kernel_size=3, padding=1)
        self.conv10 = nn.Conv2d(in_channels=24, out_channels=100, kernel_size=3, padding=1)
        
        # Define the pooling layers
        self.pool1 = nn.AvgPool2d(kernel_size=2, stride=2) #kernel_size=2, stride=2
        self.pool2 = nn.AvgPool2d(kernel_size=2, stride=2)
        
        # Define the fully connected layer
        self.fc = nn.Linear(in_features=100, out_features=512)
        
    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = self.pool1(nn.functional.relu(self.conv2(x)))
        x = nn.functional.relu(self.conv3(x))
        x = self.pool2(nn.functional.relu(self.conv4(x)))
        x = nn.functional.relu(self.conv5(x))
        x = self.pool2(nn.functional.relu(self.conv6(x)))
        x = nn.functional.relu(self.conv7(x))
        x = self.pool2(nn.functional.relu(self.conv8(x)))
        x = nn.functional.relu(self.conv9(x))
        x = self.pool2(nn.functional.relu(self.conv10(x)))
        x = torch.flatten(x, start_dim=1)
        x = nn.functional.relu(self.fc(x))
        return x

"""**IMPORTING THE DATA FROM GitHUB**"""

! git clone https://github.com/seshuad/IMagenet
! ls 'IMagenet/tiny-imagenet-200/'

"""**CREATING DATA DIRECTORIES**"""

import time
import imageio as nd
import numpy as np

path = 'IMagenet/tiny-imagenet-200/'

def get_id_dictionary():
    id_dict = {}
    for i, line in enumerate(open( path + 'wnids.txt', 'r')):
        id_dict[line.replace('\n', '')] = i
    return id_dict
  
def get_class_to_id_dict():
    id_dict = get_id_dictionary()
    all_classes = {}
    result = {}
    for i, line in enumerate(open( path + 'words.txt', 'r')):
        n_id, word = line.split('\t')[:2]
        all_classes[n_id] = word
    for key, value in id_dict.items():
        result[value] = (key, all_classes[key])      
    return result

def get_data(id_dict):
    print('starting loading data')
    train_data, test_data = [], []
    train_labels, test_labels = [], []
    t = time.time()
    for key, value in id_dict.items():
        train_data += [nd.imread( path + 'train/{}/images/{}_{}.JPEG'.format(key, key, str(i)), pilmode='RGB') for i in range(500)]
        train_labels_ = np.array([[0]*200]*500)
        train_labels_[:, value] = 1
        train_labels += train_labels_.tolist()

    for line in open( path + 'val/val_annotations.txt'):
        img_name, class_id = line.split('\t')[:2]
        test_data.append(nd.imread( path + 'val/images/{}'.format(img_name) ,pilmode='RGB'))
        test_labels_ = np.array([[0]*200])
        test_labels_[0, id_dict[class_id]] = 1
        test_labels += test_labels_.tolist()

    print('finished loading data, in {} seconds'.format(time.time() - t))
    return np.array(train_data), np.array(train_labels), np.array(test_data), np.array(test_labels)
  
train_data, train_labels, test_data, test_labels = get_data(get_id_dictionary())

print( "train data shape: ",  train_data.shape )
print( "train label shape: ", train_labels.shape )
print( "test data shape: ",   test_data.shape )
print( "test_labels.shape: ", test_labels.shape )

"""**DEFINING TRANSFORMS, AND LOADING THE DATA INTO TRAINLOADER AND VALLOADER**"""

import torch
import torchvision
import torchvision.transforms as transforms

'''# Define the path to the Tiny ImageNet dataset'''
data_dir = "/content/IMagenet/tiny-imagenet-200"

'''# Define the transformation to be applied to the data'''
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.RandomCrop(64, padding=4),
    transforms.Resize((32, 32)), # Resize the image to match the input size of the CNN
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

'''# Load the train and validation datasets'''
trainset = torchvision.datasets.ImageFolder(root=data_dir+'/train', transform=transform)
valset = torchvision.datasets.ImageFolder(root=data_dir+'/val', transform=transform)

'''# Create data loaders to load the data in batches'''
trainloader = torch.utils.data.DataLoader(trainset, batch_size=1024, shuffle=True, num_workers=2, pin_memory=True)
valloader = torch.utils.data.DataLoader(valset, batch_size=1024, shuffle=False, num_workers=2, pin_memory=True)

"""**CHECKING IF CUDA GPU IS AVAILABLE**"""

'''#checking if CUDA is available'''
device = 'cuda' if torch.cuda.is_available() else 'cpu'
teacher_net = TeacherModel().to(device)

print(device)

"""**TRAINING THE TEACHER MODEL**"""

'''# define the model, optimizer and loss function'''
import torch.optim as optim

teacher_net = TeacherModel().to(device)
optimizer = optim.Adam(teacher_net.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

num_epochs= 5
'''# train the model'''
for epoch in range(num_epochs):

    # set the model to training mode
    teacher_net.train()

    # iterate over the batches
    for i, (inputs, labels) in enumerate(trainloader):

        # move the data to the device
        inputs = inputs.to(device)
        labels = labels.to(device)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward pass
        outputs = teacher_net(inputs)

        # compute the loss
        loss = criterion(outputs, labels)

        # backward pass
        loss.backward()

        # update the parameters
        optimizer.step()

        # print statistics
        if i % 100 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(trainloader)}], Loss: {loss.item():.4f}")

    # evaluate the model on the test set
    teacher_net.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for inputs, labels in trainloader:
            # move the data to the device
            inputs = inputs.to(device)
            labels = labels.to(device)

            # forward pass
            outputs = teacher_net(inputs)

            # compute the predictions
            _, predicted = torch.max(outputs.data, 1)

            # update the metrics
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        # print the accuracy
        print(f"Epoch [{epoch+1}/{num_epochs}], Test Accuracy: {(100 * correct / total):.2f}%")

"""**STUDENT MODEL**"""

import torch
import torch.nn as nn

class StudentModel(nn.Module):
    def __init__(self):
        super(StudentModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.AvgPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64*4*4, 512)
        self.fc2 = nn.Linear(512, 10)

    def forward(self, x):
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.relu(self.conv2(x))
        x = self.pool(nn.functional.relu(self.conv3(x)))
        x = torch.flatten(x, start_dim=1)
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.log_softmax(self.fc2(x), dim=1)
        return x

"""**TRAINING THE STUDENT MODEL**"""

device = 'cuda' if torch.cuda.is_available() else 'cpu'
teacher_net = TeacherModel().to(device)
student_net = StudentModel().to(device)

print(device)

"""**TRAINING FUNCTION FOR STUDENT**"""

'''# knowledge distillation loss'''

def loss_fn_kd(outputs, labels, teacher_outputs, temperature):
    soft_outputs = nn.functional.softmax(outputs / temperature, dim=1)
    soft_teacher_outputs = nn.functional.softmax(teacher_outputs / temperature, dim=1)
    return nn.KLDivLoss()(soft_outputs, soft_teacher_outputs) * (temperature ** 2)

'''# Define the training function'''

def train_student_model(student_net, teacher_net, train_loader, optimizer, criterion, temperature, alpha, device):
    student_net.train()
    teacher_net.eval()
    train_loss = 0
    train_acc = 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        with torch.no_grad():
            teacher_outputs = teacher_net(inputs)
        outputs = student_net(inputs)
        loss = criterion(outputs, labels) * (1 - alpha) + loss_fn_kd(outputs, labels, teacher_outputs, temperature) * alpha
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * inputs.size(0)
        train_acc += (outputs.argmax(1) == labels).sum().item()
    train_loss /= len(train_loader.dataset)
    train_acc /= len(train_loader.dataset)
    return train_loss, train_acc

"""**TESTING FUNCTION FOR STUDENT**"""

'''# Define the testing function'''

def test_student_model(student_net, test_loader, criterion, device):
    student_net.eval()
    test_loss = 0
    test_acc = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = student_net(inputs)
            loss = criterion(outputs, labels)
            test_loss += loss.item() * inputs.size(0)
            test_acc += (outputs.argmax(1) == labels).sum().item()
    test_loss /= len(test_loader.dataset)
    test_acc /= len(test_loader.dataset)
    return test_loss, test_acc

import torch
import torchvision
import torchvision.transforms as transforms

'''# Define the path to the Tiny ImageNet dataset'''
data_dir = "/content/IMagenet/tiny-imagenet-200"

'''# Define the transformation to be applied to the data'''
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.RandomCrop(64, padding=4),
    transforms.Resize((128, 128)), # Resize the image to match the input size of the CNN
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

'''# Load the train and validation datasets'''
trainset = torchvision.datasets.ImageFolder(root=data_dir+'/train', transform=transform)
valset = torchvision.datasets.ImageFolder(root=data_dir+'/val', transform=transform)

'''# Create data loaders to load the data in batches'''
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True, num_workers=2, pin_memory=True)
valloader = torch.utils.data.DataLoader(valset, batch_size=64, shuffle=False, num_workers=2, pin_memory=True)

train_student = train_student_model(student_net, teacher_net, trainloader, optimizer, criterion, 3, 0.3, device)
test_loss, test_acc_ema = test_student_model(StudentModel, trainloader, criterion, ema, device)
print('Test Loss with EMA: {:.4f}, Test Accuracy with EMA: {:.4f}'.format(test_loss, test_acc))

"""**TRAINING FUNCTION FOR STUDENT WITH EMA**"""

'''# Define the training function with EMA'''

import torch.nn.functional as F
from torch.optim.lr_scheduler import MultiStepLR

def train_student_model_ema(student_net, teacher_net, train_loader, criterion, optimizer, ema_alpha, device):
    student_net.train()
    teacher_net.eval()
    for param in teacher_net.parameters():
        param.requires_grad = False
    ema = EMA(ema_alpha)
    ema.register(student_net.parameters())
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        student_output = student_net(data)
        teacher_output = teacher_net(data).detach()
        loss = criterion(student_output, target) + F.kl_div(F.log_softmax(student_output, dim=1), F.softmax(teacher_output / 3.0, dim=1), reduction='batchmean') * 3.0 * 3.0
        loss.backward()
        optimizer.step()
        ema(student_net.parameters())
    return ema

"""**TESTING FUNCTION FOR STUDENT WITH EMA**"""

'''# Define the testing function with EMA'''

def test_student_model_ema(student_net, test_loader, criterion, ema, device):
    student_net.eval()
    ema.apply_shadow()
    test_loss = 0
    test_acc = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = student_net(data)
            test_loss += criterion(output, target).item() * data.size(0)
            pred = output.argmax(dim=1, keepdim=True)
            test_acc += pred.eq(target.view_as(pred)).sum().item()
    ema.restore()
    test_loss /= len(test_loader.dataset)
    test_acc /= len(test_loader.dataset)
    return test_loss, test_acc

'''# Test the student model with EMA'''

ema = train_student_model_ema(student_net, teacher_net, train_loader, criterion, optimizer, ema_alpha, device)
test_loss_ema, test_acc_ema = test_student_model_ema(student_net, test_loader, criterion, ema, device)
print('Test Loss with EMA: {:.4f}, Test Accuracy with EMA: {:.4f}'.format(test_loss_ema, test_acc_ema))