
# coding: utf-8

import argparse
import os
import numpy as np
import math
import torchvision.transforms as transforms
from torchvision.utils import save_image
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch

os.makedirs('new_images', exist_ok=True)

'''
Set Defaults
'''
num_epochs = 200
batch_size = 64
num_classes = 10 # number of classes for dataset
lr = 0.0002
b1 = 0.5 # adam: decay of first order momentum of gradient
b2 = 0.999 # adam: decay of first order momentum of gradient
n_cpu = 8 # number of cpu threads to use during batch generation
latent_dim = 100 # dimensionality of the latent space
img_size = 32 # size of each image dimension
channels = 1 # number of output image channels
sample_interval = 400 # interval between image sampling

# Set cuda
if torch.cuda.is_available():
    cuda = True
else:
    cuda = False

def weights_init_normal(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.zero_()


class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()

        self.label_emb = nn.Embedding(num_classes, latent_dim)
        self.init_size = img_size // 4 # Initial size before upsampling

        self.linear = nn.Sequential(
            nn.Linear(latent_dim, 128*self.init_size**2),
        )
        self.conv1 = nn.Sequential(
            nn.BatchNorm2d(num_features=128),
            nn.ConvTranspose2d(in_channels=128, out_channels=128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(num_features=128, eps=0.8),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.conv2 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(num_features=64, eps=0.8),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.conv3 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=64, out_channels=channels, kernel_size=4, stride=2, padding=1),
            nn.Tanh()
        )

    def forward(self, noise):
        print('--------')
        print(noise.size())
        out = self.linear(noise)
        print(out.size())
        out = out.view(out.shape[0], 128, self.init_size, self.init_size)
        print(out.size())
        img = self.conv1(out)
        print(img.size())
        img = self.conv2(img)
        print(img.size())
        img = self.conv3(img)
        print(img.size())
        print('---------')
        return img

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=channels, out_channels=16, kernel_size=3, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Dropout2d(0.25),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Dropout2d(0.25),
            nn.BatchNorm2d(num_features=32, eps=0.8)
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Dropout2d(0.25),
            nn.BatchNorm2d(num_features=64, eps=0.8)
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Dropout2d(0.25),
            nn.BatchNorm2d(num_features=128, eps=0.8)
        )

        # The height and width of downsampled image
        ds_size = img_size // 2**4

        # Output layers
        self.adv_layer = nn.Sequential(
            nn.Linear(in_features=128*ds_size**2, out_features=1),
            nn.Sigmoid()
        )
        self.aux_layer = nn.Sequential(
            nn.Linear(in_features=128*ds_size**2, out_features=num_classes+1),
            nn.Softmax()
        )

    def forward(self, img):
        out = self.conv1(img)
        out = self.conv2(out)
        out = self.conv3(out)
        out = self.conv4(out)

        out = out.view(out.shape[0], -1)
        validity = self.adv_layer(out)
        label = self.aux_layer(out)

        return validity, label

# Loss functions
adversarial_loss = torch.nn.BCELoss()
auxiliary_loss = torch.nn.CrossEntropyLoss()

# Initialize generator and discriminator
generator = Generator()
discriminator = Discriminator()

if cuda:
    generator.cuda()
    discriminator.cuda()
    adversarial_loss.cuda()
    auxiliary_loss.cuda()

# Initialize weights
generator.apply(weights_init_normal)
discriminator.apply(weights_init_normal)

# Configure DataLoader
DATA_FOLDER = './torch_data/MNIST'

def mnist_data():
    compose = transforms.Compose([
        transforms.Resize(img_size),
        transforms.ToTensor(),
        transforms.Normalize((.5, .5, .5), (.5, .5, .5))
        ])
    out_dir = '{}/dataset'.format(DATA_FOLDER)
    return datasets.MNIST(root=out_dir, train=True, transform=compose, download=True)

data = mnist_data()
dataloader = torch.utils.data.DataLoader(data, batch_size=batch_size, shuffle=True)

# Optimizers
optimizer_G = torch.optim.Adam(generator.parameters(), lr=lr, betas=(b1, b2))
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=lr, betas=(b1, b2))

FloatTensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor
LongTensor = torch.cuda.LongTensor if cuda else torch.LongTensor

# Defining ground-truth for real and fake images

def real_data_groundtruth(size):
    '''
    Variable containing ones, with shape = size, 1
    '''
    data = Variable(torch.ones(size, 1), requires_grad=False)
    if torch.cuda.is_available():
        return data.cuda()
    return data

def fake_data_groundtruth(size):
    '''
    Variable containing zeros, with shape = size, 1
    '''
    data = Variable(torch.zeros(size, 1), requires_grad=False)
    if torch.cuda.is_available():
        return data.cuda()
    return data

def fake_aux_groundtruth(size):
    '''
    Variable containing num_classes+1, with shape = size
    '''
    data = Variable(LongTensor(size).fill_(num_classes), requires_grad=False)
    return data


def noise(size):
    n = Variable(torch.randn(size, latent_dim))
    if torch.cuda.is_available():
        return n.cuda()
    else:
        return n


def train_discriminator(optimizer_D, real_imgs, fake_imgs, labels):
    optimizer_D.zero_grad()

    # Loss for real images
    real_pred, real_aux = discriminator(real_imgs)
    d_real_loss =  (adversarial_loss(real_pred, valid) + auxiliary_loss(real_aux, labels)) / 2.0

    # Loss for fake images
    fake_pred, fake_aux = discriminator(fake_imgs)
    d_fake_loss =  (adversarial_loss(fake_pred, fake) + auxiliary_loss(fake_aux, fake_aux_gt)) / 2.0

    # Total discriminator loss
    d_loss = (d_real_loss + d_fake_loss) / 2.0

    # Calculate discriminator accuracy
    pred = np.concatenate([real_aux.data.cpu().numpy(), fake_aux.data.cpu().numpy()], axis=0)
    gt = np.concatenate([labels.data.cpu().numpy(), fake_aux_gt.data.cpu().numpy()], axis=0)
    d_acc = np.mean(np.argmax(pred, axis=1) == gt)

    d_loss.backward()
    optimizer_D.step()

    return d_loss, d_acc

def train_generator(optimizer_G, gen_imgs):
    optimizer_G.zero_grad()

    # Loss measures generator's ability to fool the discriminator
    validity, _ = discriminator(gen_imgs)
    g_loss = adversarial_loss(validity, valid)

    g_loss.backward()
    optimizer_G.step()

    return g_loss

'''
Start Training
'''
for epoch in range(num_epochs):
    for i, (imgs, labels) in enumerate(dataloader):

        batch_size_ = imgs.shape[0]

        # Adversarial ground truths
        valid = real_data_groundtruth(batch_size_)
        fake = fake_data_groundtruth(batch_size_)
        fake_aux_gt = fake_aux_groundtruth(batch_size_)

        # Configure input
        real_imgs = Variable(imgs.type(FloatTensor))
        labels = Variable(labels.type(LongTensor))

        ###############################################
        #              Train Generator                #
        ###############################################

        gen_imgs = generator(noise(batch_size_))
        g_loss = train_generator(optimizer_G, gen_imgs)

        ###############################################
        #              Train Discriminator            #
        ###############################################

        fake_imgs = generator(noise(batch_size_)).detach()
        d_loss, d_acc = train_discriminator(optimizer_D, real_imgs, fake_imgs, labels)

        # Display Progress
        print ("[Epoch %d/%d] [Batch %d/%d] [D loss: %f, acc: %d%%] [G loss: %f]" % (epoch, num_epochs, i, len(dataloader),
                                                            d_loss.item(), 100 * d_acc,
                                                            g_loss.item()))

        batches_done = epoch * len(dataloader) + i
        if batches_done % sample_interval == 0:
            save_image(gen_imgs.data[:25], 'new_images/%d.png' % batches_done, nrow=5, normalize=True)
